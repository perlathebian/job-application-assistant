from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.models.schemas import ResumeParseOutput
from backend.services.resume_parser import ResumeParser

router = APIRouter()

# Initialize resume parser (singleton)
resume_parser = ResumeParser()


@router.post("/parse-resume", response_model=ResumeParseOutput)
async def parse_resume(file: UploadFile = File(...)):
    """
    Parse resume from PDF or DOCX file
    
    Accepts:
    - PDF files (.pdf)
    - Word documents (.docx, .doc)
    
    Returns:
    - Extracted text
    - List of skills
    - Contact information (email, phone)
    - Years of experience (if found)
    - File type
    """
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    file_extension = file.filename.lower().split('.')[-1]
    if file_extension not in ['pdf', 'docx', 'doc']:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {file_extension}. Only PDF and DOCX are supported."
        )
    
    try:
        # Read file bytes
        contents = await file.read()
        
        # Parse the resume
        result = await resume_parser.parse(contents, file.filename)
        
        return ResumeParseOutput(
            text=result["text"],
            skills=result["skills"],
            contact=result["contact"],
            years_experience=result["years_experience"],
            file_type=result["file_type"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume parsing failed: {str(e)}")