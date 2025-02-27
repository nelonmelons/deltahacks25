# leaderboard.py
import streamlit as st
from gamification.supabase_client import get_supabase_client
import pandas as pd

def display_leaderboard():
    st.header("Leaderboard")
    supabase = get_supabase_client()
    
    # Fetch top 10 users by points
    response = supabase.table('profiles').select('username, points').order('points', desc=True).limit(10).execute()
    data = response.data
    
    if data:
        df = pd.DataFrame(data)
        st.table(df)
    else:
        st.write("No data available.")
