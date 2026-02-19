import streamlit as st
import asyncio


def show():
    """Resume upload page"""
    st.title("📄 Resume Upload")
    st.markdown("Upload your resume (PDF or DOCX format)")
    
    if not st.session_state.job_data:
        st.warning("⚠️ Please input job description first")
        return
    
    # Show job context
    st.info(f"📌 Applying to: **{st.session_state.job_data['company_name']}**")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose your resume",
            type=["pdf", "docx"],
            help="Upload PDF or Word document"
        )
        
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            if st.button("📊 Parse Resume", type="primary"):
                with st.spinner("Parsing your resume..."):
                    try:
                        from frontend.utils import call_api
                        
                        # Prepare file for upload
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                        
                        result = asyncio.run(call_api(
                            "/api/v1/resumes/parse-resume",
                            files=files
                        ))
                        
                        # Store in session state
                        st.session_state.resume_data = {
                            "filename": uploaded_file.name,
                            "text": result["text"],
                            "skills": result["skills"],
                            "contact": result["contact"],
                            "years_experience": result.get("years_experience"),
                            "file_type": result["file_type"]
                        }
                        
                        st.success("✅ Resume parsed successfully!")
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.session_state.resume_data:
            st.markdown("### ✅ Extracted Information")
            
            data = st.session_state.resume_data
            
            # Contact info
            if data["contact"].get("email"):
                st.info(f"📧 {data['contact']['email']}")
            if data["contact"].get("phone"):
                st.info(f"📱 {data['contact']['phone']}")
            
            # Experience
            if data.get("years_experience"):
                st.metric("Experience", f"{data['years_experience']} years")
            
            # Skills
            st.markdown(f"**Your Skills ({len(data['skills'])}):**")
            for skill in data['skills'][:10]:
                st.markdown(f"• {skill}")
            if len(data['skills']) > 10:
                st.caption(f"...and {len(data['skills']) - 10} more")
            
            st.markdown("---")
            if st.button("➡️ Next: Calculate Match"):
                st.session_state.page = "match_display"
                st.rerun()