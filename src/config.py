from dotenv import load_dotenv
import os

load_dotenv()


#auth0 config
AUTH0_CONFIG_URL=os.getenv("AUTH0_CONFIG_URL", None)
AUTH0_CLIENT_ID=os.getenv("AUTH0_CLIENT_ID", None)
AUTH0_SECRET=os.getenv("AUTH0_SECRET", None)
AUTH0_AUDIENCE=os.getenv("AUTH0_AUDIENCE", None)
AUTH0_BASE_URL=os.getenv("AUTH0_BASE_URL", "http://localhost:8000")

assert AUTH0_CONFIG_URL is not None, "AUTH0_CONFIG_URL must be set"
assert AUTH0_CLIENT_ID is not None, "AUTH0_CLIENT_ID must be set"
assert AUTH0_SECRET is not None, "AUTH0_SECRET must be set"
assert AUTH0_AUDIENCE is not None, "AUTH0_AUDIENCE must be set"

# AWS
AWS_PDF_FUNCTION_URL = os.getenv("AWS_PDF_FUNCTION_URL", "")

# redis config
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
