# 🤖 Agentic AI Job Application Platform

An end-to-end Agentic AI platform that helps job seekers analyze resumes, optimize applications, generate tailored cover letters, prepare for interviews, and track job applications using Generative AI.

Built with **Python, Streamlit, Gemini AI, Plotly, Pandas, and NLP techniques**, this project demonstrates how multiple AI agents can collaborate to automate and improve the job application process.

---

## 🚀 Live Demo

Add your Streamlit deployment link here:

```text
https://your-streamlit-app-url.streamlit.app
```

---

## 📌 Project Overview

Applying for jobs is often repetitive and time-consuming. Candidates must:

* Tailor resumes for each role
* Understand ATS requirements
* Generate cover letters
* Prepare for interviews
* Track multiple applications

This platform automates these tasks through an Agentic AI workflow that simulates multiple specialist agents working together.

---

## 🎯 Key Features

### 📄 CV Upload & Parsing

* Upload resume in PDF format
* Extract text automatically using PyPDF2
* Process resume content for AI analysis

### 🎯 Skill Match Agent

* Compares CV against job descriptions
* Calculates job match score
* Identifies matching skills
* Detects missing skills and competency gaps

### 📝 CV Review Agent

* ATS optimization suggestions
* Resume improvement recommendations
* Keyword enhancement guidance
* Formatting and content recommendations

### ✉️ Cover Letter Agent

* Generates personalized cover letters
* Tailors content to specific job descriptions
* Highlights relevant experience and achievements

### 🎤 Interview Coach Agent

* Generates interview questions
* Provides sample answers
* Covers technical and behavioral scenarios
* Helps candidates prepare effectively

### 📊 Application Dashboard

* Job Match Score
* Skill Signals
* Improvement Areas
* Candidate Fit Radar Chart

### 📁 Application Tracker

* Save analyzed applications
* Track application status
* Monitor interview progress
* Store notes and job links

### 📈 Analytics Dashboard

* Total Applications
* Interviews
* Offers
* Average Match Score
* Application Status Breakdown
* Match Score Distribution

---

# 🧠 Why This Is Agentic AI

This project follows an Agentic AI architecture.

Instead of using a single AI response, the system simulates multiple specialist agents:

```text
Master Agent
│
├── Skill Match Agent
├── CV Review Agent
├── Cover Letter Agent
└── Interview Coach Agent
```

Each agent focuses on a specialized task while the Master Agent coordinates the workflow and produces a unified output.

This approach improves:

* Modularity
* Explainability
* Scalability
* User experience

---

# 🏗️ System Architecture

```text
User
 │
 ▼
Upload CV + Job Description
 │
 ▼
PDF Parsing Layer
(PyPDF2)
 │
 ▼
Master Agent
(Gemini AI)
 │
 ├── Skill Match Agent
 ├── CV Review Agent
 ├── Cover Letter Agent
 └── Interview Coach Agent
 │
 ▼
Streamlit Dashboard
 │
 ▼
Application Tracker
(Pandas CSV Storage)
```

---

# 🛠️ Technology Stack

## Programming Language

* Python

## AI & NLP

* Google Gemini API
* Prompt Engineering
* Generative AI

## Frontend

* Streamlit

## Data Processing

* Pandas
* NumPy

## Visualization

* Plotly

## Document Processing

* PyPDF2

## Deployment

* GitHub
* Streamlit Community Cloud

---

# 📸 Screenshots

## AI Job Application Agent

Features:

* CV Upload
* Job Description Analysis
* AI-Powered Recommendations

Add screenshot:

```text
screenshots/ai_analysis_page.png
```

---

## Application Dashboard

Features:

* Match Score
* Skill Analysis
* Radar Chart

Add screenshot:

```text
screenshots/dashboard.png
```

---

## Application Tracker

Features:

* Job Tracking
* Status Monitoring
* Analytics Dashboard

Add screenshot:

```text
screenshots/application_tracker.png
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/agentic-ai-job-application-platform.git

cd agentic-ai-job-application-platform
```

## Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configure Gemini API

Create:

```text
.env
```

Add:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

Get your API key from:

https://aistudio.google.com/app/apikey

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# ☁️ Deploy to Streamlit Cloud

1. Push project to GitHub
2. Login to Streamlit Cloud
3. Connect GitHub repository
4. Deploy application
5. Add secret:

```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```

under:

```text
Settings → Secrets
```

---

# 📊 Example Workflow

### Step 1

Upload CV

### Step 2

Paste Job Description

### Step 3

AI Analysis

Output:

* Match Score
* Skill Analysis
* ATS Suggestions
* Cover Letter
* Interview Questions

### Step 4

Save Analysis

### Step 5

Track Progress

---

# 🚀 Future Enhancements

* LinkedIn Integration
* Job Scraping Agent
* ATS Score Gauge
* Multi-LLM Support
* Resume Version Control
* Personalized Career Recommendations
* RAG-Based Resume Memory
* Vector Database Integration

---

# 🎓 Author

## Debodip Chowdhury

MSc Financial Technology with Data Science
University of Bristol

BSc (Hons) Computer Science
University of East Anglia

### Connect With Me

LinkedIn:

https://www.linkedin.com/in/debodipchowdhury/

GitHub:

https://github.com/Debodip-cloud

---

# ⭐ Support

If you found this project useful:

* Star the repository
* Connect on LinkedIn
* Subscribe to my YouTube channel
* Share feedback and suggestions

streamlitapp_link: https://agentic-ai-job-application-platform-9gp5eqxmshwsprrjpnqz2i.streamlit.app/
