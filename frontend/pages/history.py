import streamlit as st
import asyncio
import pandas as pd


def show():
    """History page"""
    st.title("📚 Application History")
    
    try:
        # Import database service
        import sys
        sys.path.append('.')
        from backend.services.database_service import db_service
        
        # Get all matches
        matches = asyncio.run(db_service.get_all_matches())
        
        if not matches:
            st.info("No saved applications yet. Complete a workflow and save it!")
            return
        
        # Display as table
        st.markdown(f"### Total Applications: {len(matches)}")
        
        # Convert to dataframe
        data = []
        for match in matches:
            data.append({
                "Date": match.created_at.strftime("%Y-%m-%d %H:%M"),
                "Company": match.company_name,
                "Position": match.job_title or "N/A",
                "Match Score": f"{match.overall_score:.1f}%",
                "Resume": match.resume_filename
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # Detail view
        st.markdown("---")
        st.markdown("### 📄 View Details")
        
        selected_company = st.selectbox(
            "Select application",
            options=[m.company_name for m in matches],
            index=0
        )
        
        # Find selected match
        selected_match = next((m for m in matches if m.company_name == selected_company), None)
        
        if selected_match:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Overall Score", f"{selected_match.overall_score:.1f}%")
            with col2:
                st.metric("Skill Score", f"{selected_match.skill_score:.1f}%")
            with col3:
                st.metric("Semantic Score", f"{selected_match.semantic_score:.1f}%")
            
            # Show cover letter
            if selected_match.cover_letter:
                st.markdown("### ✉️ Cover Letter")
                st.text_area(
                    "Saved Letter",
                    value=selected_match.cover_letter,
                    height=300,
                    disabled=True
                )
                
                st.download_button(
                    "📥 Download Letter",
                    data=selected_match.cover_letter,
                    file_name=f"cover_letter_{selected_match.company_name}.txt",
                    mime="text/plain"
                )
            
            # Delete button
            if st.button("🗑️ Delete This Application", type="secondary"):
                asyncio.run(db_service.delete_match(selected_match.id))
                st.success("Deleted!")
                st.rerun()
    
    except Exception as e:
        st.error(f"❌ Error loading history: {str(e)}")