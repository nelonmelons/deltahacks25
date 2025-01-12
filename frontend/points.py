# points_management.py
import streamlit as st
from supabase_client import get_supabase_client

def add_points(nickname, points):
    supabase = get_supabase_client()
    # Fetch current points
    response = supabase.table('profiles').select('points').eq('username', nickname).single().execute()
    current_points = response.data['points']
    new_points = current_points + points
        # Update points
    update_response = supabase.table('profiles').update({'points': new_points}).eq('username', nickname).execute()


def deduct_points(user_id, points):
    supabase = get_supabase_client()
    # Fetch current points
    response = supabase.table('profiles').select('points').eq('id', user_id).single().execute()
    if response.status_code == 200:
        current_points = response.data['points']
        new_points = max(current_points - points, 0)  # Prevent negative points
        # Update points
        update_response = supabase.table('profiles').update({'points': new_points}).eq('id', user_id).execute()
        if update_response.status_code == 200:
            st.warning(f"Deducted {points} points.")
        else:
            st.error("Failed to update points.")
    else:
        st.error("User profile not found.")

def manage_points(user_id):
    st.header("Manage Points")
    
    action = st.selectbox("Select Action", ["Add Points", "Deduct Points"])
    points = st.number_input("Points", min_value=1, step=1)
    
    if st.button("Submit"):
        if action == "Add Points":
            add_points(user_id, points)
        else:
            deduct_points(user_id, points)

if __name__ == "__main__":
    add_points("liurnicole", 10)
