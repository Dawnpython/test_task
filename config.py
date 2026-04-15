import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
RETAIL_SUBDOMEN = os.getenv("RETAIL_SUBDOMEN")
RETAIL_API = os.getenv("RETAIL_API")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API = os.getenv("SUPABASE_API")