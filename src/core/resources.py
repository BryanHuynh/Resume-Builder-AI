from pathlib import Path
from fastmcp import FastMCP
from fastmcp.resources.types import FileResource
from db.repo import user_repository


def register_resources(mcp: FastMCP):
    @mcp.resource("doc://resume/{name}", mime_type="application/json")
    def get_resume_data(name: str):
        """Loads resume data from the database. name = user_id."""
        data = user_repository.get_user_resume_json(name)
        if data is None:
            return "User data not found"
        return data

    @mcp.resource("doc://resume/output/{filename}", mime_type="application/pdf")
    def get_catered_resume(filename: str):
        resume_data = Path(f"output/{filename}.pdf")
        if not resume_data.exists():
            return None
        return FileResource(
            mime_type="application/pdf",
            is_binary=True,
            path=resume_data.absolute(),
            uri=resume_data.resolve().as_uri(),
        ).read()
