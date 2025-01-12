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
    """Initialize the start time in session state."""
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

def get_elapsed_time():
    """Calculate elapsed time since the start of the session."""
    return int(time.time() - st.session_state.start_time)

# Initialize session state variables
if 'app_state' not in st.session_state:
    st.session_state.app_state = "upload"  # Start at the upload page

if 'pdf_bytes' not in st.session_state:
    st.session_state.pdf_bytes = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = 1


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
        st.session_state.app_state = "read"  # Automatically transition to reading mode
        st.session_state.start_time = time.time()  # Start timer
        st.rerun()  # Rerun the app to switch to the reading page

     # Add a clickable icon to redirect to the read page
    if st.button("🔍 Go to Read Page", key="read_page_icon"):
        if st.session_state.pdf_bytes:
            st.session_state.app_state = "read"
            st.rerun()

def read_page():
    """Page for reading PDF."""
    pdf_bytes = st.session_state.get('pdf_bytes')

    if pdf_bytes:
        try:
            # Convert PDF to images
            images = convert_from_bytes(pdf_bytes)

            # Start timer if not already started
            start_timer()

            # Timer placeholder at the top
            timer_placeholder = st.empty()

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
            if st.button("Go Back", key="go_back_button"):
                st.session_state.app_state = "upload"
                st.session_state.pdf_bytes = None
                st.session_state.current_page = 1
                st.rerun()  # Rerun the app to switch to the upload page

            # Continuously update timer at the top
            while True:
                elapsed_time = get_elapsed_time()
                timer_placeholder.markdown(f"### ⏱️ Time spent on document: {elapsed_time} seconds")
                time.sleep(1)
           
        except Exception as e:
            st.error("An error occurred while processing the PDF.")
            st.exception(e)
    else:
        st.error("No PDF file loaded. Please upload a PDF file on the main page.")
    

# Page routing
if st.session_state.app_state == "upload":
    upload_page()
elif st.session_state.app_state == "read":
    read_page()
