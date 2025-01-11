# supabase_client.py
from supabase import create_client, Client
import os

SUPABASE_URL = "https://qgbyverabqyngxwtrqra.supabase.co"  # Replace with your Supabase URL
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def get_supabase_client() -> Client:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase
