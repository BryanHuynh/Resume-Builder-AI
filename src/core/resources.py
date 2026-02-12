from pathlib import Path
from fastmcp import FastMCP
from fastmcp.resources.types import FileResource
from db.repo import user_repository
from db.repo.user_repository import get_user_resume_json
from fastmcp.server.dependencies import get_access_token


def register_resources(mcp: FastMCP):
    @mcp.resource(
        "doc://resume/full",
        mime_type="application/json",
        name="get_complete_user_resume_information",
        description="Gets the complete set of user information required to generate a resume.",
    )
    def get_resume_data():
        """Loads resume data from the database. name = user_id."""
        user_id = get_access_token().claims.get("sub")
        user_resume = user_repository.get_user_resume_json(user_id)
        if user_resume is None:
            return "User Resume not found. Ask them to upload a sample resume so you can generate a user information pool."
        return user_resume

