import pdfplumber
from crewai import Agent, Task, Crew, LLM
llm = LLM(model="gpt-4o-mini")
# Define the agents

resume_reader = Agent(
    role="Resume Reader",
    goal="Read a resume and extract all skills mentioned.",
    backstory="You are an expert at parsing resumes to find and list all technical and soft skills.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

jd_analyst = Agent(
    role="Job Description Analyst",
    goal="Read a job description, summarize the required skills, and enrich the text.",
    backstory="You are a skilled recruiter who understands job descriptions deeply and can identify core skills and keywords.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

matcher = Agent(
    role="Profile Matcher",
    goal="Analyze the skills from a resume and a job description and determine the best match level.",
    backstory="You are a professional HR specialist who makes final decisions on candidate suitability based on a skills comparison.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Define the tasks

read_resume_task = Task(
    description=(
        "Read the provided resume text below and generate a concise summary of the candidate's skills, formatted as a bulleted list. "
        "Resume Text: {resume_text}"
    ),
    agent=resume_reader,
    expected_output="A bulleted list of skills extracted from the resume.",
)

analyze_jd_task = Task(
    description=(
        "Read the job description text below. Summarize the key skills and qualifications required for the role. "
        "Job Description Text: {jd_text}"
    ),
    agent=jd_analyst,
    expected_output="A summary of required skills from the job description.",
)

match_profile_task = Task(
    description=(
        "Compare the skills from the resume summary with the required skills from the job description summary. "
        "Based on the comparison, classify the candidate's profile into one of three categories: 'Best Match', 'OK to Go', or 'Irrelevant Profile'. "
        "Provide a brief, one-sentence justification for your classification. "
        "Resume Skills: {resume_skills_summary}\n"
        "Job Description Skills: {jd_skills_summary}"
    ),
    agent=matcher,
    expected_output="The classification (Best Match, OK to Go, or Irrelevant Profile) with a brief justification.",
)


# Define the crew

skill_sync_crew = Crew(
    agents=[resume_reader, jd_analyst, matcher],
    tasks=[read_resume_task, analyze_jd_task, match_profile_task],
    verbose=True
)