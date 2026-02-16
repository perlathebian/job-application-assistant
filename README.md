# job-application-assistant

AI-powered job application assistant with skill matching and cover letter generation.

## Development Progress

### Day 1 (Completed)

- Project structure initialized
- FastAPI application with health endpoint
- Pydantic schemas for data validation
- CORS middleware configured
- Testing infrastructure with pytest
- API documentation at `/api/docs`

**Running the API:**

```bash
uvicorn backend.main:app --reload
```

**Access:**

- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/api/docs

### Day 2 (Completed)

- Skills database with 100+ tech skills
- Skill extraction service with NLP
- POST `/api/v1/jobs/extract-skills` endpoint
- Experience level detection
- Job title extraction
- Test suite with 7 passing tests

**Test endpoint:**

```bash
# Start API
uvicorn backend.main:app --reload

# Run tests
pytest tests/test_services/ -v
```
