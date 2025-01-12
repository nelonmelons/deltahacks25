# group_leaderboard.py
import streamlit as st
import pandas as pd
from supabase_client import get_supabase_client

def display_group_leaderboard(group_id: str):
    """
    Displays a leaderboard for the given group_id, assuming:
    1. The 'profiles' table has columns: id, username, points, groups (text[]).
    2. A user belongs to a group if 'group_id' is in their 'groups' array.
    """

    st.header(f"Group Leaderboard: {group_id}")
    supabase = get_supabase_client()

    # Query 'profiles' for all users where 'groups' array contains group_id
    # The supabase-py call for "contains" is .cs() with an array of values.
    # e.g.: .cs("groups", [group_id]) checks if group_id is in the text[] column "groups".
    response = (
        supabase.table("profiles")
        .select("username, points")
        .cs("groups", [group_id])  # .cs() means "column contains all elements in [group_id]"
        .order("points", desc=True)
        .execute()
    )

    data = response.data
    if data and len(data) > 0:
        # Convert to DataFrame for nice display
        df = pd.DataFrame(data)
        st.table(df)
    else:
        st.warning("No members found for this group ID or none have points yet.")

def app():
    """
    This Streamlit page can be referenced by your main script, or run directly via:
        streamlit run group_leaderboard.py
    """
    st.set_page_config(page_title="Group Leaderboard", layout="centered")
    st.title("Group Leaderboard")

    # Example usage: prompt user for a group_id, then display the leaderboard
    group_id_input = st.text_input("Enter Group ID to view leaderboard")
    if st.button("Show Leaderboard"):
        if group_id_input:
            display_group_leaderboard(group_id_input)
        else:
            st.error("Please enter a valid Group ID.")

if __name__ == "__main__":
    app()
