from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from backend.models.database import Base, JobMatch
from backend.config import settings
import json
from typing import List, Optional


class DatabaseService:
    """Service for database operations"""
    
    def __init__(self):
        # Create async engine
        self.engine = create_async_engine(
            settings.DATABASE_URL,
            echo=False
        )
        
        # Create session factory
        self.async_session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    async def init_db(self):
        """Initialize database tables"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def save_match(
        self,
        company_name: str,
        job_title: Optional[str],
        job_description: str,
        resume_filename: str,
        overall_score: float,
        skill_score: float,
        semantic_score: float,
        matched_skills: List[str],
        missing_skills: List[str],
        cover_letter: Optional[str] = None,
        model_used: Optional[str] = None
    ) -> int:
        """Save a job match to database"""
        async with self.async_session() as session:
            job_match = JobMatch(
                company_name=company_name,
                job_title=job_title,
                job_description=job_description,
                resume_filename=resume_filename,
                overall_score=overall_score,
                skill_score=skill_score,
                semantic_score=semantic_score,
                matched_skills=json.dumps(matched_skills),
                missing_skills=json.dumps(missing_skills),
                cover_letter=cover_letter,
                model_used=model_used
            )
            
            session.add(job_match)
            await session.commit()
            await session.refresh(job_match)
            
            return job_match.id
    
    async def get_all_matches(self) -> List[JobMatch]:
        """Get all job matches ordered by date"""
        async with self.async_session() as session:
            result = await session.execute(
                select(JobMatch).order_by(JobMatch.created_at.desc())
            )
            return result.scalars().all()
    
    async def get_match_by_id(self, match_id: int) -> Optional[JobMatch]:
        """Get a specific job match by ID"""
        async with self.async_session() as session:
            result = await session.execute(
                select(JobMatch).where(JobMatch.id == match_id)
            )
            return result.scalar_one_or_none()
    
    async def delete_match(self, match_id: int) -> bool:
        """Delete a job match"""
        async with self.async_session() as session:
            result = await session.execute(
                select(JobMatch).where(JobMatch.id == match_id)
            )
            match = result.scalar_one_or_none()
            
            if match:
                await session.delete(match)
                await session.commit()
                return True
            return False


# Singleton instance
db_service = DatabaseService()