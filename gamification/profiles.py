# profiles.py
import streamlit as st
from gamification.supabase_client import get_supabase_client

def get_user_profile(user_id):
    supabase = get_supabase_client()
    response = supabase.table('profiles').select('*').eq('id', user_id).single().execute()
    if response.status_code == 200 and response.data:
        return response.data
    else:
        return None

def display_profile(user_id):
    profile = get_user_profile(user_id)
    if profile:
        st.write(f"**Username:** {profile['username']}")
        st.write(f"**Points:** {profile['points']}")
        st.write(f"**Groups:** {', '.join(profile['groups']) if profile['groups'] else 'None'}")
    else:
        st.error("Profile not found.")
