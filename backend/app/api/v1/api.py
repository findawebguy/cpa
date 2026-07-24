import backend.app.db.base
from fastapi import APIRouter
from backend.app.api.v1.endpoints import auth, curriculum, simulations, flashcards, analytics, study, case_studies

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication & User"])
api_router.include_router(curriculum.router, tags=["Adaptive Curriculum"])
api_router.include_router(simulations.router, tags=["Task-Based Simulations"])
api_router.include_router(flashcards.router, tags=["Flashcards"])
api_router.include_router(analytics.router, tags=["Analytics & Diagnostics"])
api_router.include_router(study.router, prefix="/study", tags=["Study Guides & Modules"])
api_router.include_router(case_studies.router, prefix="/cases", tags=["Case Studies"])
