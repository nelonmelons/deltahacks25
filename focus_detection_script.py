# focus_detection_script.py
from supabase_client import get_supabase_client
from hardware_control import activate_water_gun, play_lock_message
import time

def monitor_focus(user_id):
    supabase = get_supabase_client()
    
    while True:
        focused = detect_focus(user_id)  # Your existing focus detection function
        if focused:
            supabase.table('profiles').update({'points': supabase.rpc('increment', {'value': 10})}).eq('id', user_id).execute()
        else:
            supabase.table('profiles').update({'points': supabase.rpc('decrement', {'value': 5})}).eq('id', user_id).execute()
            activate_water_gun()
            play_lock_message()
        time.sleep(900)  # Check every 15 minutes

if __name__ == "__main__":
    user_id = "user-uuid"  # Replace with actual user ID
    monitor_focus(user_id)
