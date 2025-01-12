import streamlit as st
from auth0_component import login_button
from auth import add_to_supabase

# Initialize session state variables if they don't exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None

class Login:
    @staticmethod
    def state():
        # Returns the current login state
        return st.session_state.logged_in

    @staticmethod
    def login():
        # Login logic using Auth0 component
        clientId = 'On2JJoTgtQVYaWxHvqxhn2LBBAwm6EqX'
        domain = 'dev-j3m4k7dwiqywttol.us.auth0.com'
        user_info = login_button(clientId=clientId, domain=domain)

        if user_info:
            st.session_state.logged_in = True
            st.session_state.user_info = user_info
            add_to_supabase(user_info)
            st.rerun()  # Refresh the app after login

    @staticmethod
    def display():
        # Display login/logout message based on the state
        if st.session_state.logged_in and st.session_state.user_info:
            pass
        else:
            st.write("Please log in to continue")
            Login.login()
