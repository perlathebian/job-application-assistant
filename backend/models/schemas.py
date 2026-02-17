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