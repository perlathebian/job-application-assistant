import pytest
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture
def client():
    """Provides a test client for API testing"""
    return TestClient(app)


@pytest.fixture
def sample_job_description():
    """Provides sample job description for testing"""
    return """
    We are looking for a Senior Machine Learning Engineer with 5+ years of experience.
    
    Required skills:
    - Python programming
    - PyTorch and TensorFlow
    - Docker and Kubernetes
    - AWS cloud services
    - RESTful API development
    
    You will work on building recommendation systems and NLP models.
    """