# points_management.py
import streamlit as st
from supabase_client import get_supabase_client

def add_points(user_id, points):
    supabase = get_supabase_client()
    supabase.table('profiles').update({'points': supabase.rpc('increment', {'value': points})}).eq('id', user_id).execute()

def deduct_points(user_id, points):
    supabase = get_supabase_client()
    supabase.table('profiles').update({'points': supabase.rpc('decrement', {'value': points})}).eq('id', user_id).execute()

def manage_points(user_id):
    st.header("Manage Points")
    
    action = st.selectbox("Select Action", ["Add Points", "Deduct Points"])
    points = st.number_input("Points", min_value=1, step=1)
    
    if st.button("Submit"):
        if action == "Add Points":
            add_points(user_id, points)
            st.success(f"Added {points} points to your account.")
        else:
            deduct_points(user_id, points)
            st.warning(f"Deducted {points} points from your account.")

