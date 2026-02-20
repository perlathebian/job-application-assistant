from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.v1.router import api_router

from fastapi.exceptions import RequestValidationError
from backend.middleware.error_handler import (
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(
    title="Job Application Assistant API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# CORS middleware for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 routes
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Starting Job Application Assistant API")
    logger.info("Initializing database...")
    from backend.services.database_service import db_service
    await db_service.init_db()
    logger.info("Database initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Job Application Assistant API")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}