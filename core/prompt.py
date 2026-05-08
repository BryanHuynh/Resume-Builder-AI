from pathlib import Path
from fastmcp.server import FastMCP


docs_dir = Path("documents")
user_dir = docs_dir / "user_data"


def register_prompts(mcp: FastMCP):
    @mcp.prompt("Create a new resume")
    def create_resume(name: str, company_name: str, position: str, job_posting: str):
        user_data = Path(f"{user_dir}/{name}.json")
        if not user_data.exists():
            return "User information not found"
        with open(user_data, "r") as f:
            user_info = f.read()
        prompt = f"""
You are a resume writer. 
You are tasked with creating a resume for a new job opening. 
The company name is {company_name} and the position is {position}.
The job posting is as follows:
{job_posting}

Your task is to create a resume that highlights the job posting and showcases your relevant experience and skills. 
Please ensure that the resume is well-organized, concise, and visually appealing. 
Use a professional and polished writing style, and include relevant information such as education, work experience, and skills.
If you believe a point can be improved, please suggest a change, but do not change the content.
Remove any unnessary information and or points that are not relevant to the job posting.
If there is any additional information that you want to know about the user to help fill out the resume, please ask.
If there is information about certifications, remove any that are not relevant to the job posting.
Do not remove any sub-sections, expecially if they include business impact.

Resume section ordering:
DocBuilder renders the sections dictionary in the order it appears in the JSON, so intentionally order the sections before saving.
For experienced candidates, use this default order: relevant Work Experience or Professional Experience first, then relevant Projects, Leadership, Activities, or Accomplishments, then Education. Keep Skills, Certifications, and Additional Information at the end unless they are required or unusually important for the target role.
For recent graduates or candidates with limited direct experience, use this default order: Education first, then Projects, Internships, or Relevant Experience, then Leadership or Activities, then Skills and Additional Information.
For career changes, place the strongest job-relevant proof near the top, such as relevant projects, transferable experience, required certifications, or role-specific skills.
Within each section, order entries in reverse chronological order by default. If creating a dedicated relevant section, put the most relevant entries and bullet points first.

Here is the user information:
{user_info}

Use the save_catered_resume_data tool to save the resume data to the catered_resume_data directory before making the call to generate_pdf.
The save_catered_resume_data tool returns a "filename" field — pass that value as the filename parameter to generate_pdf.
After the first save, do not resend the full resume for small page-fit changes.
If the generated resume is more than 1 page, call get_catered_resume_outline with the returned filename, then use the catered resume CRUD tools to remove or replace whole sections, whole subsection entries, or whole additionals subsection lists only.
If the page_fill is less than 0.90, call get_catered_resume_outline with the returned filename, then use the catered resume CRUD tools to add or replace whole sections, whole subsection entries, or whole additionals subsection lists only.
After each CRUD operation, call generate_pdf again with the same filename and repeat until the generated resume is no more than 1 page and the page_fill is at least 0.90 when possible.
"""
        return prompt
