# Main application entry point - updated for AUD case studies
import os
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.core.config import settings
from backend.app.api.v1.api import api_router
from backend.app.db.session import engine
from backend.app.db.base import Base
from backend.app.db.init_db import init_db, SessionLocal

# Create tables
Base.metadata.create_all(bind=engine)

# Auto seed database on startup
db = SessionLocal()
init_db(db)
db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json"
)

# Set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com https://fonts.gstatic.com data: blob:;"
    return response

# Mount API Router on both /api/v1 and /cpa/api/v1 for reverse proxy subpath support
app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router, prefix="/cpa/api/v1")

# Mount static files on both /static and /cpa/static
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    app.mount("/cpa/static", StaticFiles(directory=static_dir), name="cpa_static")

@app.get("/favicon.ico")
@app.get("/cpa/favicon.ico")
def get_favicon():
    # Return 204 No Content for favicon to prevent 404 console errors
    return Response(status_code=204)

@app.get("/")
@app.get("/cpa")
@app.get("/cpa/")
def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "CPA Exam Adaptive Learning Platform API Active. Access /docs for API documentation."}
