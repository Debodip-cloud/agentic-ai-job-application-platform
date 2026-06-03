import google.generativeai as genai


def skill_match_agent(model, cv_text, job_description):

    prompt = f"""
    Compare the CV and Job Description.

    CV:
    {cv_text}

    Job Description:
    {job_description}

    Return:

    1. Match Score (0-100)
    2. Matching Skills
    3. Missing Skills
    """

    return model.generate_content(prompt).text


def cv_improvement_agent(model, cv_text, job_description):

    prompt = f"""
    Review this CV against the job description.

    CV:
    {cv_text}

    Job Description:
    {job_description}

    Return:

    1. ATS Optimization Suggestions
    2. Missing Keywords
    3. CV Improvement Recommendations
    """

    return model.generate_content(prompt).text


def cover_letter_agent(model, cv_text, job_description):

    prompt = f"""
    Create a professional cover letter.

    Candidate CV:
    {cv_text}

    Job Description:
    {job_description}
    """

    return model.generate_content(prompt).text


def interview_agent(model, cv_text, job_description):

    prompt = f"""
    You are an expert interview coach.

    Based on the CV and job description, generate a concise interview preparation guide.

    CV:
    {cv_text}

    Job Description:
    {job_description}

    Return only:

    ## Interview Questions

    1. One leadership question
    2. One technical data engineering question
    3. One machine learning question
    4. One stakeholder communication question
    5. One consulting/business impact question

    For each question, provide:
    - Why this question may be asked
    - A short suggested answer using the candidate's experience

    Keep the total answer under 900 words.
    """

    return model.generate_content(prompt).text
def master_job_application_agent(model, cv_text, job_description):

    prompt = f"""
    You are an Agentic AI Job Application Assistant.

    You are simulating four specialist agents:
    1. Skill Match Agent
    2. CV Review Agent
    3. Cover Letter Agent
    4. Interview Coach Agent

    Analyze the CV and job description.

    CV:
    {cv_text}

    Job Description:
    {job_description}

    Return the output in this exact structure:

    ## Skill Match Agent
    Match Score: __/100

    Matching Skills:
    - skill 1
    - skill 2
    - skill 3
    - skill 4
    - skill 5

    Missing Skills:
    - missing skill 1
    - missing skill 2
    - missing skill 3

    ## CV Review Agent
    ATS Suggestions:
    - suggestion 1
    - suggestion 2
    - suggestion 3

    CV Improvement Recommendations:
    - recommendation 1
    - recommendation 2
    - recommendation 3

    ## Cover Letter Agent
    Write a concise professional cover letter under 350 words.

    ## Interview Coach Agent
    Provide 5 interview questions with short suggested answers.
    Keep this section under 600 words.
    """

    return model.generate_content(prompt).text