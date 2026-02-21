COVER_LETTER_PROMPT = """You are a professional cover letter writer. Write a concise, compelling cover letter.

Applicant Name: {applicant_name}
Company: {company_name}
Match Score: {match_score}%
Key Matching Skills: {key_skills}

Job Description (excerpt):
{job_description}

Applicant Background (excerpt):
{resume_highlights}

Write a professional 3-paragraph cover letter that:
1. Opens with genuine interest in the specific role and company
2. Highlights 2-3 relevant skills that match the job requirements
3. Closes with enthusiasm and a call to action

Requirements:
- Keep it under 250 words
- Be specific, not generic
- Sound human, not robotic
- Do not include subject line or date

Cover Letter:"""