"""
Stores data for a person
"""


class Person:
    def __init__(self, name: str, room: str, picture: str = "TODO"):  #TODO: add picture support
        self.name = name
        self.room = room
        self.picture = picture

    def __str__(self):
        return f'{self.name}, {self.room}, {self.picture}'

    def __repr__(self):
        return str(self)
