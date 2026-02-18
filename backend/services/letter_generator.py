import requests
from backend.config import settings
from backend.utils.prompts import COVER_LETTER_PROMPT


class LetterGenerator:
    """Generate cover letters using Groq LLM"""
    
    def __init__(self):
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        self.model = settings.MODEL_NAME
    
    def _build_prompt(
        self,
        job_description: str,
        resume_text: str,
        company_name: str,
        applicant_name: str,
        match_score: float,
        matched_skills: list
    ) -> str:
        """Build the prompt for cover letter generation"""
        return COVER_LETTER_PROMPT.format(
            applicant_name=applicant_name,
            company_name=company_name,
            match_score=round(match_score, 1),
            key_skills=", ".join(matched_skills[:5]) if matched_skills else "relevant skills",
            job_description=job_description[:600],
            resume_highlights=resume_text[:400]
        )
    
    def _clean_output(self, text: str) -> str:
        """Clean LLM output"""
        text = text.strip()
        
        # Remove empty lines at start
        lines = text.split("\n")
        while lines and not lines[0].strip():
            lines.pop(0)
        
        return "\n".join(lines).strip()
    
    def _template_fallback(
        self,
        applicant_name: str,
        company_name: str,
        matched_skills: list
    ) -> str:
        """Template-based fallback if LLM fails"""
        skills_text = ", ".join(matched_skills[:3]) if matched_skills else "relevant technologies"
        
        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the position at {company_name}. With proven expertise in {skills_text}, I am confident in my ability to contribute meaningfully to your team.

Throughout my career, I have developed strong technical skills and a track record of delivering high-quality results. I am particularly drawn to {company_name} because of its commitment to innovation and excellence.

I would welcome the opportunity to discuss how my background aligns with your needs. Thank you for considering my application, and I look forward to speaking with you.

Best regards,
{applicant_name}"""
    
    async def generate(
        self,
        job_description: str,
        resume_text: str,
        company_name: str,
        applicant_name: str,
        match_score: float,
        matched_skills: list
    ) -> dict:
        """Generate tailored cover letter"""
        prompt = self._build_prompt(
            job_description=job_description,
            resume_text=resume_text,
            company_name=company_name,
            applicant_name=applicant_name,
            match_score=match_score,
            matched_skills=matched_skills
        )
        
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 400,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"API returned {response.status_code}: {response.text}")
            
            result = response.json()
            generated_text = result["choices"][0]["message"]["content"]
            letter = self._clean_output(generated_text)
            
            if len(letter) < 100:
                letter = self._template_fallback(applicant_name, company_name, matched_skills)
                return {"cover_letter": letter, "model_used": "template_fallback"}
            
            return {"cover_letter": letter, "model_used": self.model}
        
        except Exception as e:
            print(f"LLM failed: {e}")
            letter = self._template_fallback(applicant_name, company_name, matched_skills)
            return {"cover_letter": letter, "model_used": "template_fallback"}