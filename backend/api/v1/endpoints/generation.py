from fastapi import APIRouter, HTTPException
from backend.models.schemas import CoverLetterInput, CoverLetterOutput
from backend.services.letter_generator import LetterGenerator

router = APIRouter()

# Initialize letter generator (singleton)
letter_generator = LetterGenerator()


@router.post("/generate-letter", response_model=CoverLetterOutput)
async def generate_cover_letter(letter_data: CoverLetterInput):
    """
    Generate a tailored cover letter using AI
    
    Uses Groq LLM (Llama 3.1) to generate personalized letters.
    Falls back to template if LLM is unavailable.
    
    Returns:
    - Generated cover letter text
    - Model used (LLM name or 'template_fallback')
    """
    try:
        result = await letter_generator.generate(
            job_description=letter_data.job_description,
            resume_text=letter_data.resume_text,
            company_name=letter_data.company_name,
            applicant_name=letter_data.applicant_name,
            match_score=letter_data.match_score,
            matched_skills=letter_data.matched_skills
        )
        
        return CoverLetterOutput(
            cover_letter=result["cover_letter"],
            model_used=result["model_used"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Letter generation failed: {str(e)}")