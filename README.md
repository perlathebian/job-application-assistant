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

### Day 5 (Completed)

**Streamlit Frontend with Database Persistence**

**Features:**

- Multi-page Streamlit application (5 pages)
- Job description input with skill extraction
- Resume upload and parsing (PDF/DOCX)
- Interactive match visualization with Plotly gauge charts
- AI cover letter generation with Groq LLM
- Application history with SQLite database
- Professional UI with custom CSS
- Full workflow: job -> resume -> match -> letter -> save

**Running the Application:**

```bash
# Terminal 1: Start Backend API
uvicorn backend.main:app --reload

# Terminal 2: Start Frontend (separate terminal)
streamlit run frontend/app.py
```

**Access:**

- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

**First-time setup:**

```bash
python init_db.py  # Initialize database
```

**Project Structure:**

```
frontend/
├── app.py              # Main Streamlit app
├── utils.py            # API client utilities
└── pages/
    ├── job_input.py    # Job description input
    ├── resume_upload.py # Resume upload
    ├── match_display.py # Match visualization
    ├── letter_display.py # Letter generation
    └── history.py       # Application history
```

**Tech Stack:**

- Frontend: Streamlit 1.31.0
- Charts: Plotly 5.18.0
- HTTP Client: httpx 0.26.0
- Database: SQLAlchemy + aiosqlite
- LLM: Groq API (Llama 3.3 70B)
