import base64
from pathlib import Path
import re
from core.prompt import register_prompts
from core.resources import register_resources
from core.tools import register_tools
from doc_utils.doc_builder import DocBuilder
from doc_utils.doc_model import DocModel, SectionContentDescriptions
from fastmcp import FastMCP

mcp = FastMCP("ai_resume_editor")
register_tools(mcp)
register_resources(mcp)
register_prompts(mcp)

if __name__ == "__main__":
    mcp.run()

    
