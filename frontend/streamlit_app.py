import streamlit as st
from login import Login

# Define pages for navigation
login_page = st.Page("login.py", title="Log in", icon=":material/login:")
logout_page = st.Page("logout.py", title="Log out", icon=":material/logout:")
lock_in_page = st.Page("pdfViewer.py", title="Focus Session", icon="🔒")
quiz_page = st.Page("questionViewer.py", title="Quiz", icon="📝")
leaderboard_page = st.Page("leaderboard.py", title="Leaderboard", icon="🏆")

# Check login state and display appropriate navigation
if Login.state():
    Login.display()  # Show user info if logged in
    pg = st.navigation({"Account": [logout_page], "Lock In": [lock_in_page, quiz_page], "Community": [leaderboard_page]})
else:
    Login.display()  # Show login prompt
    pg = st.navigation([login_page])

pg.run()
