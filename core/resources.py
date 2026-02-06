from pathlib import Path
from fastmcp import FastMCP
from fastmcp.server.transforms import ResourcesAsTools
from fastmcp.resources.types import FileResource


docs_dir = Path("documents")
user_dir = docs_dir / "user_data"


def register_resources(mcp: FastMCP):
    @mcp.resource("doc://resume/{name}", mime_type="application/json")
    def get_resume_data(name: str):
        user_data = Path(f"{user_dir}/{name}.json")
        if not user_data.exists():
            return None
        with open(user_data, "r") as f:
            return f.read()

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
    
