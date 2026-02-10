from fastmcp.server import FastMCP
from db.repo import user_repository


def register_prompts(mcp: FastMCP):
    @mcp.prompt("Create a new resume")
    def create_resume(name: str, company_name: str, position: str, job_posting: str):
        """name = user_id from the auth token."""
        user_info = user_repository.get_user_resume_json(name)
        if user_info is None:
            return "User information not found"
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

Here is the user information:
{user_info}

Use the save_catered_resume_data tool to save the resume data before making the call to generate_pdf.
The save_catered_resume_data tool returns a "job_name" field — pass that value as the job_name parameter to generate_pdf.
If the generated resume is more than 1 page, remake the catered_resume_data and save it again.
Repeat the process until the generated resume is no more than 1 page.
If the page_fill is less than 0.90, add more content to better fill the page.
"""
        return prompt
