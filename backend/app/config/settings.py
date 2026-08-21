import os
from dotenv import load_dotenv

load_dotenv()

SOCIALCRAWL_API_KEY = os.getenv("SOCIALCRAWL_API_KEY")

SOCIALCRAWL_BASE_URL = "https://www.socialcrawl.dev/v1"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")

SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SOCIALCRAWL_API_KEY:
    raise ValueError("SOCIALCRAWL_API_KEY is missing from .env")


if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing from .env")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is missing from .env")
