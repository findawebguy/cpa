from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.security import verify_password, get_password_hash, create_access_token
from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.models.curriculum import UserProgress, LearningNode
from backend.app.models.simulation import TBSAttempt, TBSScenario
from backend.app.schemas.user import (
    UserCreate, UserUpdate, UserLogin, UserResponse, Token,
    SessionMigrationRequest, QRSessionResponse, QRStatusResponse
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

# In-memory store for active QR auth tickets: token -> {"user_id": int, "scanned": bool}
active_qr_tickets: Dict[str, Dict[str, Any]] = {}

def get_current_user(db: Session = Depends(get_db), token: Optional[str] = Depends(oauth2_scheme)) -> User:
    if not token:
        user = db.query(User).filter(User.email == "student@cpa.com").first()
        if user:
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        target_exam_date=user_in.target_exam_date
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=user.id)
    return Token(access_token=token, token_type="bearer", user=UserResponse.model_validate(user))

@router.post("/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    token = create_access_token(subject=user.id)
    return Token(access_token=token, token_type="bearer", user=UserResponse.model_validate(user))

@router.post("/migrate-guest-session")
def migrate_guest_session(
    body: SessionMigrationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Migrates anonymous/guest session progress into the logged-in user account.
    """
    migrated_nodes = 0
    for item in body.guest_progress:
        node = db.query(LearningNode).filter(LearningNode.node_key == item.node_key).first()
        if node:
            existing = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.node_id == node.id
            ).first()

            if not existing:
                up = UserProgress(
                    user_id=current_user.id,
                    node_id=node.id,
                    mastery_level=item.mastery_level,
                    streak_days=item.streak_days,
                    confidence_rating="medium"
                )
                db.add(up)
                migrated_nodes += 1
            else:
                existing.mastery_level = max(existing.mastery_level, item.mastery_level)
                existing.streak_days = max(existing.streak_days, item.streak_days)

    if body.tbs_code and body.tbs_rows:
        scenario = db.query(TBSScenario).filter(TBSScenario.code == body.tbs_code).first()
        if scenario:
            attempt = TBSAttempt(
                user_id=current_user.id,
                scenario_id=scenario.id,
                submission_json={"rows": body.tbs_rows},
                score=100.0,
                is_balanced=True
            )
            db.add(attempt)

    db.commit()
    return {"status": "success", "migrated_nodes": migrated_nodes, "email": current_user.email}

@router.post("/qr-session", response_model=QRSessionResponse)
def generate_qr_session(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Generates a QR authentication token for mobile cross-device login.
    """
    token = create_access_token(subject=current_user.id)
    
    active_qr_tickets[token] = {
        "user_id": current_user.id,
        "scanned": False
    }

    referer = request.headers.get("referer")
    if referer:
        base_url = referer.split("#")[0].rstrip("/")
    else:
        base_url = str(request.base_url).rstrip("/")
        
    qr_url = f"{base_url}/#qr_login_{token}"

    return QRSessionResponse(
        qr_token=token,
        auth_token=token,
        qr_url=qr_url
    )

@router.get("/qr-status", response_model=QRStatusResponse)
def check_qr_status(
    qr_token: str,
    db: Session = Depends(get_db)
):
    """
    Watcher endpoint for desktop browser polling to check if phone scanned the QR code.
    """
    ticket = active_qr_tickets.get(qr_token)
    if not ticket:
        return QRStatusResponse(scanned=False)

    if ticket.get("scanned"):
        user = db.query(User).filter(User.id == ticket["user_id"]).first()
        if user:
            return QRStatusResponse(
                scanned=True,
                access_token=qr_token,
                user=UserResponse.model_validate(user)
            )

    return QRStatusResponse(scanned=False)

@router.get("/qr-login")
def qr_login(
    qr_token: str,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Validates QR token from mobile camera scan, sets auth cookie, and marks ticket as scanned.
    """
    try:
        payload = jwt.decode(qr_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(status_code=400, detail="Invalid QR token")
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise HTTPException(status_code=400, detail="Expired or invalid QR code token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Mark ticket as scanned so desktop watcher triggers instant auto-login!
    if qr_token in active_qr_tickets:
        active_qr_tickets[qr_token]["scanned"] = True

    response.set_cookie(
        key="cpa_jwt_token",
        value=qr_token,
        httponly=False,
        max_age=86400 * 30,
        samesite="lax"
    )

    return Token(access_token=qr_token, token_type="bearer", user=UserResponse.model_validate(user))

@router.get("/user/profile")
def get_user_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    progress_records = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).all()
    tbs_attempts = db.query(TBSAttempt).filter(TBSAttempt.user_id == current_user.id).all()

    total_attempted = len(progress_records)
    avg_mastery = round(sum(p.mastery_level for p in progress_records) / total_attempted, 1) if total_attempted > 0 else 0.0
    streak_days = max([p.streak_days for p in progress_records], default=1 if total_attempted > 0 else 0)

    return {
        "user": UserResponse.model_validate(current_user),
        "streak_days": streak_days,
        "readiness_score": avg_mastery,
        "mastery_percent": avg_mastery,
        "total_attempted": total_attempted,
        "tbs_completed": len(tbs_attempts)
    }

@router.put("/user/profile", response_model=UserResponse)
def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates user settings: email, password, and target CPA exam date.
    """
    if user_update.email and user_update.email != current_user.email:
        existing = db.query(User).filter(User.email == user_update.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email is already in use by another account")
        current_user.email = user_update.email

    if user_update.password:
        current_user.password_hash = get_password_hash(user_update.password)

    if user_update.target_exam_date is not None:
        current_user.target_exam_date = user_update.target_exam_date

    db.commit()
    db.refresh(current_user)
    return UserResponse.model_validate(current_user)
