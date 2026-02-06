from pathlib import Path
from fastmcp.server import FastMCP


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
        with open(resume_data, "rb") as f:
            return f.read()
        