import pytest
from backend.services.skill_extractor import SkillExtractor


@pytest.fixture
def extractor():
    """Provides a skill extractor instance"""
    return SkillExtractor()


def test_extract_skills_python(extractor):
    """Test extraction of Python skill"""
    text = "Looking for Python developer with 5 years experience"
    skills = extractor.extract_skills(text)
    
    assert "Python" in skills
    assert isinstance(skills, list)


def test_extract_skills_multiple(extractor):
    """Test extraction of multiple skills"""
    text = """
    We need a developer with Python, FastAPI, Docker, and PostgreSQL experience.
    Knowledge of AWS and Kubernetes is a plus.
    """
    skills = extractor.extract_skills(text)
    
    assert "Python" in skills
    assert "Fastapi" in skills or "FastAPI" in skills
    assert "Docker" in skills
    assert "Postgresql" in skills or "PostgreSQL" in skills
    assert len(skills) >= 4


def test_extract_experience_senior(extractor):
    """Test senior level detection"""
    text = "Looking for Senior Machine Learning Engineer"
    level = extractor.extract_experience_level(text)
    
    assert level == "Senior"


def test_extract_experience_junior(extractor):
    """Test junior level detection"""
    text = "Entry-level position for Junior Developer"
    level = extractor.extract_experience_level(text)
    
    assert level == "Junior"


def test_extract_experience_mid(extractor):
    """Test mid-level with explicit mention"""
    text = "Looking for mid-level Machine Learning Engineer with 3 years experience"
    level = extractor.extract_experience_level(text)
    
    assert level == "Mid-level"


def test_extract_job_title(extractor):
    """Test job title extraction"""
    text = "We are hiring a Machine Learning Engineer to join our team"
    title = extractor.extract_job_title(text)
    
    # Job title extraction includes context words: verify it contains the key terms
    assert "Machine Learning Engineer" in title

def test_extract_all(extractor):
    """Test complete extraction"""
    text = """
    Senior Machine Learning Engineer position
    
    Required skills:
    - Python programming
    - PyTorch and TensorFlow
    - Docker and Kubernetes
    
    5+ years of experience required.
    """
    
    result = extractor.extract_all(text)
    
    assert "skills" in result
    assert "experience_level" in result
    assert "job_title" in result
    assert result["experience_level"] == "Senior"
    assert len(result["skills"]) > 0