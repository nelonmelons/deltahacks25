import streamlit as st
from supabase_client import get_supabase_client
import uuid
import json

def _fetch_user_groups(user_id: str):
    """
    Fetch the user's 'groups' array from the 'profiles' table.
    Each item is likely a JSON string representing a dict.
    Returns a list of strings or dicts (depending on how they're stored).
    """
    supabase = get_supabase_client()
    response = (
        supabase.table("profiles")
        .select("groups")
        .eq("id", user_id)
        .single()
        .execute()
    )

    if response.data and "groups" in response.data and response.data["groups"] is not None:
        return response.data["groups"]  # a list of strings or dicts
    return []


def _update_user_groups(user_id: str, new_groups: list):
    """
    Overwrite the user's 'groups' array with the 'new_groups' list.
    If 'new_groups' contains dicts, serialize them to JSON strings 
    before storing in a text[] column.
    """
    supabase = get_supabase_client()

    serialized = []
    for g in new_groups:
        if isinstance(g, dict):
            # Convert dict to JSON string
            g = json.dumps(g)
        # else assume it's already a string
        serialized.append(g)

    supabase.table("profiles").update({"groups": serialized}).eq("id", user_id).execute()


def create_group(group_name: str, creator_id: str) -> str:
    """
    Generate a new group (ID + name) and append it to the creator's 'groups'.
    Returns the newly created group_id.
    """
    group_id = str(uuid.uuid4())
    new_group_obj = {"id": group_id, "name": group_name}

    existing_groups = _fetch_user_groups(creator_id)
    # Convert any existing strings to dicts
    parsed_groups = []
    for g in existing_groups:
        if isinstance(g, str):
            try:
                g = json.loads(g)
            except json.JSONDecodeError:
                g = {}
        parsed_groups.append(g)

    parsed_groups.append(new_group_obj)
    _update_user_groups(creator_id, parsed_groups)

    return group_id


def join_group(group_id: str, user_id: str) -> bool:
    """
    Append a group (by ID) to user's 'groups' if not already joined.
    Return True if joined successfully, False if user was already in that group or invalid.
    """
    if not group_id:
        return False

    existing_groups = _fetch_user_groups(user_id)
    parsed_groups = []
    already_in_group = False

    for g in existing_groups:
        if isinstance(g, str):
            try:
                g_dict = json.loads(g)
            except json.JSONDecodeError:
                g_dict = {}
        else:
            g_dict = g

        if g_dict.get("id") == group_id:
            already_in_group = True
        parsed_groups.append(g_dict)

    if already_in_group:
        return False

    # We have no centralized place to fetch the real name, so store a placeholder
    new_group_obj = {"id": group_id, "name": "Joined Group"}
    parsed_groups.append(new_group_obj)
    _update_user_groups(user_id, parsed_groups)
    return True


def leave_group(group_id: str, user_id: str) -> bool:
    """
    Remove a group (by ID) from the user's 'groups' array.
    Return True if a group was removed, False if none found.
    """
    if not group_id:
        return False

    existing_groups = _fetch_user_groups(user_id)
    parsed_groups = []
    removed_something = False

    for g in existing_groups:
        if isinstance(g, str):
            try:
                g_dict = json.loads(g)
            except json.JSONDecodeError:
                g_dict = {}
        else:
            g_dict = g

        # Keep only groups that don't match group_id
        if g_dict.get("id") == group_id:
            removed_something = True
            continue  # skip adding to new list
        parsed_groups.append(g_dict)

    if removed_something:
        _update_user_groups(user_id, parsed_groups)

    return removed_something


def manage_groups(user_id: str):
    """
    Streamlit UI for managing groups in 'profiles'.
      - Create Group
      - Join Group
      - Leave Group
      - Display current groups
    """
    st.subheader("Manage Groups in 'profiles'")

    tab_create, tab_join, tab_leave = st.tabs(["Create Group", "Join Group", "Leave Group"])

    # 1. Create Group
    with tab_create:
        group_name = st.text_input("Enter a new group name", key="create_group_name")
        if st.button("Create Group", key="create_group_btn"):
            if group_name:
                group_id = create_group(group_name, user_id)
                st.success(f"Group '{group_name}' created with ID: {group_id}")
            else:
                st.error("Please enter a group name.")

    # 2. Join Group
    with tab_join:
        group_id_input = st.text_input("Enter a group ID to join", key="join_group_id")
        if st.button("Join Group", key="join_group_btn"):
            if group_id_input:
                success = join_group(group_id_input, user_id)
                if success:
                    st.success(f"Successfully joined group {group_id_input}")
                else:
                    st.warning("Either already joined or group ID is invalid.")
            else:
                st.error("Please enter a group ID.")

    # 3. Leave Group
    with tab_leave:
        group_id_leave = st.text_input("Enter a group ID to leave", key="leave_group_id")
        if st.button("Leave Group", key="leave_group_btn"):
            if group_id_leave:
                success = leave_group(group_id_leave, user_id)
                if success:
                    st.success(f"Successfully left group {group_id_leave}")
                else:
                    st.warning("No matching group found or invalid group ID.")
            else:
                st.error("Please enter a group ID.")

    # Display the user's current groups
    st.write("## Your Current Groups:")
    user_groups = _fetch_user_groups(user_id)

    for g in user_groups:
        # Convert from JSON string to dict
        if isinstance(g, str):
            try:
                g = json.loads(g)
            except json.JSONDecodeError:
                g = {"name": "Unparseable", "id": None}

        group_name = g.get("name", "Unnamed")
        group_id = g.get("id", "???")
        st.write(f"- **{group_name}** (ID: {group_id})")


def app():
    """
    This page can be called from your main Streamlit app.
    """
    st.set_page_config(page_title="Group Management", layout="centered")
    st.title("Group Management Page")

    # For demo, we hard-code a user ID. In real use, retrieve from st.session_state after login.
    user_id = '8e948565-82ec-44a3-9238-7652292d0a64'# this shit doesnt work so put in ur own user id for demoing

    manage_groups(user_id)


app()
