from pydantic import BaseModel, Field
from typing import List


class JobDescriptionInput(BaseModel):
    """Input schema for job description"""
    text: str = Field(..., min_length=50, description="Job description text")
    company: str | None = None


class SkillsOutput(BaseModel):
    """Output schema for extracted skills"""
    skills: List[str]
    experience_level: str | None = None
    job_title: str | None = None

class ResumeParseOutput(BaseModel):
    """Output schema for parsed resume"""
    text: str
    skills: List[str]
    contact: dict
    years_experience: int | None = None
    file_type: str    


class MatchInput(BaseModel):
    """Input schema for matching endpoint"""
    job_description: str = Field(..., min_length=50)
    job_skills: List[str]
    resume_text: str = Field(..., min_length=50)
    resume_skills: List[str]


class MatchOutput(BaseModel):
    """Output schema for match results"""
    overall_match_score: float
    skill_match_score: float
    semantic_match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    extra_skills: List[str]
    recommendation: str


class CoverLetterInput(BaseModel):
    """Input schema for cover letter generation"""
    job_description: str = Field(..., min_length=50)
    resume_text: str = Field(..., min_length=50)
    company_name: str = "the company"
    applicant_name: str = "Applicant"
    match_score: float = 0.0
    matched_skills: List[str] = []


class CoverLetterOutput(BaseModel):
    """Output schema for generated cover letter"""
    cover_letter: str
    model_used: str