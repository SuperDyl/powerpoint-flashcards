"""
Setup and create get-to-know-you flashcards using PowerPoint
"""

from person import Person


class FlashcardPowerPoint:
    def __init__(self):
        self.people = list()

    def add_person(self, person: Person):
        self.people.append(person)


class GetToKnowProfessorBuilder (FlashcardPowerPoint):
    def __init__(self):
        super().__init__()
