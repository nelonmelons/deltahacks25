# focus_session.py

import streamlit as st
from gamification.focus_detection_script import detect_focus, get_supabase_client
from gamification.points import add_points, deduct_points
from gamification.hardware_control import activate_water_gun, play_lock_message
import threading
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def monitor_focus_session(user_id, stop_event):
    """
    Monitors focus during a focus session.
    
    Args:
        user_id (str): The ID of the user.
        stop_event (threading.Event): Event to signal when to stop monitoring.
    """
    supabase = get_supabase_client()
    
    while not stop_event.is_set():
        focused = detect_focus()
        if focused:
            try:
                # Add points
                supabase.table('profiles').update({'points': supabase.rpc('increment', {'value': 10})}).eq('id', user_id).execute()
                st.session_state['last_focus'] = "Focused! +10 points"
                logging.info(f"User {user_id} is focused. Points incremented by 10.")
            except Exception as e:
                st.session_state['last_focus'] = "Error updating points."
                logging.error(f"Error incrementing points for user {user_id}: {e}")
        else:
            try:
                # Deduct points
                supabase.table('profiles').update({'points': supabase.rpc('decrement', {'value': 5})}).eq('id', user_id).execute()
                st.session_state['last_focus'] = "Distraction detected! -5 points"
                logging.info(f"User {user_id} is not focused. Points decremented by 5.")
                # Activate hardware controls
                activate_water_gun()
                play_lock_message()
                # Optionally, stop the focus session
                st.session_state['focus'] = False
                break
            except Exception as e:
                st.session_state['last_focus'] = "Error updating points."
                logging.error(f"Error decrementing points for user {user_id}: {e}")
        time.sleep(60)  # Check every minute

def focus_session(user_id):
    st.header("Focus Session")
    
    if 'focus' not in st.session_state:
        st.session_state['focus'] = False
    if 'focus_thread' not in st.session_state:
        st.session_state['focus_thread'] = None
    if 'stop_event' not in st.session_state:
        st.session_state['stop_event'] = None
    if 'last_focus' not in st.session_state:
        st.session_state['last_focus'] = ""
    
    if st.button("Start Focus Session"):
        if not st.session_state['focus']:
            st.session_state['focus'] = True
            st.session_state['stop_event'] = threading.Event()
            # Start monitoring in a separate thread
            focus_thread = threading.Thread(target=monitor_focus_session, args=(user_id, st.session_state['stop_event']))
            focus_thread.start()
            st.session_state['focus_thread'] = focus_thread
            st.success("Focus session started. Stay focused!")
    
    if st.session_state['focus']:
        st.write("Focus session is active.")
        st.write(st.session_state['last_focus'])
        if st.button("Stop Focus Session"):
            st.session_state['stop_event'].set()
            st.session_state['focus'] = False
            st.success("Focus session ended.")
    
    # Display current points
    supabase = get_supabase_client()
    try:
        user_profile = supabase.table('profiles').select('points').eq('id', user_id).single().execute()
        points = user_profile.data['points'] if user_profile.data else 0
    except Exception as e:
        logging.error(f"Error fetching points for user {user_id}: {e}")
        points = "Error"
    st.write(f"Current Points: {points}")


