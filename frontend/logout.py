import streamlit as st

# Logout logic
def logout():
    # Reset session state variables
    st.session_state.logged_in = False
    st.session_state.user_info = None
    
    # Display logout message
    st.success("You have been logged out.")
    
    # Redirect user back to the login screen
    st.rerun()

if "logged_in" in st.session_state and st.session_state.logged_in:
    user_name = st.session_state.user_info.get("name", "User")
    st.subheader(f"👋 Welcome, **{user_name}**!")
    st.write("You are logged in. Feel free to explore the app.")

# Log out button
if st.button("Log out"):
    logout()



