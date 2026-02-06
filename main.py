import base64
from pathlib import Path
import re
from core.prompt import register_prompts
from core.resources import register_resources
from core.tools import register_tools
from doc_utils.doc_builder import DocBuilder
from doc_utils.doc_model import DocModel
from mcp.server import FastMCP


mcp = FastMCP()
register_tools(mcp)
register_resources(mcp)
register_prompts(mcp)

if __name__ == "__main__":
    # mcp.run(transport="streamable-http")
    mcp.run()
    # docs_dir = Path("documents")
    # user_dir = docs_dir / "user_data"
    # catered_resume_dir = docs_dir / "catered_resume_data"
    # filename = "user_folder/job_name.json"
    # job_name="Developer"

    # output_dir = Path("output")
    # resume_path = catered_resume_dir / Path(filename)
    # with open(resume_path, "r") as f:
    #     data = f.read()
    # output_dir.mkdir(parents=True, exist_ok=True)
    # doc_model = DocModel.model_validate_json(data)
    # builder = DocBuilder(doc_model, job_name)
    # builder.build()
    # export_path = builder.export()
    
    
