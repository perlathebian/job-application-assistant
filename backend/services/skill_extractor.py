import spacy
import json
from pathlib import Path
from typing import List, Dict
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class SkillExtractor:
    """Extract skills and metadata from job descriptions"""
    
    def __init__(self):
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")
    
        # Load skills database
        skills_file = Path(__file__).parent.parent.parent / "data" / "skills_database.json"
        with open(skills_file, 'r') as f:
            data = json.load(f)
        
            # Flatten all categories into single skills list
            self.skills = []
            if isinstance(data, dict):
                for category, skill_list in data.items():
                    if isinstance(skill_list, list):
                        self.skills.extend(skill_list)
            elif isinstance(data, list):
                self.skills = data
        
            logger.info(f"Loaded {len(self.skills)} skills from database")
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from job description"""
        logger.info(f"Extracting skills from text of length {len(text)}")
        
        try:
            # Process text with spaCy
            doc = self.nlp(text.lower())
            
            # Find skills in text
            found_skills = set()
            
            for skill in self.skills:
                skill_lower = skill.lower()
                if skill_lower in text.lower():
                    found_skills.add(skill)
            
            # Also check for multi-word skills
            for token in doc:
                token_text = token.text.lower()
                if token_text in [s.lower() for s in self.skills]:
                    # Find original casing
                    for skill in self.skills:
                        if skill.lower() == token_text:
                            found_skills.add(skill)
                            break
            
            result = sorted(list(found_skills))
            logger.info(f"Found {len(result)} skills: {result[:5]}...")
            return result
        
        except Exception as e:
            logger.error(f"Error extracting skills: {str(e)}", exc_info=True)
            return []
    
    def extract_experience_level(self, text: str) -> str:
        """Extract experience level from job description"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["senior", "lead", "principal", "staff"]):
            return "Senior"
        elif any(word in text_lower for word in ["junior", "entry", "graduate", "intern"]):
            return "Junior"
        elif any(word in text_lower for word in ["mid", "intermediate"]):
            return "Mid-level"
        
        # Check for years
        if "5+ years" in text_lower or "5 years" in text_lower:
            return "Senior"
        elif "2-3 years" in text_lower or "2 years" in text_lower:
            return "Mid-level"
        elif "0-1 years" in text_lower:
            return "Junior"
        
        return "Not specified"
    
    def extract_job_title(self, text: str) -> str | None:
        """Extract likely job title from description"""
        doc = self.nlp(text)
        
        # Common job title keywords
        title_keywords = [
            "engineer", "developer", "scientist", "analyst", "manager",
            "architect", "consultant", "specialist", "lead", "director"
        ]
        
        # Look for job titles in first few sentences
        for sent in list(doc.sents)[:3]:
            sent_text = sent.text.lower()
            for keyword in title_keywords:
                if keyword in sent_text:
                    # Extract phrase around keyword
                    words = sent.text.split()
                    for i, word in enumerate(words):
                        if keyword in word.lower():
                            # Get 2 words before and 1 after
                            start = max(0, i-2)
                            end = min(len(words), i+2)
                            title = " ".join(words[start:end])
                            return title.strip()
        
        return None
    
    def extract_all(self, text: str) -> Dict:
        """Extract all information from job description"""
        return {
            "skills": self.extract_skills(text),
            "experience_level": self.extract_experience_level(text),
            "job_title": self.extract_job_title(text)
        }