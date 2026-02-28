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


def test_false_positive_go_not_extracted(extractor):
    text = "We are looking to go beyond traditional approaches and grow the team."
    skills = extractor.extract_skills(text)
    assert "Go" not in skills


def test_false_positive_r_not_extracted(extractor):
    text = "We are looking for a developer or analyst to join our team."
    skills = extractor.extract_skills(text)
    assert "R" not in skills


def test_go_extracted_when_standalone(extractor):
    text = "Required skills: Go, Python, Docker"
    skills = extractor.extract_skills(text)
    assert "Go" in skills


def test_r_extracted_when_standalone(extractor):
    text = "Must know Python, R, and SQL for this data analyst role."
    skills = extractor.extract_skills(text)
    assert "R" in skills

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
    assert "detected_domain" in result
    assert result["experience_level"] == "Senior"
    assert len(result["skills"]) > 0