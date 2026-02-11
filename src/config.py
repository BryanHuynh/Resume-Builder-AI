from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

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

# SUPABASE
SUPABASE_USER= os.getenv("SUPABASE_USER", None)
SUPABASE_PASSWORD=os.getenv("SUPABASE_PASSWORD", None)
SUPABASE_HOST=os.getenv("SUPABASE_HOST", None)
SUPABASE_PORT=os.getenv("SUPABASE_PORT", None)
SUPABASE_DBNAME=os.getenv("SUPABASE_DBNAME", None)

assert SUPABASE_USER is not None, "SUPABASE_USER must be set"
assert SUPABASE_PASSWORD is not None, "SUPABASE_PASSWORD must be set"
assert SUPABASE_HOST is not None, "SUPABASE_HOST must be set"
assert SUPABASE_PORT is not None, "SUPABASE_PORT must be set"
assert SUPABASE_DBNAME is not None, "SUPABASE_DBNAME must be set"

