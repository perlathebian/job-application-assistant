from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class JobMatch(Base):
    """Database model for storing job match results"""
    __tablename__ = "job_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    job_title = Column(String, nullable=True)
    job_description = Column(Text, nullable=False)
    resume_filename = Column(String, nullable=False)
    
    # Match scores
    overall_score = Column(Float, nullable=False)
    skill_score = Column(Float, nullable=False)
    semantic_score = Column(Float, nullable=False)
    
    # Skills
    matched_skills = Column(Text, nullable=False)  # JSON string
    missing_skills = Column(Text, nullable=False)  # JSON string
    
    # Generated letter
    cover_letter = Column(Text, nullable=True)
    model_used = Column(String, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<JobMatch(company={self.company_name}, score={self.overall_score})>"