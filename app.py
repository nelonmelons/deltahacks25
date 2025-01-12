# app.py
import streamlit as st
from gamification.auth import login, register
from gamification.leaderboard import display_leaderboard
from gamification.groupleaderboard import display_group_leaderboard
from gamification.points import manage_points
from gamification.groups import manage_groups
from gamification.focus_session import focus_session
from gamification.questions import questions
from gamification.supabase_client import get_supabase_client
import os
from auth0_component import login_button

import dotenv



def main():

    dotenv.load_dotenv()
    clientId = 'On2JJoTgtQVYaWxHvqxhn2LBBAwm6EqX'
    domain = 'dev-j3m4k7dwiqywttol.us.auth0.com'


    st.title("Focus and Productivity App")
    
    # Bypass login with a test user
    if 'user' not in st.session_state:
        class User:
            def __init__(self, id):
                self.id = id
        st.session_state['user'] = User(id="test_user_id")
    
    menu = ["Home", "Leaderboard", "Groups", "Take Quiz", "Focus Session", "Manage Points", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        st.write("### Welcome!")
    
    elif choice == "Leaderboard":
        display_leaderboard()
    
    elif choice == "Groups":
        manage_groups(st.session_state['user'].id)
        # Optionally, display group leaderboards here
    
    elif choice == "Take Quiz":
        questions(st.session_state['user'].id)
    
    elif choice == "Focus Session":
        focus_session(st.session_state['user'].id)
    
    elif choice == "Manage Points":
        manage_points(st.session_state['user'].id)
    
    elif choice == "Logout":
        supabase = get_supabase_client()
        supabase.auth.sign_out()
        del st.session_state['user']
        st.success("Logged out successfully!")

if __name__ == "__main__":
    main()
