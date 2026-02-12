import json
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from scalekit import ScalekitClient
import logging

from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from scalekit.common.scalekit import TokenValidationOptions

import config


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

security = HTTPBearer()

scalekit_client = ScalekitClient(
    config.SCALEKIT_ENVIRONMENT_URL,
    config.SCALEKIT_CLIENT_ID,
    config.SCALEKIT_CLIENT_SECRET,
)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/.well-known/"):
            return await call_next(request)

        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=401, detail="Authorization header is missing or invalid"
                )

            token = auth_header.split("Bearer ")[1]

            request_body = await request.body()

            try:
                request_data = json.loads(request_body.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                request_data = {}

            validation_options = TokenValidationOptions(
                issuer=config.SCALEKIT_ENVIRONMENT_URL,
                audience=[config.SCALEKIT_RESOURCE_NAME],
            )

            is_tool_call = request_data.get("method") == "tools/call"

            required_scopes = ["search:read"]

            if is_tool_call:
                validation_options.required_scopes = required_scopes

            try:
                scalekit_client.validate_token(token, validation_options)
            except Exception as e:
                logger.error(f"Error validating token: {e}")
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token or token does not have required scopes",
                )

        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "error": "unauthorized" if e.status_code == 401 else "forbidden",
                    "error_description": e.detail,
                },
                headers={
                    "WWW-Authenticate": f'Bearer realm="OAUTH", resource_metadata="{config.SCALEKIT_RESOURCE_METADATA_URL}"'
                },
            )
        return await call_next(request)
