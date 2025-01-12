# app.py
import streamlit as st
# from gamification.auth import login, register
# from gamification.leaderboard import display_leaderboard
# from gamification.groupleaderboard import display_group_leaderboard
# from gamification.points import manage_points
# from gamification.groups import manage_groups
# from gamification.focus_session import focus_session
# from gamification.questions import questions
# from gamification.supabase_client import get_supabase_client
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



    # st.write(user_info)
    # # Authentication
    # if 'user' not in st.session_state:
    #     menu = ["Login", "Register"]
    #     choice = st.sidebar.selectbox("Authentication", menu)
        
    #     if choice == "Login":
    #         login()
    #     elif choice == "Register":
    #         register()
    # else:
    #     menu = ["Home", "Leaderboard", "Groups", "Take Quiz", "Focus Session", "Manage Points", "Logout"]
    #     choice = st.sidebar.selectbox("Menu", menu)
        
    #     if choice == "Home":
    #         st.write(f"Welcome, {st.session_state['user'].email}! Stay focused and climb the leaderboard.")
        
    #     elif choice == "Leaderboard":
    #         display_leaderboard()
        
    #     elif choice == "Groups":
    #         manage_groups(st.session_state['user'].id)
    #         # You can list user's groups and allow selecting which to view
    #         # display_group_leaderboard(group_id="")  # Modify to display user’s groups
        
    #     elif choice == "Take Quiz":
    #         questions(st.session_state['user'].id)
        
    #     elif choice == "Focus Session":
    #         focus_session(st.session_state['user'].id)
        
    #     elif choice == "Manage Points":
    #         manage_points(st.session_state['user'].id)
        
    #     elif choice == "Logout":
    #         supabase = get_supabase_client()
    #         supabase.auth.sign_out()
    #         del st.session_state['user']
    #         st.success("Logged out successfully!")
        
if __name__ == "__main__":
    main()
