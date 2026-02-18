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

### Day 3 (Completed)

- Resume parser for PDF and DOCX files
- Contact information extraction (email, phone)
- Years of experience detection
- POST `/api/v1/resumes/parse-resume` endpoint
- File upload handling with validation
- Test suite with 8 passing tests (15 total)

**Test resume parsing:**

```bash
# Start API
uvicorn backend.main:app --reload

# Visit http://localhost:8000/api/docs
# Use POST /api/v1/resumes/parse-resume
# Upload PDF or DOCX file

# Run tests
pytest tests/test_services/ -v
```

### Day 4 (Completed)

- Semantic matching with sentence-transformers
- POST `/api/v1/matching/match` endpoint
- LLM cover letter generation (Groq API - FREE)
- POST `/api/v1/generation/generate-letter` endpoint
- Embedding cache for performance
- Template fallback if LLM unavailable
- Test suite: 22 tests passing

**Model:** Llama 3.3 70B Versatile via Groq (free, fast, high-quality)
