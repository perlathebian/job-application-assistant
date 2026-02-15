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
