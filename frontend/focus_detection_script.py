# focus_detection_script.py

from supabase_client import get_supabase_client
from cam.eyegaze_cam import eyegaze
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def detect_focus():
    """
    Determines if the user is focused based on eyegaze data.
    
    Returns:
        bool: True if focused, False otherwise.
    """
    try:
        eyegaze_data = eyegaze.get_eyegaze_data()
        text, face_direction = eyegaze_data

        logging.debug(f"Eyegaze Data - Text: {text}, Face Direction: {face_direction}")

        # Define focus criteria
        if text == "Eyes paying attention" and face_direction == "Center":
            logging.debug("User is focused.")
            return True
        else:
            logging.debug("User is not focused.")
            return False
    except Exception as e:
        logging.error(f"Error in detect_focus: {e}")
        return False

def monitor_focus(user_id):
    supabase = get_supabase_client()
    
    while True:
        focused = detect_focus()
        if focused:
            try:
                # Increment points by 10
                supabase.table('profiles').update({'points': supabase.rpc('increment', {'value': 10})}).eq('id', user_id).execute()
                logging.info(f"User {user_id} is focused. Points incremented by 10.")
            except Exception as e:
                logging.error(f"Error incrementing points for user {user_id}: {e}")
        else:
            try:
                # Decrement points by 5
                supabase.table('profiles').update({'points': supabase.rpc('decrement', {'value': 5})}).eq('id', user_id).execute()
                logging.info(f"User {user_id} is not focused. Points decremented by 5.")
                # Optionally, activate hardware controls here or handle in another script
                # activate_water_gun()
                # play_lock_message()
            except Exception as e:
                logging.error(f"Error decrementing points for user {user_id}: {e}")
        time.sleep(900)  # Check every 15 minutes


