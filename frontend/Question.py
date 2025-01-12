class Question:
    def __init__(self, title, choices, correct_choice):
        self.title = title
        self.choices = choices
        self.correct_choice = correct_choice

    def is_correct(self, choice):
        return choice == self.correct_choice
