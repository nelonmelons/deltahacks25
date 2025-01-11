# profiles.py
import streamlit as st
from gamification.supabase_client import get_supabase_client

def view_profile(user_id):
    supabase = get_supabase_client()
    profile = supabase.table('profiles').select('*').eq('id', user_id).single().execute()
    if profile.data:
        st.write(f"**Username:** {profile.data['username']}")
        st.write(f"**Points:** {profile.data['points']}")
        st.write(f"**Groups:** {', '.join(profile.data['groups']) if profile.data['groups'] else 'None'}")
    else:
        st.error("Profile not found.")
