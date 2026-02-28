import streamlit as st
import asyncio
import pandas as pd
from frontend.utils import call_api


def show():
    """History page"""
    st.title("📚 Application History")

    try:
        # Only fetch if not already cached, or after delete
        if "history_data" not in st.session_state or st.session_state.get("history_refresh"):
            with st.spinner("Loading applications..."):
                matches = asyncio.run(call_api("/api/v1/applications/all", method="GET"))
            st.session_state.history_data = matches
            st.session_state.history_refresh = False
        else:
            matches = st.session_state.history_data
        if not matches:
            st.info("No saved applications yet. Complete a workflow and save it!")
            return

        st.markdown(f"### Total Applications: {len(matches)}")

        data = []
        for m in matches:
            data.append({
                "Date": m["created_at"][:16],
                "Company": m["company_name"],
                "Position": m["job_title"] or "N/A",
                "Match Score": f"{m['overall_score']:.1f}%",
                "Resume": m["resume_filename"]
            })

        df = pd.DataFrame(data)
        st.table(df)

        st.markdown("---")
        st.markdown("### 📄 View Details")

        options = {f"{m['company_name']} — {m['created_at'][:16]} ({m['id']})": m for m in matches}
        selected_label = st.selectbox("Select application", options=list(options.keys()), index=0)
        selected = options[selected_label]

        if selected:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Score", f"{selected['overall_score']:.1f}%")
            with col2:
                st.metric("Skill Score", f"{selected['skill_score']:.1f}%")
            with col3:
                st.metric("Semantic Score", f"{selected['semantic_score']:.1f}%")

            if selected["cover_letter"]:
                st.markdown("### ✉️ Cover Letter")
                st.text_area(
                    "Saved Letter",
                    value=selected["cover_letter"],
                    height=300,
                    disabled=True
                )
                st.download_button(
                    "📥 Download Letter",
                    data=selected["cover_letter"],
                    file_name=f"cover_letter_{selected['company_name']}.txt",
                    mime="text/plain"
                )

            if st.button("🗑️ Delete This Application", type="secondary"):
                asyncio.run(call_api(
                    f"/api/v1/applications/{selected['id']}",
                    method="DELETE"
                ))
                st.session_state.history_refresh = True
                st.session_state.pop("history_data", None)
                st.rerun()

    except Exception as e:
        st.error(f"❌ Error loading history: {str(e)}")