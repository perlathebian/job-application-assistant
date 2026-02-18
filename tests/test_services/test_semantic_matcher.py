import pytest
from backend.services.semantic_matcher import SemanticMatcher


@pytest.fixture
def matcher():
    """Provides a semantic matcher instance"""
    return SemanticMatcher()


def test_skill_overlap_full_match(matcher):
    """Test skill overlap with complete match"""
    job_skills = ["Python", "Docker"]
    resume_skills = ["Python", "Docker"]
    
    result = matcher.calculate_skill_overlap(job_skills, resume_skills)
    
    assert result["overlap_score"] == 100.0
    assert len(result["matched_skills"]) == 2
    assert len(result["missing_skills"]) == 0


def test_skill_overlap_partial_match(matcher):
    """Test skill overlap with partial match"""
    job_skills = ["Python", "Docker", "AWS"]
    resume_skills = ["Python", "Git"]
    
    result = matcher.calculate_skill_overlap(job_skills, resume_skills)
    
    assert "python" in result["matched_skills"]
    assert "docker" in result["missing_skills"]
    assert "aws" in result["missing_skills"]
    assert result["overlap_score"] > 0


def test_skill_overlap_no_match(matcher):
    """Test skill overlap with no matching skills"""
    job_skills = ["Rust", "Go"]
    resume_skills = ["Python", "JavaScript"]
    
    result = matcher.calculate_skill_overlap(job_skills, resume_skills)
    
    assert result["overlap_score"] == 0.0
    assert len(result["matched_skills"]) == 0


def test_semantic_similarity_same_text(matcher):
    """Test that identical texts have high similarity"""
    text = "Python machine learning engineer with deep learning experience"
    
    score = matcher.calculate_semantic_similarity(text, text)
    
    assert score > 90.0


def test_semantic_similarity_similar_text(matcher):
    """Test similar texts have decent similarity"""
    job = "Looking for Python developer with machine learning experience"
    resume = "Experienced Python programmer skilled in ML and data science"
    
    score = matcher.calculate_semantic_similarity(job, resume)
    
    assert score > 50.0


def test_generate_match_report_structure(matcher):
    """Test that match report has all required fields"""
    job_desc = "Senior Python developer needed with FastAPI and Docker experience. 5+ years required."
    job_skills = ["Python", "FastAPI", "Docker"]
    resume_text = "Python developer with 4 years experience in web development and containerization."
    resume_skills = ["Python", "Flask", "Docker"]
    
    report = matcher.generate_match_report(
        job_desc, job_skills, resume_text, resume_skills
    )
    
    assert "overall_match_score" in report
    assert "skill_match_score" in report
    assert "semantic_match_score" in report
    assert "matched_skills" in report
    assert "missing_skills" in report
    assert "recommendation" in report
    assert 0 <= report["overall_match_score"] <= 100