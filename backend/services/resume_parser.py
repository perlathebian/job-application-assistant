import pdfplumber
import re
from docx import Document
from typing import Dict, List
from io import BytesIO
from backend.services.skill_extractor import SkillExtractor


class ResumeParser:
    """Parse resumes from PDF and DOCX formats"""
    
    def __init__(self):
        # Initialize skill extractor
        self.skill_extractor = SkillExtractor()
    
    async def parse_pdf(self, file_bytes: bytes) -> str:
        """Extract text from PDF file"""
        text = ""
        
        # pdfplumber requires file-like object
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        return text
    
    async def parse_docx(self, file_bytes: bytes) -> str:
        """Extract text from DOCX file"""
        doc = Document(BytesIO(file_bytes))
        
        # Extract text from all paragraphs
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        return text
    
    def extract_contact(self, text: str) -> Dict[str, str | None]:
        """Extract contact information using regex"""
        contact = {
            "email": None,
            "phone": None
        }
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact["email"] = email_match.group(0)
        
        # Phone pattern (various formats)
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # 123-456-7890 or 1234567890
            r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',     # (123) 456-7890
            r'\+\d{1,3}\s?\d{3}[-.]?\d{3}[-.]?\d{4}'  # +1 123-456-7890
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact["phone"] = phone_match.group(0)
                break
        
        return contact
    
    def extract_years_experience(self, text: str) -> int | None:
        """Extract years of experience from text"""
        # Patterns for experience
        patterns = [
            r'(\d+)\+?\s*years?\s*of\s*experience',
            r'(\d+)\+?\s*years?\s*experience',
            r'experience:\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s*experience'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    async def parse(self, file_bytes: bytes, filename: str) -> Dict:
        """Main parsing function that handles both PDF and DOCX"""
        # Determine file type
        file_extension = filename.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            text = await self.parse_pdf(file_bytes)
        elif file_extension in ['docx', 'doc']:
            text = await self.parse_docx(file_bytes)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Extract skills
        skills = self.skill_extractor.extract_skills(text)
        
        # Extract contact information
        contact = self.extract_contact(text)
        
        # Extract years of experience
        years_exp = self.extract_years_experience(text)
        
        return {
            "text": text,
            "skills": skills,
            "contact": contact,
            "years_experience": years_exp,
            "file_type": file_extension
        }