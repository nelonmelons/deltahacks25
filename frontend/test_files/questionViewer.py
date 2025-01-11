import streamlit as st
import questionDriver as qd
import questionGenerator as qg

text = "### Question 1: Limits and Continuity\n**Question:** What is the formal definition of the limit as \\( x \\) approaches \\( a \\), denoted as \\( \\lim_{x \\to a} f(x) \\)?\n\n**A)** \\( f(a) = L \\)\n\n**B)** \\( \\forall \\epsilon > 0, \\exists \\delta > 0 \\) such that \\( |f(x) - L| < \\epsilon \\) whenever \\( |x - a| < \\delta \\)\n\n**C)** \\( f(x) = L \\)\n\n**D)** \\( f(a) = L \\) and \\( f(x) = L \\)\n\n**Correct Answer:** B) \\( \\forall \\epsilon > 0, \\exists \\delta > 0 \\) such that \\( |f(x) - L| < \\epsilon \\) whenever \\( |x - a| < \\delta \\)\n\n### Question 2: Differentiability\n**Question:** State the definition of a function \\( f \\) being differentiable at a point \\( a \\).\n\n**A)** \\( f(a) = 0 \\)\n\n**B)** \\( f'(a) = \\lim_{h \\to 0} \\frac{f(a + h) - f(a)}{h} \\)\n\n**C)** \\( f(a) = L \\)\n\n**D)** \\( f'(a) = L \\)\n\n**Correct Answer:** B) \\( f'(a) = \\lim_{h \\to 0} \\frac{f(a + h) - f(a)}{h} \\)\n\n### Question 3: Intermediate Value Theorem\n**Question:** State the Intermediate Value Theorem.\n\n**A)** If a function \\( f \\) is continuous on the interval \\( [a, b] \\) and \\( k \\) is any number between \\( f(a) \\) and \\( f(b) \\), then there exists a number \\( c \\) in \\( [a, b] \\) such that \\( f(c) = k \\).\n\n**B)** If a function \\( f \\) is differentiable on the interval \\( [a, b] \\) and \\( k \\) is any number between \\( f(a) \\) and \\( f(b) \\), then there exists a number \\( c \\) in \\( [a, b] \\) such that \\( f'(c) = k \\).\n\n**C)** If a function \\( f \\) is continuous on the interval \\( [a, b] \\) and \\( k \\) is any number between \\( f(a) \\) and \\( f(b) \\), then there exists a number \\( c \\) in \\( [a, b] \\) such that \\( f(c) = k \\).\n\n**D)** If a function \\( f \\) is differentiable on the interval \\( [a, b] \\) and \\( k \\) is any number between \\( f(a) \\) and \\( f(b) \\), then there exists a number \\( c \\) in \\( [a, b] \\) such that \\( f'(c) = k \\).\n\n**Correct Answer:** A) If a function \\( f \\) is continuous on the interval \\( [a, b] \\) and \\( k \\) is any number between \\( f(a) \\) and \\( f(b) \\), then there exists a number \\( c \\) in \\( [a, b] \\) such that \\( f(c) = k \\).\n\n### Question 4: L'Hopital's Rule\n**Question:** State L'Hopital's rule for indeterminate forms of type 0/0.\n\n**A)** If \\( \\lim_{x \\to a} f(x) = 0 \\) and \\( \\lim_{x \\to a} g(x) = 0 \\), then \\( \\lim_{x \\to a} \\frac{f(x)}{g(x)} = L \\).\n\n**B)** If \\( \\lim_{x \\to a} f(x) = \\infty \\) and \\( \\lim_{x \\to a} g(x) = \\infty \\), then \\( \\lim_{x \\to a} \\frac{f(x)}{g(x)} = L \\).\n\n**C)** If \\( \\lim_{x \\to a} f(x) = 0 \\) and \\( \\lim_{x \\to a} g(x) = 0 \\), then \\( \\lim_{x \\to a} \\frac{f(x)}{g(x)} = L \\).\n\n**D)** If \\( \\lim_{x \\to a} f(x) = \\infty \\) and \\( \\lim_{x \\to a} g(x) = \\infty \\), then \\( \\lim_{x \\to a} \\frac{f(x)}{g(x)} = L \\).\n\n**Correct Answer:** C) If \\( \\lim_{x \\to a} f(x) = 0 \\) and \\( \\lim_{x \\to a} g(x) = 0 \\), then \\( \\lim_{x \\to a} \\frac{f(x)}{g(x)} = L \\).\n\n### Question 5: Sequences and Series\n**Question:** What is the definition of a sequence?\n\n**A)** A sequence is a function whose domain is the set of natural numbers.\n\n**B)** A sequence is a function whose domain is the set of real numbers.\n\n**C)** A sequence is an ordered list of numbers.\n\n**D)** A sequence is an infinite sum of terms.\n\n**Correct Answer:** C) A sequence is an ordered list of numbers.\n\n### Question 6: Applications of Calculus\n**Question:** What are some applications of calculus in physics?\n\n**A)** Calculus is used to model population growth and decay.\n\n**B)** Calculus is used to describe the motion of objects under constant acceleration.\n\n**C)** Calculus is used to solve problems involving optimization and optimization techniques.\n\n**D)** All of the above.\n\n**Correct Answer:** D) All of the above.\n\n### Question 7: Trigonometric Functions\n**Question:** What is the relationship between trigonometric functions and calculus?\n\n**A)** Trigonometric functions are used to solve differential equations.\n\n**B)** Trigonometric functions are used to model periodic phenomena.\n\n**C)** Trigonometric functions are used to describe the motion of objects under constant acceleration.\n\n**D)** Trigonometric functions are used to solve problems involving optimization and optimization techniques.\n\n**Correct Answer:** B) Trigonometric functions are used to model periodic phenomena.\n\n### Question 8: Fundamental Theorem of Calculus\n**Question:** State the Fundamental Theorem of Calculus.\n\n**A)** The Fundamental Theorem of Calculus states that differentiation and integration are inverse processes.\n\n**B)** The Fundamental Theorem of Calculus states that integration is the inverse process of differentiation.\n\n**C)** The Fundamental Theorem of Calculus states that differentiation is the inverse process of integration.\n\n**D)** The Fundamental Theorem of Calculus states that both differentiation and integration are inverse processes.\n\n**Correct Answer:** D) The Fundamental Theorem of Calculus states that both differentiation and integration are inverse processes.\n\n### Question 9: Taylor's Theorem\n**Question:** What does Taylor's Theorem state?\n\n**A)** Taylor's Theorem states that any function can be approximated by a polynomial.\n\n**B)** Taylor's Theorem states that any polynomial can be approximated by a function.\n\n**C)** Taylor's Theorem states that any function can be expanded into a power series.\n\n**D)** Taylor's Theorem states that any power series can be expanded into a function.\n\n**Correct Answer:** C) Taylor's Theorem states that any function can be expanded into a power series.\n\n### Question 10: Academic Integrity\n**Question:** What is one aspect of academic integrity emphasized in MAT137?\n\n**A)** Plagiarism is strictly forbidden.\n\n**B)** Cheating on exams is not tolerated.\n\n**C)** Respecting the work of others and properly citing sources is essential.\n\n**D)** All of the above.\n\n**Correct Answer:** D) All of the above."
driver = qd.QuestionDriver(text)

# App layout
st.title("Quiz Application")

# Session state to track current question, score, and submission status
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
    st.stop()

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
        st.rerun()
    else:
        st.session_state.feedback = f"❌ Incorrect. The correct answer is **{current_question.correct_choice}) {current_question.choices[current_question.correct_choice]}**."
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
    else: # Last question
        if st.button("Finish Quiz"):
            st.session_state.current_question += 1
            st.session_state.answered = False
            st.session_state.feedback = ""  # Clear feedback for the next question
            st.rerun()  # Reload for the next question