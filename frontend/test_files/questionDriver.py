import re
from Question import Question

class QuestionDriver:
    def __init__(self, text):
        self.text = text
        self.questions = []
        self.parse_questions()

    def parse_questions(self):
        # Split the text into sections for each question
        question_blocks = re.split(r'### Question \d+:', self.text)[1:]

        for block in question_blocks:
            # Extract title
            title_match = re.search(r'(.*?)\n\*\*Question:\*\*', block, re.DOTALL)
            title = title_match.group(1).strip() if title_match else "Untitled"

            # Extract choices and convert LaTeX to plain text
            choices = re.findall(r'\*\*([A-D])\)\*\* (.*?)\n', block)
            choice_dict = {letter: self.convert_latex_to_text(text) for letter, text in choices}

            # Extract correct answer
            correct_match = re.search(r'\*\*Correct Answer:\*\* ([A-D])', block)
            correct_choice = correct_match.group(1) if correct_match else None

            # Create Question object if valid
            if title and choice_dict and correct_choice:
                question = Question(title, choice_dict, correct_choice)
                self.questions.append(question)

    def convert_latex_to_text(self, text):
        # Replace LaTeX symbols with plain text equivalents
        text = re.sub(r'\\forall', '∀', text)  # For all
        text = re.sub(r'\\exists', '∃', text)  # There exists
        text = re.sub(r'\\epsilon', 'ε', text)  # Epsilon
        text = re.sub(r'\\delta', 'δ', text)  # Delta
        text = re.sub(r'\\to', '→', text)  # Arrow (->)
        text = re.sub(r'\\lim_\{(.*?)\}\s*', r'lim_{\1}', text)  # Correctly format limits
        text = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1 / \2)', text)  # Handle fractions
        text = re.sub(r'_(\{.*?\}|\w)', lambda m: f"_{m.group(1).strip('{}')}" if m else '', text)  # Subscripts
        text = re.sub(r'\^(\{.*?\}|\w)', lambda m: f"^{m.group(1).strip('{}')}" if m else '', text)  # Superscripts
        text = re.sub(r'\\\(|\\\)', '', text)  # Remove \( and \)
        text = re.sub(r'\\_', '_', text)  # Literal underscore
        text = re.sub(r'\\infty', '∞', text)  # Infinity symbol
        text = re.sub(r'\\leq', '≤', text)  # Less than or equal to
        text = re.sub(r'\\geq', '≥', text)  # Greater than or equal to
        text = re.sub(r'\\times', '×', text)  # Multiplication symbol
        text = re.sub(r'\\sqrt\{(.*?)\}', r'√(\1)', text)  # Square root
        text = re.sub(r'\\sum', '∑', text)  # Summation symbol
        text = re.sub(r'\\int', '∫', text)  # Integral symbol
        text = re.sub(r'\\left\|', '|', text)  # Left absolute value
        text = re.sub(r'\\right\|', '|', text)  # Right absolute value
        text = re.sub(r'\\[\[\]]', '', text)  # Remove \[ and \]
        text = re.sub(r'\{(.*?)\}', r'\1', text)  # Remove braces around variables
        return text

    def display_questions(self):
        for i, question in enumerate(self.questions, start=1):
            print(f"Question {i}: {question.title}")
            for key, value in question.choices.items():
                print(f"  {key}) ({value})")
            print(f"Correct Answer: {question.correct_choice}\n")

# Example usage
if __name__ == "__main__":
    text = """### Question 1: Limits and Continuity\n**Question:** What is the formal definition of the limit as \\( x \\) approaches \\( a \\), denoted as \\( \\lim_{x \\to a} f(x) \\)?\n\n**A)** \\( f(a) = L \\)\n\n**B)** \\( \\forall \\epsilon > 0, \\exists \\delta > 0 \\) such that \\( |f(x) - L| < \\epsilon \\) whenever \\( |x - a| < \\delta \\)\n\n**C)** \\( f(x) = L \\)\n\n**D)** \\( f(a) = L \\) and \\( f(x) = L \\)\n\n**Correct Answer:** B) \\( \\forall \\epsilon > 0, \\exists \\delta > 0 \\) such that \\( |f(x) - L| < \\epsilon \\) whenever \\( |x - a| < \\delta \\)\n\n### Question 2: Differentiability\n**Question:** State the definition of a function \\( f \\) being differentiable at a point \\( a \\).\n\n**A)** \\( f(a) = 0 \\)\n\n**B)** \\( f'(a) = \\lim_{h \\to 0} \\frac{f(a + h) - f(a)}{h} \\)\n\n**C)** \\( f(a) = L \\)\n\n**D)** \\( f'(a) = L \\)\n\n**Correct Answer:** B) \\( f'(a) = \\lim_{h \\to 0} \\frac{f(a + h) - f(a)}{h} \\)\n\n### Question 3: Intermediate Value Theorem\n**Question:** State the Intermediate Value Theorem.\n\n**A)** If a function \\( f \\) is continuous on the interval \\( [a, b] \\) and \\( k \\) is any number between \\( f(a) \\) and \\( f(b) \\), then there exists a number \\( c \\) in \\( [a, b] \\) such that \\( f(c) = k \\).\n\n**B)** If a function \\( f \\) is differentiable on the interval \\( [a, b] \\) and \\( k \\) is any number between \\( f(a) \\) and \\( f(b) \\), then there exists a number \\( c \\) in \\( [a, b] \\) such that \\( f'(c) = k \\).\n\n**C)** If a function \\( f \\) is continuous on the interval \\( [a, b] \\) and \\( k \\) is any number between \\( f(a) \\) and \\( f(b) \\), then there exists a number \\( c \\) in \\( [a, b] \\) such that \\( f(c) = k \\).\n\n**D)** If a function \\( f \\) is differentiable on the interval \\( [a, b] \\) and \\( k \\) is any number between \\( f(a) \\) and \\( f(b) \\), then there exists a number \\( c \\) in \\( [a, b] \\) such that \\( f'(c) = k \\).\n\n**Correct Answer:** A) If a function \\( f \\) is continuous on the interval \\( [a, b] \\) and \\( k \\) is any number between \\( f(a) \\) and \\( f(b) \\), then there exists a number \\( c \\) in \\( [a, b] \\) such that \\( f(c) = k \\).\n\n### Question 4: L'Hopital's Rule\n**Question:** State L'Hopital's rule for indeterminate forms of type 0/0.\n\n**A)** If \\( \\lim_{x \\to a} f(x) = 0 \\) and \\( \\lim_{x \\to a} g(x) = 0 \\), then \\( \\lim_{x \\to a} \\frac{f(x)}{g(x)} = L \\).\n\n**B)** If \\( \\lim_{x \\to a} f(x) = \\infty \\) and \\( \\lim_{x \\to a} g(x) = \\infty \\), then \\( \\lim_{x \\to a} \\frac{f(x)}{g(x)} = L \\).\n\n**C)** If \\( \\lim_{x \\to a} f(x) = 0 \\) and \\( \\lim_{x \\to a} g(x) = 0 \\), then \\( \\lim_{x \\to a} \\frac{f(x)}{g(x)} = L \\).\n\n**D)** If \\( \\lim_{x \\to a} f(x) = \\infty \\) and \\( \\lim_{x \\to a} g(x) = \\infty \\), then \\( \\lim_{x \\to a} \\frac{f(x)}{g(x)} = L \\).\n\n**Correct Answer:** C) If \\( \\lim_{x \\to a} f(x) = 0 \\) and \\( \\lim_{x \\to a} g(x) = 0 \\), then \\( \\lim_{x \\to a} \\frac{f(x)}{g(x)} = L \\).\n\n### Question 5: Sequences and Series\n**Question:** What is the definition of a sequence?\n\n**A)** A sequence is a function whose domain is the set of natural numbers.\n\n**B)** A sequence is a function whose domain is the set of real numbers.\n\n**C)** A sequence is an ordered list of numbers.\n\n**D)** A sequence is an infinite sum of terms.\n\n**Correct Answer:** C) A sequence is an ordered list of numbers.\n\n### Question 6: Applications of Calculus\n**Question:** What are some applications of calculus in physics?\n\n**A)** Calculus is used to model population growth and decay.\n\n**B)** Calculus is used to describe the motion of objects under constant acceleration.\n\n**C)** Calculus is used to solve problems involving optimization and optimization techniques.\n\n**D)** All of the above.\n\n**Correct Answer:** D) All of the above.\n\n### Question 7: Trigonometric Functions\n**Question:** What is the relationship between trigonometric functions and calculus?\n\n**A)** Trigonometric functions are used to solve differential equations.\n\n**B)** Trigonometric functions are used to model periodic phenomena.\n\n**C)** Trigonometric functions are used to describe the motion of objects under constant acceleration.\n\n**D)** Trigonometric functions are used to solve problems involving optimization and optimization techniques.\n\n**Correct Answer:** B) Trigonometric functions are used to model periodic phenomena.\n\n### Question 8: Fundamental Theorem of Calculus\n**Question:** State the Fundamental Theorem of Calculus.\n\n**A)** The Fundamental Theorem of Calculus states that differentiation and integration are inverse processes.\n\n**B)** The Fundamental Theorem of Calculus states that integration is the inverse process of differentiation.\n\n**C)** The Fundamental Theorem of Calculus states that differentiation is the inverse process of integration.\n\n**D)** The Fundamental Theorem of Calculus states that both differentiation and integration are inverse processes.\n\n**Correct Answer:** D) The Fundamental Theorem of Calculus states that both differentiation and integration are inverse processes.\n\n### Question 9: Taylor's Theorem\n**Question:** What does Taylor's Theorem state?\n\n**A)** Taylor's Theorem states that any function can be approximated by a polynomial.\n\n**B)** Taylor's Theorem states that any polynomial can be approximated by a function.\n\n**C)** Taylor's Theorem states that any function can be expanded into a power series.\n\n**D)** Taylor's Theorem states that any power series can be expanded into a function.\n\n**Correct Answer:** C) Taylor's Theorem states that any function can be expanded into a power series.\n\n### Question 10: Academic Integrity\n**Question:** What is one aspect of academic integrity emphasized in MAT137?\n\n**A)** Plagiarism is strictly forbidden.\n\n**B)** Cheating on exams is not tolerated.\n\n**C)** Respecting the work of others and properly citing sources is essential.\n\n**D)** All of the above.\n\n**Correct Answer:** D) All of the above."""  # Partial text for testing

    driver = QuestionDriver(text)
    driver.display_questions()
