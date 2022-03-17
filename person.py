"""
Stores data for a person
"""
from room import Room


class Person:
    def __init__(self, name: str, room: str, picture: str = "TODO"):  # TODO: add picture support
        self.name = name
        self.room = room
        self.picture = picture

    def __str__(self):
        return f'{self.name}, {self.room}, {self.picture}'

    def __repr__(self):
        return str(self)

    @classmethod  # TODO:Remove from Person class
    def from_string(cls, string):
        *name, room = string.split(', ')
        prof = Person(', '.join(name), Room.from_string(room))
        cls.name = prof.name
        cls.room = prof.room
        return cls
