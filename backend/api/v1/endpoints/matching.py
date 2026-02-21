from fastapi import APIRouter, HTTPException
from backend.models.schemas import MatchInput, MatchOutput
from backend.services.semantic_matcher import SemanticMatcher

router = APIRouter()

# Initialize semantic matcher (singleton)
semantic_matcher = SemanticMatcher()


@router.post("/match", response_model=MatchOutput)
async def match_resume(match_data: MatchInput):
    """
    Calculate match score between job description and resume
    
    Returns:
    - Overall match score (weighted: 60% skills, 40% semantic)
    - Skill match score
    - Semantic similarity score
    - Matched and missing skills
    - Recommendation
    """
    try:
        report = semantic_matcher.generate_match_report(
            job_description=match_data.job_description,
            job_skills=match_data.job_skills,
            resume_text=match_data.resume_text,
            resume_skills=match_data.resume_skills
        )
        
        return MatchOutput(
            overall_match_score=report["overall_match_score"],
            skill_match_score=report["skill_match_score"],
            semantic_match_score=report["semantic_match_score"],
            matched_skills=report["matched_skills"],
            missing_skills=report["missing_skills"],
            extra_skills=report["extra_skills"],
            recommendation=report["recommendation"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")