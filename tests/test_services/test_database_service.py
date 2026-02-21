import pytest
from backend.services.database_service import db_service


@pytest.mark.asyncio
async def test_init_db():
    """Test database initialization"""
    await db_service.init_db()
    # Should not raise any errors


@pytest.mark.asyncio
async def test_save_and_retrieve_match():
    """Test saving and retrieving a match"""
    # Save match
    match_id = await db_service.save_match(
        company_name="TestCorp",
        job_title="ML Engineer",
        job_description="Test job description",
        resume_filename="test_resume.pdf",
        overall_score=75.5,
        skill_score=70.0,
        semantic_score=80.0,
        matched_skills=["Python", "ML"],
        missing_skills=["AWS"],
        cover_letter="Test cover letter",
        model_used="test_model"
    )
    
    assert match_id > 0
    
    # Retrieve match
    match = await db_service.get_match_by_id(match_id)
    
    assert match is not None
    assert match.company_name == "TestCorp"
    assert match.overall_score == 75.5
    
    # Cleanup
    await db_service.delete_match(match_id)


@pytest.mark.asyncio
async def test_get_all_matches():
    """Test retrieving all matches"""
    matches = await db_service.get_all_matches()
    assert isinstance(matches, list)


@pytest.mark.asyncio
async def test_delete_match():
    """Test deleting a match"""
    # Create match
    match_id = await db_service.save_match(
        company_name="DeleteTest",
        job_title=None,
        job_description="Test",
        resume_filename="test.pdf",
        overall_score=50.0,
        skill_score=50.0,
        semantic_score=50.0,
        matched_skills=[],
        missing_skills=[]
    )
    
    # Delete
    result = await db_service.delete_match(match_id)
    assert result is True
    
    # Verify deleted
    match = await db_service.get_match_by_id(match_id)
    assert match is None