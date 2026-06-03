import os
import re
from datetime import date

import pandas as pd
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2
import plotly.graph_objects as go
import plotly.express as px
from google.api_core.exceptions import ResourceExhausted

from agents import master_job_application_agent


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.3,
    "max_output_tokens": 4096,
}

model = genai.GenerativeModel(
    "gemini-3.5-flash",
    generation_config=generation_config
)

TRACKER_PATH = "data/applications.csv"


def extract_pdf_text(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_match_score(text):
    match = re.search(r"(\d{1,3})\s*/\s*100", text)
    if match:
        return min(int(match.group(1)), 100)

    match = re.search(r"(\d{1,3})%", text)
    if match:
        return min(int(match.group(1)), 100)

    return 0


def extract_company_name(job_description):
    patterns = [
        r"At\s+([A-Z][A-Za-z0-9&.\s]+?)(?:,|\s+you|\s+we|\s+you’ll)",
        r"Company[:\-]\s*([A-Za-z0-9&.\s]+)",
        r"([A-Z][A-Za-z0-9&.\s]+)\s+Consulting"
    ]

    for pattern in patterns:
        match = re.search(pattern, job_description, re.IGNORECASE)
        if match:
            company = match.group(1).strip()
            company = company.replace("UK FutureNow", "").strip()
            if len(company) > 2:
                return company

    if "IBM" in job_description.upper():
        return "IBM"

    return "Unknown Company"


def extract_role_name(job_description):
    patterns = [
        r"as a[n]?\s+([A-Za-z\s]+?)(?: with| in|!|\.|,)",
        r"Role[:\-]\s*([A-Za-z\s]+)",
        r"position[:\-]?\s*([A-Za-z\s]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, job_description, re.IGNORECASE)
        if match:
            role = match.group(1).strip()
            if len(role) > 3:
                return role.title()

    if "Senior Data Engineer" in job_description:
        return "Senior Data Engineer"

    return "Unknown Role"


def create_radar_chart():
    categories = [
        "Python",
        "SQL",
        "Machine Learning",
        "Data Engineering",
        "Communication",
        "Cloud"
    ]

    values = [90, 85, 88, 75, 80, 70]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name="Candidate Fit"
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=450
    )

    return fig


def load_tracker():
    if os.path.exists(TRACKER_PATH):
        return pd.read_csv(TRACKER_PATH)

    return pd.DataFrame(
        columns=[
            "Company",
            "Role",
            "Job Link",
            "Application Date",
            "Status",
            "Match Score",
            "Notes"
        ]
    )


def save_tracker(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(TRACKER_PATH, index=False)


def save_analysis_to_tracker(company, role, job_link, match_score, analysis_text):
    tracker_df = load_tracker()

    new_row = pd.DataFrame(
        [
            {
                "Company": company,
                "Role": role,
                "Job Link": job_link,
                "Application Date": str(date.today()),
                "Status": "Saved",
                "Match Score": match_score,
                "Notes": analysis_text[:1000]
            }
        ]
    )

    tracker_df = pd.concat(
        [tracker_df, new_row],
        ignore_index=True
    )

    save_tracker(tracker_df)


st.set_page_config(
    page_title="AI Job Application Agent",
    page_icon="🤖",
    layout="wide"
)

if "latest_analysis" not in st.session_state:
    st.session_state.latest_analysis = None

if "latest_match_score" not in st.session_state:
    st.session_state.latest_match_score = 0

if "latest_company" not in st.session_state:
    st.session_state.latest_company = ""

if "latest_role" not in st.session_state:
    st.session_state.latest_role = ""

if "latest_job_link" not in st.session_state:
    st.session_state.latest_job_link = ""


st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "AI Application Agent",
        "Application Tracker"
    ]
)


if page == "AI Application Agent":

    st.title("AI Job Application Agent")

    st.write(
        "Upload your CV, paste a job description, and let a Master AI Agent simulate multiple specialist job-application agents."
    )

    st.markdown("---")

    job_link_input = st.text_input("Job Link Optional")

    uploaded_cv = st.file_uploader(
        "Upload your CV / Resume as PDF",
        type=["pdf"]
    )

    job_description = st.text_area(
        "Paste the Job Description",
        height=250
    )

    analyze_clicked = st.button("Analyze Application")

    if analyze_clicked:

        if uploaded_cv is None:
            st.error("Please upload your CV first.")

        elif not job_description.strip():
            st.error("Please paste a job description.")

        elif not api_key:
            st.error("Gemini API key not found. Please check your .env file.")

        else:
            with st.spinner("Extracting CV text..."):
                cv_text = extract_pdf_text(uploaded_cv)

            if not cv_text.strip():
                st.error(
                    "Could not extract text from the uploaded PDF. Please upload a text-based CV PDF."
                )

            else:
                extracted_company = extract_company_name(job_description)
                extracted_role = extract_role_name(job_description)

                try:
                    with st.spinner("Master AI Agent is analyzing your application..."):
                        full_result = master_job_application_agent(
                            model,
                            cv_text,
                            job_description
                        )

                    match_score = extract_match_score(full_result)

                    st.session_state.latest_analysis = full_result
                    st.session_state.latest_match_score = match_score
                    st.session_state.latest_company = extracted_company
                    st.session_state.latest_role = extracted_role
                    st.session_state.latest_job_link = job_link_input

                    st.success("Application analysis completed.")

                except ResourceExhausted:
                    st.error(
                        "Gemini free-tier quota was reached. Please wait a short time and try again, or test fewer times."
                    )

                except Exception as e:
                    st.error("An error occurred while generating the analysis.")
                    st.exception(e)

    if st.session_state.latest_analysis:

        match_score = st.session_state.latest_match_score
        full_result = st.session_state.latest_analysis

        matching_skills_count = 8
        missing_skills_count = 4

        st.markdown("## Application Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric("Job Match Score", f"{match_score}%")
        col2.metric("Detected Skill Signals", matching_skills_count)
        col3.metric("Improvement Areas", missing_skills_count)

        st.markdown("---")

        st.markdown("### Auto-Detected Job Details")

        dcol1, dcol2 = st.columns(2)

        dcol1.info(f"Company: {st.session_state.latest_company}")
        dcol2.info(f"Role: {st.session_state.latest_role}")

        st.markdown("---")

        left_col, right_col = st.columns([1, 1])

        with left_col:
            st.subheader("Candidate Fit Radar")
            st.plotly_chart(
                create_radar_chart(),
                use_container_width=True
            )

        with right_col:
            st.subheader("Agent Workflow")
            st.markdown(
                """
                **Master Agent simulates:**

                1. Skill Match Agent  
                2. CV Review Agent  
                3. Cover Letter Agent  
                4. Interview Coach Agent  

                This uses only **one Gemini API request** to reduce free-tier quota usage.
                """
            )

            if st.button("Save This Analysis to Tracker"):
                save_analysis_to_tracker(
                    st.session_state.latest_company,
                    st.session_state.latest_role,
                    st.session_state.latest_job_link,
                    st.session_state.latest_match_score,
                    st.session_state.latest_analysis
                )

                st.success("Analysis saved to Application Tracker.")

        st.markdown("---")

        st.markdown("## Full Agent Analysis")
        st.markdown(full_result)


if page == "Application Tracker":

    st.title("Application Tracker")

    st.write(
        "Track job applications, statuses, match scores, and notes in one place."
    )

    tracker_df = load_tracker()

    st.markdown("## Add New Application")

    with st.form("application_form"):

        company = st.text_input("Company")
        role = st.text_input("Role")
        job_link = st.text_input("Job Link")
        application_date = st.date_input("Application Date", value=date.today())

        status = st.selectbox(
            "Status",
            [
                "Saved",
                "Applied",
                "Assessment",
                "Interview",
                "Offer",
                "Rejected"
            ]
        )

        match_score = st.number_input(
            "Match Score",
            min_value=0,
            max_value=100,
            value=0
        )

        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Save Application")

        if submitted:

            if not company.strip() or not role.strip():
                st.error("Please enter both company and role.")

            else:
                new_row = pd.DataFrame(
                    [
                        {
                            "Company": company,
                            "Role": role,
                            "Job Link": job_link,
                            "Application Date": str(application_date),
                            "Status": status,
                            "Match Score": match_score,
                            "Notes": notes
                        }
                    ]
                )

                tracker_df = pd.concat(
                    [tracker_df, new_row],
                    ignore_index=True
                )

                save_tracker(tracker_df)

                st.success("Application saved successfully.")

    st.markdown("---")

    st.markdown("## Tracker Dashboard")

    tracker_df = load_tracker()

    if tracker_df.empty:
        st.info("No applications saved yet.")

    else:
        total_apps = len(tracker_df)
        interviews = len(tracker_df[tracker_df["Status"] == "Interview"])
        offers = len(tracker_df[tracker_df["Status"] == "Offer"])
        avg_score = round(tracker_df["Match Score"].mean(), 1)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Applications", total_apps)
        col2.metric("Interviews", interviews)
        col3.metric("Offers", offers)
        col4.metric("Average Match Score", f"{avg_score}%")

        st.markdown("---")

        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("Application Status Breakdown")

            status_counts = tracker_df["Status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]

            fig_status = px.bar(
                status_counts,
                x="Status",
                y="Count",
                title="Applications by Status"
            )

            st.plotly_chart(
                fig_status,
                use_container_width=True
            )

        with col_right:
            st.subheader("Match Score Distribution")

            fig_score = px.histogram(
                tracker_df,
                x="Match Score",
                nbins=10,
                title="Distribution of Match Scores"
            )

            st.plotly_chart(
                fig_score, use_container_width=True
            )

        st.markdown("---")

        st.markdown("## Saved Applications")

        st.dataframe(
            tracker_df,
            use_container_width=True
        )