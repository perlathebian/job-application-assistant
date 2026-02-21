import asyncio
import time
from backend.services.skill_extractor import SkillExtractor
from backend.services.semantic_matcher import SemanticMatcher
from backend.services.letter_generator import LetterGenerator


async def benchmark():
    """Benchmark key operations"""
    print("=" * 60)
    print("PERFORMANCE BENCHMARK")
    print("=" * 60)
    
    # Skill extraction
    print("\n1. Skill Extraction")
    extractor = SkillExtractor()
    text = "We need a Python developer with FastAPI, Docker, AWS, and PostgreSQL experience for building microservices."
    
    start = time.time()
    for _ in range(10):
        extractor.extract_skills(text)
    elapsed = time.time() - start
    print(f"   Average: {elapsed/10*1000:.2f}ms per extraction")
    
    # Semantic matching
    print("\n2. Semantic Matching")
    matcher = SemanticMatcher()
    job_desc = text
    resume = "Python developer with 4 years FastAPI and Docker experience"
    
    start = time.time()
    for _ in range(10):
        matcher.calculate_semantic_similarity(job_desc, resume)
    elapsed = time.time() - start
    print(f"   Average: {elapsed/10*1000:.2f}ms per match")
    
    # Full match report
    print("\n3. Complete Match Report")
    start = time.time()
    matcher.generate_match_report(
        job_desc,
        ["Python", "FastAPI", "Docker"],
        resume,
        ["Python", "FastAPI"]
    )
    elapsed = time.time() - start
    print(f"   Time: {elapsed*1000:.2f}ms")
    
    # Cover letter generation
    print("\n4. Cover Letter Generation (with LLM)")
    generator = LetterGenerator()
    
    start = time.time()
    result = await generator.generate(
        job_description=job_desc,
        resume_text=resume,
        company_name="TechCorp",
        applicant_name="John Doe",
        match_score=75.0,
        matched_skills=["Python", "FastAPI"]
    )
    elapsed = time.time() - start
    print(f"   Time: {elapsed:.2f}s")
    print(f"   Model: {result['model_used']}")
    
    print("\n" + "=" * 60)
    print("BENCHMARK COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(benchmark())