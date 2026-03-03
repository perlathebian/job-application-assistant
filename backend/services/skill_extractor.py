import spacy
import json
from pathlib import Path
from typing import List, Dict
import re
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

            # store domain map for detect_domain
            self.skills_by_domain = data if isinstance(data, dict) else {}    
        
            logger.info(f"Loaded {len(self.skills)} skills from database")
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from job description using word-boundary matching."""
        logger.info(f"Extracting skills from text of length {len(text)}")

        # Short skills that are valid (require exact case + word boundary)
        # Without this: "R" matches "or", "for"; "Go" matches "going", "cargo"
        SHORT_SKILLS_WHITELIST = {"R", "Go", "C", "C#", "C++", "ML", "AI", "UI", "UX", "AWS", "GCP"}

        try:
            found_skills = set()

            for skill in self.skills:
                if len(skill) <= 2:
                    if skill in SHORT_SKILLS_WHITELIST:
                        # Exact case-sensitive match with word boundary
                        pattern = r'(?<![a-zA-Z])' + re.escape(skill) + r'(?![a-zA-Z])'
                        if re.search(pattern, text):
                            found_skills.add(skill)
                    # Any short skill not in whitelist is skipped entirely
                    continue

                # Normal skills: word boundary, case-insensitive
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text, re.IGNORECASE):
                    found_skills.add(skill)

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

    
    def detect_domain(self, matched_skills: List[str]) -> str:
        """Detect the most likely job domain based on matched skills."""
        if not self.skills_by_domain or not matched_skills:
            return "general"

        domain_scores = {}
        for domain, skills in self.skills_by_domain.items():
            skills_lower = {s.lower() for s in skills}
            matched = [s for s in matched_skills if s.lower() in skills_lower]
            domain_scores[domain] = len(matched)

        if all(v == 0 for v in domain_scores.values()):
            return "general"

        best_domain = max(domain_scores, key=domain_scores.get)
        logger.info(f"Detected domain: {best_domain} (score: {domain_scores[best_domain]})")
        return best_domain

    
    def extract_all(self, text: str) -> Dict:
        """Extract all information from job description"""
        skills = self.extract_skills(text)
        return {
            "skills": skills,
            "experience_level": self.extract_experience_level(text),
            "detected_domain": self.detect_domain(skills)  
        }