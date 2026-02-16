from fastapi import APIRouter
from backend.api.v1.endpoints import jobs

api_router = APIRouter()

# Include job endpoints
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])