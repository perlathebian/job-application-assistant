from fastapi import APIRouter, HTTPException
from backend.models.schemas import JobDescriptionInput, SkillsOutput
from backend.services.skill_extractor import SkillExtractor

router = APIRouter()

# Initialize skill extractor (singleton)
skill_extractor = SkillExtractor()


@router.post("/extract-skills", response_model=SkillsOutput)
async def extract_skills(job: JobDescriptionInput):
    """
    Extract skills from job description
    
    Returns:
    - List of extracted skills
    - Experience level (Junior/Mid-level/Senior)
    - Job title (if detected)
    """
    try:
        result = skill_extractor.extract_all(job.text)
        
        return SkillsOutput(
            skills=result["skills"],
            experience_level=result["experience_level"],
            job_title=result["job_title"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skill extraction failed: {str(e)}")