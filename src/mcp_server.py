from pathlib import Path

from cryptography.fernet import Fernet
from fastmcp import FastMCP
from fastmcp.server.auth.providers.auth0 import Auth0Provider

from core.prompt import register_prompts
from core.resources import register_resources
from core.tools import register_tools
import config

auth_provider = Auth0Provider(
    config_url=config.AUTH0_CONFIG_URL,
    client_id=config.AUTH0_CLIENT_ID,
    client_secret=config.AUTH0_SECRET,
    audience=config.AUTH0_AUDIENCE,
    base_url=config.AUTH0_BASE_URL,
)

mcp = FastMCP("ai_resume_editor", auth=auth_provider)
register_tools(mcp)
register_resources(mcp)
register_prompts(mcp)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host=config.HOST, port=config.PORT)
