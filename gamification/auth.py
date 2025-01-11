# auth.py
import streamlit as st
from gamification.supabase_client import get_supabase_client

def register():
    st.header("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    username = st.text_input("Username")
    
    if st.button("Register"):
        if email and password and username:
            supabase = get_supabase_client()
            try:
                user = supabase.auth.sign_up(email=email, password=password)
                # Insert into profiles table
                supabase.table('profiles').insert({
                    'id': user.user.id,
                    'username': username,
                    'points': 0,
                    'groups': []
                }).execute()
                st.success("Registration successful! Please log in.")
            except Exception as e:
                st.error(f"Registration failed: {e}")
        else:
            st.error("Please fill out all fields.")

# auth.py (continued)
def login():
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if email and password:
            supabase = get_supabase_client()
            try:
                user = supabase.auth.sign_in(email=email, password=password)
                if user.session:
                    st.session_state['user'] = user.user
                    st.success("Logged in successfully!")
                else:
                    st.error("Login failed. Check your credentials.")
            except Exception as e:
                st.error(f"Login failed: {e}")
        else:
            st.error("Please enter both email and password.")
