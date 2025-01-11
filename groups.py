# group_management.py
import streamlit as st
from supabase_client import get_supabase_client
import uuid

def create_group(group_name, creator_id):
    supabase = get_supabase_client()
    group_id = str(uuid.uuid4())
    supabase.table('groups').insert({
        'id': group_id,
        'group_name': group_name,
        'members': [creator_id],
        'group_points': 0,
        'created_at': 'now()'
    }).execute()
    
    # Update user's group list
    supabase.table('profiles').update({'groups': {'append': [group_id]}}).eq('id', creator_id).execute()
    return group_id

def join_group(group_id, user_id):
    supabase = get_supabase_client()
    group = supabase.table('groups').select('*').eq('id', group_id).single().execute()
    if group.data:
        supabase.table('groups').update({'members': {'append': [user_id]}}).eq('id', group_id).execute()
        supabase.table('profiles').update({'groups': {'append': [group_id]}}).eq('id', user_id).execute()
        return True
    else:
        return False

def manage_groups(user_id):
    st.header("Manage Groups")
    
    sub_menu = st.selectbox("Select Option", ["Create Group", "Join Group"])
    
    if sub_menu == "Create Group":
        group_name = st.text_input("Group Name")
        if st.button("Create"):
            if group_name:
                group_id = create_group(group_name, user_id)
                st.success(f"Group '{group_name}' created with ID: {group_id}")
            else:
                st.error("Please enter a group name.")
    
    elif sub_menu == "Join Group":
        group_id = st.text_input("Group ID")
        if st.button("Join"):
            if group_id:
                success = join_group(group_id, user_id)
                if success:
                    st.success(f"Joined group {group_id} successfully.")
                else:
                    st.error("Group not found.")
            else:
                st.error("Please enter a group ID.")
