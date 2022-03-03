from room_address import RoomAddress


class Professor:
    def __init__(self, name, room):  # , pic_file=""):
        self.name = name
        self.room = room
        # self.picture = pic_file

    def __str__(self):
        return f'{self.name}, {self.room}'
        # return f'{self.name}, {self.room}, {self.picture}'

    def __repr__(self):
        return str(self)

    @classmethod
    def from_string(cls, string):
        *name, room = string.split(', ')
        prof = Professor(', '.join(name), RoomAddress.from_string(room))
        cls.name = prof.name
        cls.room = prof.room

        return cls
