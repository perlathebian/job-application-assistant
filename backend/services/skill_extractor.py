import spacy
import json
from pathlib import Path
from typing import Dict, List


class SkillExtractor:
    """Extract skills from job descriptions using NLP"""
    
    def __init__(self):
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Load skills database
        self.skills_list = self._load_skills()
    
    def _load_skills(self) -> List[str]:
        """Load skills from JSON database"""
        skills_file = Path(__file__).parent.parent.parent / "data" / "skills_database.json"
        
        with open(skills_file, 'r') as f:
            skills_db = json.load(f)
        
        # Flatten all categories into single list
        all_skills = []
        for category_skills in skills_db.values():
            all_skills.extend(category_skills)
        
        # Convert to lowercase for matching
        return [skill.lower() for skill in all_skills]
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using pattern matching"""
        text_lower = text.lower()
        found_skills = set()
        
        # Simple keyword matching
        for skill in self.skills_list:
            if skill in text_lower:
                found_skills.add(skill)
        
        # Return capitalized skills
        return sorted([skill.title() for skill in found_skills])
    
    def extract_experience_level(self, text: str) -> str:
        """Extract experience level from job description"""
        text_lower = text.lower()
        
        # Check for senior level
        senior_keywords = ['senior', 'sr.', 'lead', 'principal', 'staff', 'architect']
        if any(keyword in text_lower for keyword in senior_keywords):
            return "Senior"
        
        # Check for junior/entry level
        junior_keywords = ['junior', 'jr.', 'entry', 'entry-level', 'graduate', 'intern']
        if any(keyword in text_lower for keyword in junior_keywords):
            return "Junior"
        
        # Default to mid-level
        return "Mid-level"
    
    def extract_job_title(self, text: str) -> str | None:
        """Extract job title using spaCy NER"""
        doc = self.nlp(text[:500])  # Process first 500 chars
        
        # Common job title patterns
        job_titles = [
            "Machine Learning Engineer",
            "Data Scientist",
            "Software Engineer",
            "Backend Developer",
            "Frontend Developer",
            "Full Stack Developer",
            "DevOps Engineer",
            "Data Engineer",
            "ML Engineer",
            "AI Engineer",
            "Python Developer"
        ]
        
        # Check if any title appears in text
        for title in job_titles:
            if title.lower() in text.lower():
                return title
        
        return None
    
    def extract_all(self, text: str) -> Dict[str, any]:
        """Extract all information from job description"""
        return {
            "skills": self.extract_skills(text),
            "experience_level": self.extract_experience_level(text),
            "job_title": self.extract_job_title(text)
        }