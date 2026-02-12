from pathlib import Path
from fastmcp import Context, FastMCP
import pymupdf
from doc_utils.doc_builder import DocBuilder
from doc_utils.doc_model import (
    AdditionalsListedSectionContent,
    DocModel,
    SectionContent,
)
from fastmcp.server.dependencies import get_access_token
from db.repo import (
    additionals_repository,
    user_repository,
    catered_resume_repository,
    section_repository,
)

output_dir = Path("output")


def register_tools(mcp: FastMCP):
    @mcp.tool()
    def upsert_user_additionals(title: str, content: AdditionalsListedSectionContent):
        """Updates the user's additionals details in the database.
        title: The title of the additionals to update. (eg. "Certifications", "Skills")
        """
        user_id = get_access_token().claims.get("sub")
        additionals_repository.upsert_additionals(user_id, title, content)
        return {
            "success": True,
            "message": f"Updated additionals {title} for {user_id}",
        }

    @mcp.tool()
    def get_user_additionals(title: str):
        """Gets the user's additionals details from the database.
        title: The title of the additionals to get. (eg. "Certifications", "Skills")
        """
        user_id = get_access_token().claims.get("sub")
        content = additionals_repository.get_additionals(user_id, title)
        if content is None:
            return "Additionals not found"
        return content

    @mcp.tool()
    def upsert_user_section(section_name: str, content: SectionContent):
        """Updates the user's section details in the database.
        section_name: The name of the section to update. (eg. "Education", "Work Experience")
        """
        user_id = get_access_token().claims.get("sub")
        section_repository.upsert_section(user_id, section_name, content)
        return {
            "success": True,
            "message": f"Updated section {section_name} for {user_id}",
        }

    @mcp.tool()
    def get_user_sections():
        """Gets the user's sections details from the database."""
        user_id = get_access_token().claims.get("sub")
        sections = section_repository.get_all_sections(user_id)
        return sections

    @mcp.tool()
    def save_user_data(data: DocModel):
        """Saves the user's resume data to the database."""
        user_id = get_access_token().claims.get("sub")
        user_repository.upsert_user(user_id, data)
        return {
            "success": True,
            "message": f"Saved user data for {data.user_info.full_name}",
        }

    @mcp.tool()
    def save_catered_resume_data(job: str, data: DocModel):
        """Saves the catered resume data to the database.
        Returns the job_name to pass to generate_pdf.
        """
        user_id = get_access_token().claims.get("sub")
        if not user_repository.check_user(user_id):
            return {
                "success": False,
                "message": "User not found, please ask them to upload a sample resume first to generate a user information pool.",
            }

        catered_resume_repository.save_catered_resume(user_id, job, data)
        return {
            "success": True,
            "message": f"Saved catered resume data for {data.user_info.full_name} — job: {job}",
            "job_name": job,
        }

    @mcp.tool()
    def get_catered_resume_data(job_name: str):
        """Gets the catered resume data for a specific job from the database."""
        user_id = get_access_token().claims.get("sub")
        data = catered_resume_repository.get_catered_resume_json(user_id, job_name)
        if data is None:
            return {
                "success": False,
                "message": f"Catered resume not found for {job_name}, Ask them to upload a new job posting and try again.",
            }
        return {
            "success": True,
            "message": f"Got catered resume data for {data.user_info.full_name} — job: {job_name}",
            "data": data,
        }

    @mcp.tool()
    def generate_pdf(job_name: str):
        """Generates a PDF from the catered resume data stored in the database.

        Args:
            job_name: The job name used when saving the catered resume via save_catered_resume_data.
                      Also used for the output PDF file name.

        Returns metadata including page count, file size, and output path.
        """
        user_id = get_access_token().claims.get("sub")
        doc_model = catered_resume_repository.get_catered_resume(user_id, job_name)
        if doc_model is None:
            return {
                "success": False,
                "message": f"Catered resume not found for {job_name}, Ask them to upload a new job posting and try again.",
            }

        output_dir.mkdir(parents=True, exist_ok=True)
        builder = DocBuilder(doc_model, job_name)
        builder.build()
        return builder.export()
