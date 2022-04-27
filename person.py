"""
Stores data for a person
"""
from roomold import RoomOld


class Person:
    def __init__(self, first_name: str, last_name: str, room: str, picture: str = "TODO"):  # TODO: add picture support
        self.first_name = first_name
        self.last_name = last_name
        self.room = room
        self.picture = picture

    def __str__(self):
        return f'{self.name}, {str(self.room)}, {self.picture}'
        # out = self.name
        # out += ", " + str(self.room)  # self.room.__str__(self.room)
        # out += ", " + self.picture
        # return out

    @property
    def name(self):
        return ' '.join((self.first_name, self.last_name))

    def __repr__(self):
        return str(self)

    @classmethod  # TODO:Remove from Person class
    def from_string(cls, string):
        *name, room = string.split(', ')
        prof = Person(', '.join(name), 'LAST_NAME', RoomOld.from_string(room))
        # cls.name = prof.name
        # cls.room = prof.room
        return prof
