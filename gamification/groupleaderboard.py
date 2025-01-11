# group_leaderboard.py
import streamlit as st
from gamification.supabase_client import get_supabase_client
import pandas as pd

def display_group_leaderboard(group_id):
    st.header(f"Group Leaderboard: {group_id}")
    supabase = get_supabase_client()
    
    group = supabase.table('groups').select('*').eq('id', group_id).single().execute()
    if group.data:
        member_ids = group.data['members']
        # Supabase doesn't support 'in' queries with more than 10 items. Handle accordingly.
        response = supabase.table('profiles').select('username, points').in_('id', member_ids).order('points', desc=True).execute()
        data = response.data
        
        if data:
            df = pd.DataFrame(data)
            st.table(df)
        else:
            st.write("No members in this group.")
    else:
        st.error("Group not found.")
