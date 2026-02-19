import streamlit as st
import asyncio


def show():
    """Job input page"""
    st.title("📝 Job Description Input")
    st.markdown("Paste the job description you're interested in applying for.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        company_name = st.text_input(
            "Company Name",
            placeholder="e.g., TechCorp AI",
            help="Enter the company name"
        )
        
        job_description = st.text_area(
            "Job Description",
            height=300,
            placeholder="Paste the full job description here...",
            help="Must be at least 50 characters"
        )
        
        if st.button("🔍 Extract Skills", type="primary"):
            if not company_name:
                st.error("Please enter a company name")
            elif len(job_description) < 50:
                st.error("Job description must be at least 50 characters")
            else:
                with st.spinner("Extracting skills from job description..."):
                    try:
                        # Import here to avoid circular import
                        from frontend.utils import call_api
                        
                        result = asyncio.run(call_api(
                            "/api/v1/jobs/extract-skills",
                            json={"text": job_description, "company": company_name}
                        ))
                        
                        # Store in session state
                        st.session_state.job_data = {
                            "company_name": company_name,
                            "description": job_description,
                            "skills": result["skills"],
                            "experience_level": result.get("experience_level"),
                            "job_title": result.get("job_title")
                        }
                        
                        st.success("✅ Skills extracted successfully!")
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.session_state.job_data:
            st.markdown("### ✅ Extracted Information")
            
            data = st.session_state.job_data
            
            if data.get("job_title"):
                st.info(f"**Position:** {data['job_title']}")
            
            if data.get("experience_level"):
                st.info(f"**Level:** {data['experience_level']}")
            
            st.markdown(f"**Required Skills ({len(data['skills'])}):**")
            for skill in data['skills'][:10]:
                st.markdown(f"• {skill}")
            if len(data['skills']) > 10:
                st.caption(f"...and {len(data['skills']) - 10} more")
            
            st.markdown("---")
            if st.button("➡️ Next: Upload Resume"):
                st.session_state.page = "resume_upload"
                st.rerun()