import pytest
from fastapi.testclient import TestClient
from backend.main import app
import io

client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_extract_skills_valid():
    """Test skill extraction with valid input"""
    response = client.post(
        "/api/v1/jobs/extract-skills",
        json={
            "text": "We are looking for a Python developer with experience in FastAPI, Docker, and AWS. The ideal candidate will have 5+ years of experience.",
            "company": "TechCorp"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "skills" in data
    assert "Python" in data["skills"] or "python" in [s.lower() for s in data["skills"]]


def test_extract_skills_short_text():
    """Test skill extraction fails with too short text"""
    response = client.post(
        "/api/v1/jobs/extract-skills",
        json={
            "text": "Short text",
            "company": "TechCorp"
        }
    )
    
    assert response.status_code == 422


def test_parse_resume_no_file():
    """Test resume parsing without file"""
    response = client.post("/api/v1/resumes/parse-resume")
    
    assert response.status_code == 422


def test_matching_valid():
    """Test matching endpoint with valid data"""
    response = client.post(
        "/api/v1/matching/match",
        json={
            "job_description": "Looking for Python developer with ML experience to build data pipelines",
            "job_skills": ["Python", "ML", "Docker"],
            "resume_text": "Python developer with 3 years experience in machine learning and data engineering",
            "resume_skills": ["Python", "ML", "SQL"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "overall_match_score" in data
    assert "matched_skills" in data
    assert 0 <= data["overall_match_score"] <= 100


def test_generate_letter_valid():
    """Test cover letter generation with valid data"""
    response = client.post(
        "/api/v1/generation/generate-letter",
        json={
            "job_description": "We are looking for a Python developer with ML experience to join our team",
            "resume_text": "Python developer with 3 years of machine learning experience",
            "company_name": "TechCorp",
            "applicant_name": "John Doe",
            "match_score": 75.0,
            "matched_skills": ["Python", "ML"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "cover_letter" in data
    assert "model_used" in data
    assert len(data["cover_letter"]) > 100


def test_generate_letter_short_input():
    """Test cover letter generation fails with short input"""
    response = client.post(
        "/api/v1/generation/generate-letter",
        json={
            "job_description": "Short",
            "resume_text": "Short",
            "company_name": "TechCorp",
            "applicant_name": "John Doe"
        }
    )
    
    assert response.status_code == 422