import streamlit as st
from pdf2image import convert_from_bytes
import time
import logging

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
            popup_placeholder = st.empty()
            completion_placeholder = st.empty()

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
                st.rerun()  # Rerun the app to switch to the upload page

            # Continuously update progress bar and time remaining text
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

                if elapsed_time >= st.session_state.target_time:
                    # Show popup completion message
                    popup_placeholder.markdown(
                        """
                        <div style="
                            position: fixed;
                            top: 20%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                            background-color: #d4edda;
                            color: #155724;
                            padding: 20px;
                            border-radius: 10px;
                            border: 2px solid #c3e6cb;
                            font-size: 24px;
                            font-weight: bold;
                            text-align: center;
                            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                            z-index: 1000;
                        ">
                            🎉 Congratulations! You have completed your reading session! 🎉
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.balloons()
                    st.markdown(
                        """
                        <div style='
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            background-color: #d4edda;
                            color: #155724;
                            padding: 20px;
                            border-radius: 10px;
                            border: 2px solid #c3e6cb;
                            font-size: 24px;
                            font-weight: bold;
                            text-align: center;
                            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                        '>
                            🎉 Reading session completed! Great job! You may return to the menu or attempt a quiz!
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    completion_placeholder.markdown(
                        f"<div style='text-align: center; font-size: 24px; font-weight: bold; color: #333;'>"
                        f"🎉 Reading session completed. Great job!</div>",
                        unsafe_allow_html=True
                    )
                    time.sleep(5)  # Display the popup for 5 seconds

                    # Replace the popup with a static completion message
                    popup_placeholder.empty()  # Remove the popup
                    break
                time.sleep(1)

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
