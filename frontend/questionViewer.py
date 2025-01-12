import streamlit as st
from questionDriver import QuestionDriver as qd
from questionGenerator import QuestionGenerator as qg
import serial
import time

arduino = serial.Serial(port='/dev/tty.usbmodemF412FA652F7C2', baudrate=9600, timeout=1)  # Replace 'COM4' with your Arduino's port


def send_command(command):
    """Send a command to the Arduino."""
    if arduino:
        arduino.write((command + '\n').encode())  # Send command as bytes
        time.sleep(0.1)  # Give Arduino time to process
        print(f"Command '{command}' sent to Arduino!")

# App layout
st.title("Quiz Application")

# Session state to track user input for the subject
if "quiz_subject" not in st.session_state:
    st.session_state.quiz_subject = None

# Step 1: Get the subject of the quiz
if st.session_state.quiz_subject is None:
    st.header("Enter the Subject of the Quiz")
    subject = st.text_input("Subject:", placeholder="e.g., Calculus, History, Physics")
    generate_quiz_button = st.button("Generate Quiz")

    if generate_quiz_button and subject.strip():
        st.session_state.quiz_subject = subject
        # Generate questions based on the entered subject
        st.session_state.quiz_text = qg.questions(subject)
        st.session_state.driver = qd(st.session_state.quiz_text)
        st.rerun()
else:
    # Step 2: Initialize Question Driver
    driver = st.session_state.driver

    # Ensure the driver is initialized
    if driver is None or not driver.questions:
        st.error("Failed to generate quiz questions. Please restart the app and try again.")
        st.stop()

    # Proceed with the quiz
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "feedback" not in st.session_state:
        st.session_state.feedback = ""

    # Check if all questions are answered
    if st.session_state.current_question >= len(driver.questions):
        st.markdown(f"## Quiz Complete! 🎉\nYour score: **{st.session_state.score}/{len(driver.questions)}**")
    else:
        # Fetch the current question
        current_question_index = st.session_state.current_question
        current_question = driver.questions[current_question_index]

        # Display the current question
        st.markdown(f"### Question {current_question_index + 1}: {current_question.title}")

        # Render choices as radio buttons
        user_answer = st.radio(
            "Select your answer:",
            options=list(current_question.choices.keys()),
            format_func=lambda x: f"**{x})** {current_question.choices[x]}",
            key=f"q{current_question_index}_answer",
            disabled=st.session_state.answered  # Disable radio buttons after answering
        )

        # Submit Answer Button (disabled after answering)
        submit_button = st.button("Submit Answer", disabled=st.session_state.answered)
        if submit_button and not st.session_state.answered:
            st.session_state.answered = True
            if current_question.is_correct(user_answer):
                st.session_state.feedback = "✅ Correct!"
                st.session_state.score += 1
                send_command("toggle_sweeper")
                st.rerun()
            else:
                st.session_state.feedback = f"❌ Incorrect. The correct answer is **{current_question.correct_choice}) {current_question.choices[current_question.correct_choice]}**."
                send_command("true")
                st.rerun()

        # Display feedback after answering
        if st.session_state.answered:
            if "Correct!" in st.session_state.feedback:
                st.markdown(
                    f"<div style='background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px; border: 1px solid #c3e6cb; font-size: 18px; font-weight: bold; text-align: center;'>{st.session_state.feedback}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; border: 1px solid #f5c6cb; font-size: 18px; font-weight: bold; text-align: center;'>{st.session_state.feedback}</div>",
                    unsafe_allow_html=True
                )

        # Add spacing between feedback and the "Next Question" button
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        # Show the "Next Question" button after answering
        if st.session_state.answered:
            if current_question_index < len(driver.questions) - 1:
                if st.button("Next Question"):
                    st.session_state.current_question += 1
                    st.session_state.answered = False
                    st.session_state.feedback = ""  # Clear feedback for the next question
                    st.rerun()  # Reload for the next question
            else:  # Last question
                if st.button("Finish Quiz"):
                    st.session_state.current_question += 1
                    st.session_state.answered = False
                    st.session_state.feedback = ""  # Clear feedback for the next question
                    st.rerun()

    # Exit Quiz Button (always available at the bottom)
    if st.button("Exit Quiz"):
        # Clear session state to reset the app
        for key in ["quiz_subject", "quiz_text", "driver", "current_question", "score", "answered", "feedback"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# if arduino:
#     arduino.close()
