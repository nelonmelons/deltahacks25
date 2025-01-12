import streamlit as st

st.write("Hello World")
st.write(f'**Username:** {st.session_state.user_info["nickname"]}')