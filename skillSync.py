from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import crew_ai_skillSync  # Your Crew AI app
import pdfplumber


app = FastAPI()

# Serve form HTML
@app.get("/", response_class=HTMLResponse)
def read_form():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Resume Skill Match</title>
    </head>
    <body>
        <h2>Upload Resume and Job Description</h2>
        <form action="/upload/" method="post">
            <label for="resume">Resume:</label><br>
            <input  type = "file" name = "resume" id = "resume"><br>
            <label for="job_description">Job Description:</label><br>
            <textarea name="job_description" id="job_description" rows="10" cols="70"></textarea><br><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """
#PDF-TEXT


def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf_file:
        text_extracted = []
        for page in pdf_file.pages:
            tables = page.extract_tables()
            text_extracted.append(
                {
                    "text": page.extract_text(),
                    "tables": tables
                }
            )
        return "\n\n".join(map(str, text_extracted))
    

# Handle form submission and display result
@app.post("/upload/", response_class=HTMLResponse)
def upload_resume(resume: str = Form(...), job_description: str = Form(...)):

    resume = extract_text_from_pdf(resume)
    # Call Crew AI application
    result = crew_ai_skillSync.skill_sync_crew.kickoff(inputs={
        "resume_text": resume,
        "jd_text": job_description,
        "resume_skills_summary": "",
        "jd_skills_summary": ""
    })
    
    
    # Return result in a simple HTML page
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Matching Result</title>
    </head>
    <body>
        <h2>Matching Result</h2>
        <p>{result}</p>
        <a href="/">Go Back</a>
    </body>
    </html>
    """
