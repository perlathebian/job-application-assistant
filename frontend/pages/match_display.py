import streamlit as st
import plotly.graph_objects as go
import asyncio


def show():
    """Match display page"""
    st.title("🎯 Match Analysis")
    
    if not st.session_state.job_data or not st.session_state.resume_data:
        st.warning("⚠️ Please complete previous steps first")
        return
    
    job_data = st.session_state.job_data
    resume_data = st.session_state.resume_data
    
    # Show context
    st.info(f"📌 **{job_data['company_name']}** vs **{resume_data['filename']}**")
    
    # Calculate match button
    if not st.session_state.match_data:
        if st.button("🔄 Calculate Match Score", type="primary"):
            with st.spinner("Analyzing match..."):
                try:
                    from frontend.utils import call_api
                    
                    result = asyncio.run(call_api(
                        "/api/v1/matching/match",
                        json={
                            "job_description": job_data["description"],
                            "job_skills": job_data["skills"],
                            "resume_text": resume_data["text"],
                            "resume_skills": resume_data["skills"]
                        }
                    ))
                    
                    st.session_state.match_data = result
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        return
    
    # Display match results
    match_data = st.session_state.match_data
    
    # Score gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=match_data["overall_match_score"],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Match Score", 'font': {'size': 24}},
        delta={'reference': 70, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "#ffcccc"},
                {'range': [50, 70], 'color': "#ffffcc"},
                {'range': [70, 100], 'color': "#ccffcc"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed scores
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Skill Match",
            f"{match_data['skill_match_score']:.1f}%",
            help="Percentage of required skills you have"
        )
    
    with col2:
        st.metric(
            "Semantic Match",
            f"{match_data['semantic_match_score']:.1f}%",
            help="How well your experience aligns"
        )
    
    with col3:
        st.metric(
            "Overall Score",
            f"{match_data['overall_match_score']:.1f}%",
            help="Weighted average (60% skills, 40% semantic)"
        )
    
    # Recommendation
    st.markdown("### 💡 Recommendation")
    rec = match_data["recommendation"]
    if "Excellent" in rec:
        st.success(f"✅ {rec}")
    elif "Good" in rec:
        st.info(f"ℹ️ {rec}")
    elif "Moderate" in rec:
        st.warning(f"⚠️ {rec}")
    else:
        st.error(f"❌ {rec}")
    
    # Skills breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Matched Skills")
        if match_data["matched_skills"]:
            for skill in match_data["matched_skills"]:
                st.markdown(f"• {skill}")
        else:
            st.caption("No matched skills found")
    
    with col2:
        st.markdown("### ❌ Missing Skills")
        if match_data["missing_skills"]:
            for skill in match_data["missing_skills"]:
                st.markdown(f"• {skill}")
        else:
            st.caption("No missing skills!")
    
    # Next step button
    st.markdown("---")
    if st.button("➡️ Next: Generate Cover Letter", type="primary"):
        st.session_state.page = "letter_display"
        st.rerun()