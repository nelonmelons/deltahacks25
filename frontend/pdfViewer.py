import streamlit as st
from pdf2image import convert_from_bytes
import time
import logging
import cv2
import base64
import threading
import queue

from cam.gaze_tracking.gaze_tracking import GazeTracking


# Suppress terminal messages
logging.getLogger("streamlit").setLevel(logging.ERROR)

# Streamlit app configuration
st.set_page_config(page_title="PDF Viewer", layout="wide")

# Helper functions
def start_timer():
    """Initialize the start time and target time in session state."""
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

def get_elapsed_time():
    """Calculate elapsed time since the start of the session."""
    return int(time.time() - st.session_state.start_time)

def get_progress():
    """Calculate progress towards the target time."""
    elapsed_time = get_elapsed_time()
    progress = min(1.0, elapsed_time / st.session_state.target_time) if st.session_state.target_time > 0 else 0
    return progress, elapsed_time

# Initialize session state variables
if 'app_state' not in st.session_state:
    st.session_state.app_state = "upload"  # Start at the upload page

if 'pdf_bytes' not in st.session_state:
    st.session_state.pdf_bytes = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

if 'target_time' not in st.session_state:
    st.session_state.target_time = 0  # Target time in seconds


# App workflow
def upload_page():
    """Page for uploading PDF."""
    st.title("📄 PDF Viewer")

    # File upload
    st.subheader("Upload Your PDF File:")
    uploaded_file = st.file_uploader("", type=["pdf"], help="Drag and drop a PDF file or browse to upload.", key="file_uploader")

    if uploaded_file:
        # Save PDF data in session state
        st.session_state.pdf_bytes = uploaded_file.read()
        st.session_state.app_state = "time_setting"  # Transition to the time setting screen
        st.rerun()  # Rerun the app to switch to the time setting page


def time_setting_page():
    """Page for specifying reading time."""
    st.title("⏰ Set Reading Duration")

    # Time input fields
    col1, col2, col3 = st.columns(3)
    with col1:
        hours = st.number_input("Hours:", min_value=0, value=0, step=1)
    with col2:
        minutes = st.number_input("Minutes:", min_value=0, value=0, step=1)
    with col3:
        seconds = st.number_input("Seconds:", min_value=0, value=10, step=1)

    # Calculate total time in seconds
    total_time_seconds = hours * 3600 + minutes * 60 + seconds

    # Proceed button
    if st.button("Start Reading"):
        if total_time_seconds > 0:
            st.session_state.target_time = total_time_seconds
            st.session_state.app_state = "read"  # Transition to reading mode
            st.session_state.start_time = time.time()  # Start the timer
            st.rerun()
        else:
            st.error("Please specify a valid reading duration (greater than 0).")

# Threaded webcam capture
def start_webcam_feed(webcam_queue, locking_in=True):

    ongaze=0
    offgaze=0
    absgaze=0

    face_away=0
    face_towards=0

    focuspercent=0
    distractedpercent=0
    abspercent=0
    onscreen=0
    offscreen=0
    onscreenpercent=0
    offscreenpercent=0
    maxpresence=0

    gaze = GazeTracking()
    cap = cv2.VideoCapture(0)  # Open the webcam
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    while locking_in:
        ret, frame_color_to_send = cap.read()
        if ret:
            _, encoded_image = cv2.imencode('.jpg', frame_color_to_send)
            img_base64 = base64.b64encode(encoded_image.tobytes()).decode('utf-8')
            if not webcam_queue.full():
                webcam_queue.put(img_base64)
            # Convert BGR to RGB for correct color representation

            
            gaze.refresh(frame_color_to_send)
            frame = gaze.annotated_frame()
            
            # use grayscale for faster processing
            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            except cv2.error as e:
                logging.error(f"Error converting frame from BGR to RGB: {e}")
                continue
            
            text = ""

            vertical_c = gaze.vertical_ratio()
            horizontal_c = gaze.horizontal_ratio()
            
            if vertical_c is None or horizontal_c is None:
                text = "Eyes not detected"
                absgaze += 1
            elif vertical_c<=0.4 or vertical_c>=0.6 or horizontal_c<=0.44 or horizontal_c>=0.74:
                text = "Eyes not paying attention"
                offgaze += 1
            else:
                text = "Eyes paying attention"
                ongaze += 1

            angle_from_vertical = gaze.get_head_pose_direction(gray, draw_line = True)

            if angle_from_vertical > 60 and angle_from_vertical < 95:
                face_direction = "Right"
                face_away += 1
            elif angle_from_vertical < -60:
                face_direction = "Left"
                face_away += 1
            elif angle_from_vertical  == 100:
                face_direction = "No face detected"
                face_away += 1
            else:
                face_direction = "Center"
                face_towards += 1

            # detect face(s)
            sum_gaze=ongaze+offgaze+absgaze
            eye_forward_percent=round((ongaze * 100 / sum_gaze),2) if sum_gaze != 0 else 100
            
            sum_direction = face_away + face_towards
            face_towards_percent=round((face_towards*100/sum_direction),2) if sum_direction != 0 else 100
            
            print(f'Eye gaze: {text}, face direction: {face_direction}')
            
            

        time.sleep(0.1)  # Limit frame rate to 10 FPS
    cap.release()

# Initialize webcam thread and queue
if "webcam_queue" not in st.session_state:
    st.session_state.webcam_queue = queue.Queue(maxsize=1)  # Hold only the latest frame
    webcam_thread = threading.Thread(target=start_webcam_feed, args=(st.session_state.webcam_queue,), daemon=True)
    webcam_thread.start()

def read_page():
    """Page for reading PDF."""
    pdf_bytes = st.session_state.get('pdf_bytes')

    if pdf_bytes:
        try:
            # Convert PDF to images
            images = convert_from_bytes(pdf_bytes)

            # Start timer if not already started
            start_timer()

            # Timer and progress bar placeholders
            progress_placeholder = st.empty()
            time_placeholder = st.empty()
            webcam_placeholder = st.empty()
            popup_placeholder = st.empty()

            # Navigation and display
            st.title("📖 PDF Reading Session")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("Previous", key="previous_button"):
                    st.session_state.current_page = max(1, st.session_state.current_page - 1)
            with col3:
                if st.button("Next", key="next_button"):
                    st.session_state.current_page = min(len(images), st.session_state.current_page + 1)

            # Scrollable bar for navigation
            st.session_state.current_page = st.slider(
                "Navigate Pages",
                1,
                len(images),
                st.session_state.current_page,
                key="page_slider"
            )

            # Display current page
            current_page = st.session_state.current_page
            st.image(images[current_page - 1], use_container_width=True)
            st.markdown(f"<div style='text-align: center; font-size: 18px; font-weight: bold;'>Page {current_page}</div>", unsafe_allow_html=True)

            # Go Back button
            if st.button("Return to Menu", key="go_back_button"):
                st.session_state.app_state = "upload"
                st.session_state.pdf_bytes = None
                st.session_state.current_page = 1
                st.session_state.target_time = 0
                st.rerun()

            # Continuously update progress bar, time remaining, and webcam feed
            while True:
                progress, elapsed_time = get_progress()
                remaining_time = max(0, st.session_state.target_time - elapsed_time)

                # Formatting the time remaining message
                mins, secs = divmod(remaining_time, 60)
                hrs, mins = divmod(mins, 60)
                formatted_time = f"{hrs:02d}:{mins:02d}:{secs:02d}"

                # Display progress bar
                progress_placeholder.progress(
                    progress,
                    text=f"⏳ Progress towards target"
                )

                # Display large time remaining text
                time_placeholder.markdown(
                    f"<div style='text-align: center; font-size: 36px; font-weight: bold; color: #333;'>"
                    f"⏳ Time remaining: {formatted_time}</div>",
                    unsafe_allow_html=True
                )

                # Update webcam feed
                if not st.session_state.webcam_queue.empty():
                    img_base64_str = st.session_state.webcam_queue.get()
                    webcam_placeholder.markdown(
                        f"""
                        <div style="
                            position: fixed;
                            bottom: 3%;
                            right: 1%;
                            background-color: #f9f9f9;
                            color: #333;
                            padding: 10px;
                            border-radius: 10px;
                            border: 2px solid #ddd;
                            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                            z-index: 1000;
                            text-align: center;
                            width: 280px;
                            height: 210px;
                            overflow: hidden;
                        ">
                            <img src="data:image/jpeg;base64,{img_base64_str}" 
                                style="width: 100%; height: auto; border-radius: 5px;" />
                            <div style="font-size: 14px; margin-top: 5px;">📷 Webcam Feed</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                if elapsed_time >= st.session_state.target_time:
                    # Display completion popup
                    popup_placeholder.markdown(
                        """
                        <div style="text-align: center; font-size: 24px; font-weight: bold; color: #155724;">
                            🎉 Congratulations! You have completed your reading session!
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.balloons()
                    break
                time.sleep(0.1)  # Adjust loop frequency

        except Exception as e:
            st.error("An error occurred while processing the PDF.")
            st.exception(e)
    else:
        st.error("No PDF file loaded. Please upload a PDF file on the main page.")

# Page routing
if st.session_state.app_state == "upload":
    upload_page()
elif st.session_state.app_state == "time_setting":
    time_setting_page()
elif st.session_state.app_state == "read":
    read_page()
