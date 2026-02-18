from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List
from backend.utils.cache import EmbeddingCache


class SemanticMatcher:
    """Calculate semantic similarity between job descriptions and resumes"""
    
    def __init__(self):
        # Load sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize embedding cache
        self.cache = EmbeddingCache(max_size=500)
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """Get text embedding with caching"""
        # Check cache first
        cached = self.cache.get(text)
        if cached is not None:
            return cached
        
        # Compute embedding
        embedding = self.model.encode(text)
        
        # Store in cache
        self.cache.set(text, embedding)
        
        return embedding
    
    def calculate_skill_overlap(
        self,
        job_skills: List[str],
        resume_skills: List[str]
    ) -> Dict:
        """Calculate skill overlap between job and resume"""
        # Lowercase for fair comparison
        job_set = set(skill.lower() for skill in job_skills)
        resume_set = set(skill.lower() for skill in resume_skills)
        
        # Find intersections and differences
        matched = job_set.intersection(resume_set)
        missing = job_set - resume_set
        extra = resume_set - job_set
        
        # Calculate overlap percentage
        overlap_score = (len(matched) / len(job_set) * 100) if job_set else 0.0
        
        return {
            "matched_skills": sorted(list(matched)),
            "missing_skills": sorted(list(missing)),
            "extra_skills": sorted(list(extra)),
            "overlap_score": round(overlap_score, 2)
        }
    
    def calculate_semantic_similarity(
        self,
        job_description: str,
        resume_text: str
    ) -> float:
        """Calculate semantic similarity using sentence embeddings"""
        # Get embeddings (from cache if available)
        job_embedding = self._get_embedding(job_description)
        resume_embedding = self._get_embedding(resume_text)
        
        # Cosine similarity returns value between -1 and 1
        similarity = cosine_similarity(
            [job_embedding],
            [resume_embedding]
        )[0][0]
        
        # Convert to 0-100 percentage
        return round(float(similarity) * 100, 2)
    
    def generate_recommendation(self, score: float) -> str:
        """Generate recommendation based on match score"""
        if score >= 80:
            return "Excellent match - strongly recommended to apply"
        elif score >= 65:
            return "Good match - worth applying"
        elif score >= 50:
            return "Moderate match - consider improving missing skills"
        else:
            return "Weak match - significant skill gaps exist"
    
    def generate_match_report(
        self,
        job_description: str,
        job_skills: List[str],
        resume_text: str,
        resume_skills: List[str]
    ) -> Dict:
        """Generate complete match report"""
        # Calculate skill overlap
        skill_analysis = self.calculate_skill_overlap(job_skills, resume_skills)
        
        # Calculate semantic similarity
        semantic_score = self.calculate_semantic_similarity(
            job_description,
            resume_text
        )
        
        # Combined weighted score
        # Skills matter more (60%) than semantic similarity (40%)
        skill_score = skill_analysis["overlap_score"]
        combined_score = round((skill_score * 0.6) + (semantic_score * 0.4), 2)
        
        return {
            "overall_match_score": combined_score,
            "skill_match_score": skill_score,
            "semantic_match_score": semantic_score,
            "matched_skills": skill_analysis["matched_skills"],
            "missing_skills": skill_analysis["missing_skills"],
            "extra_skills": skill_analysis["extra_skills"],
            "recommendation": self.generate_recommendation(combined_score)
        }