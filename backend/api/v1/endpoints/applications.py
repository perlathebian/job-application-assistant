from fastapi import APIRouter, HTTPException
from backend.models.schemas import ApplicationSaveInput, ApplicationSaveOutput, ApplicationListOutput
from backend.services.database_service import db_service
from backend.utils.logger import setup_logger
import json

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/save", response_model=ApplicationSaveOutput)
async def save_application(data: ApplicationSaveInput):
    """Save a job application to history"""
    try:
        app_id = await db_service.save_match(
            company_name=data.company_name,
            job_title=data.job_title,
            job_description=data.job_description,
            resume_filename=data.resume_filename,
            overall_score=data.overall_score,
            skill_score=data.skill_score,
            semantic_score=data.semantic_score,
            matched_skills=data.matched_skills,
            missing_skills=data.missing_skills,
            cover_letter=data.cover_letter,
            model_used=data.model_used
        )
        return ApplicationSaveOutput(id=app_id)
    except Exception as e:
        logger.error(f"Error saving application: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to save application: {str(e)}")


@router.get("/all", response_model=list[ApplicationListOutput])
async def get_all_applications():
    """Get all saved job applications"""
    try:
        matches = await db_service.get_all_matches()
        return [
            ApplicationListOutput(
                id=m.id,
                company_name=m.company_name,
                job_title=m.job_title,
                overall_score=m.overall_score,
                skill_score=m.skill_score,
                semantic_score=m.semantic_score,
                matched_skills=json.loads(m.matched_skills),
                missing_skills=json.loads(m.missing_skills),
                cover_letter=m.cover_letter,
                resume_filename=m.resume_filename,
                model_used=m.model_used,
                created_at=str(m.created_at)
            )
            for m in matches
        ]
    except Exception as e:
        logger.error(f"Error fetching applications: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch applications: {str(e)}")


@router.delete("/{app_id}")
async def delete_application(app_id: int):
    """Delete a saved job application"""
    try:
        deleted = await db_service.delete_match(app_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Application not found")
        return {"deleted": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting application: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to delete application: {str(e)}")