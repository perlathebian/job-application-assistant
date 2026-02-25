from fastapi import APIRouter
from backend.api.v1.endpoints import jobs, resumes, matching, generation, applications

api_router = APIRouter()

# Include job endpoints
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])

# Include resume endpoints
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])

api_router.include_router(matching.router, prefix="/matching", tags=["matching"])
api_router.include_router(generation.router, prefix="/generation", tags=["generation"])

api_router.include_router(applications.router, prefix="/applications", tags=["applications"]) 