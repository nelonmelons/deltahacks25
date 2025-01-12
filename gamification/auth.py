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
                # Sign up the user
                user_response = supabase.auth.sign_up(email=email, password=password)
                
                if user_response and user_response.user:
                    # Insert into profiles table
                    profile_response = supabase.table('profiles').insert({
                        'id': user_response.user.id,          # Link profile to user ID
                        'username': username,
                        'points': 0,
                        'groups': []
                    }).execute()
                    
                    if profile_response.status_code == 201:
                        st.success("Registration successful! Please log in.")
                    else:
                        st.error("Failed to create user profile.")
                else:
                    st.error("Registration failed. Please try again.")
            except Exception as e:
                st.error(f"Registration failed: {e}")
        else:
            st.error("Please fill out all fields.")

def login():
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if email and password:
            supabase = get_supabase_client()
            try:
                # Use sign_in_with_password
                user_response = supabase.auth.sign_in_with_password(email=email, password=password)
                
                if user_response and user_response.user:
                    st.session_state['user'] = user_response.user
                    st.success("Logged in successfully!")
                else:
                    st.error("Login failed. Check your credentials.")
            except Exception as e:
                st.error(f"Login failed: {e}")
        else:
            st.error("Please enter both email and password.")
