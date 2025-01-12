# group_leaderboard.py
import streamlit as st
import pandas as pd
import json
from supabase_client import get_supabase_client

def display_group_leaderboard(group_id: str):
    """
    1. Fetch all rows from 'profiles' (or at least the columns we need).
    2. For each user, parse the JSON strings in the 'groups' array.
    3. Keep the user if any group JSON has the matching group_id.
    4. Sort by 'points' descending and display as a leaderboard.
    """
    st.header(f"Group Leaderboard: {group_id}")
    supabase = get_supabase_client()

    # 1) Fetch all profiles (id, username, points, groups).
    response = (
        supabase.table("profiles")
        .select("id, username, points, groups")
        .execute()
    )

    if not response.data:
        st.write("No profiles found.")
        return

    all_profiles = response.data  # list of dicts

    # 2) Filter in Python
    matching_profiles = []
    for profile in all_profiles:
        user_groups = profile.get("groups", [])
        if not user_groups:
            continue
        
        # Parse each JSON string in user_groups
        found = False
        for g_str in user_groups:
            try:
                group_dict = json.loads(g_str)  # convert JSON string -> dict
            except json.JSONDecodeError:
                continue

            if group_dict.get("id") == group_id:
                found = True
                break
        
        if found:
            matching_profiles.append(profile)

    # 3) Sort matching profiles by 'points' desc
    matching_profiles.sort(key=lambda p: p.get("points", 0), reverse=True)

    # 4) Display result
    if matching_profiles:
        df = pd.DataFrame(matching_profiles)
        st.table(df[["username", "points"]])
    else:
        st.write("No profiles matched this group ID.")

def app():
    st.set_page_config(page_title="Group Leaderboard", layout="centered")
    st.title("Group Leaderboard (Client-side Filtering)")

    # Example usage: user inputs a group ID, we show the leaderboard
    group_id_input = st.text_input("Enter Group ID to view leaderboard")
    if st.button("Show Leaderboard"):
        if group_id_input:
            display_group_leaderboard(group_id_input)
        else:
            st.error("Please enter a valid Group ID.")


app()
