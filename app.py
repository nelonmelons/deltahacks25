# app.py
import streamlit as st
from frontend.auth import login, register
from frontend.leaderboard import display_leaderboard
from frontend.groupleaderboard import display_group_leaderboard
from frontend.points import manage_points
from frontend.groups import manage_groups
# from frontend.pdfViewer import view_pdf_focus_session
from frontend.focus_session import focus_session
from frontend.questions import questions
from frontend.supabase_client import get_supabase_client
import os
from auth0_component import login_button

import dotenv



def main():

    dotenv.load_dotenv()
    clientId = 'On2JJoTgtQVYaWxHvqxhn2LBBAwm6EqX'
    domain = 'dev-j3m4k7dwiqywttol.us.auth0.com'


    st.title("Focus and Productivity App")

    user_info = login_button(clientId = clientId, domain = domain)

    if user_info:
        st.write(f'Hi {user_info["nickname"]}')
        # st.write(user_info) # some private information here
            
    if not user_info:
        st.write("Please login to continue")


    
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
        # view_pdf_focus_session()
    
    elif choice == "Manage Points":
        manage_points(st.session_state['user'].id)
    
    elif choice == "Logout":
        supabase = get_supabase_client()
        supabase.auth.sign_out()
        del st.session_state['user']
        st.success("Logged out successfully!")

if __name__ == "__main__":
    main()
