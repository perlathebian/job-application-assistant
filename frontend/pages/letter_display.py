import streamlit as st
import asyncio


def show():
    """Cover letter display page"""
    st.title("✉️ Cover Letter Generator")
    
    if not all([st.session_state.job_data, st.session_state.resume_data, st.session_state.match_data]):
        st.warning("⚠️ Please complete previous steps first")
        return
    
    job_data = st.session_state.job_data
    resume_data = st.session_state.resume_data
    match_data = st.session_state.match_data
    
    # Input fields
    col1, col2 = st.columns(2)
    
    with col1:
        applicant_name = st.text_input(
            "Your Name",
            placeholder="John Doe",
            help="Enter your full name"
        )
    
    with col2:
        company_name = st.text_input(
            "Company Name",
            value=job_data["company_name"],
            help="Company you're applying to"
        )
    
    # Generate button
    if not st.session_state.letter_data:
        if st.button("✨ Generate Cover Letter", type="primary"):
            if not applicant_name:
                st.error("Please enter your name")
            else:
                with st.spinner("Generating your cover letter..."):
                    try:
                        from frontend.utils import call_api
                        
                        result = asyncio.run(call_api(
                            "/api/v1/generation/generate-letter",
                            json={
                                "job_description": job_data["description"],
                                "resume_text": resume_data["text"],
                                "company_name": company_name,
                                "applicant_name": applicant_name,
                                "match_score": match_data["overall_match_score"],
                                "matched_skills": match_data["matched_skills"]
                            }
                        ))
                        
                        st.session_state.letter_data = result
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        return
    
    # Display generated letter
    letter_data = st.session_state.letter_data
    
    st.success(f"✅ Generated using: {letter_data['model_used']}")
    
    # Editable text area
    edited_letter = st.text_area(
        "Your Cover Letter (editable)",
        value=letter_data["cover_letter"],
        height=400,
        help="You can edit the letter before downloading"
    )
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="📥 Download as Text",
            data=edited_letter,
            file_name=f"cover_letter_{company_name.replace(' ', '_')}.txt",
            mime="text/plain"
        )
    
    with col2:
        if st.button("🔄 Regenerate"):
            st.session_state.letter_data = None
            st.rerun()
    
    with col3:
        if st.button("💾 Save to History"):
            # Save to database
            try:
                # Import database service
                import sys
                sys.path.append('.')
                from backend.services.database_service import db_service
                
                asyncio.run(db_service.save_match(
                    company_name=company_name,
                    job_title=job_data.get("job_title"),
                    job_description=job_data["description"],
                    resume_filename=resume_data["filename"],
                    overall_score=match_data["overall_match_score"],
                    skill_score=match_data["skill_match_score"],
                    semantic_score=match_data["semantic_match_score"],
                    matched_skills=match_data["matched_skills"],
                    missing_skills=match_data["missing_skills"],
                    cover_letter=edited_letter,
                    model_used=letter_data["model_used"]
                ))
                
                st.success("✅ Saved to history!")
                
            except Exception as e:
                st.error(f"❌ Error saving: {str(e)}")