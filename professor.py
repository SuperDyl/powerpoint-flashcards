from room import Room
from person import Person


class Professor (Person):
    def __init__(self, name: str, room: str):  # , pic_file=""):
        super().__init__(name, room)
        # self.name = name
        # self.room = room
        # self.picture = pic_file

    # def __str__(self):
    #     return f'{self.name}, {self.room}'
    #     # return f'{self.name}, {self.room}, {self.picture}'

    # def __repr__(self):
    #     return str(self)

    @classmethod
    def from_string(cls, string):
        *name, room = string.split(', ')
        prof = Professor(', '.join(name), Room.from_string(room))
        cls.name = prof.name
        cls.room = prof.room
        return cls
