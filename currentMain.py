#!/usr/bin/python3.6
'''
A flashcards powerpoint builder
'''

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor #, ColorFormat
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE

import pdb
import re

from bs4 import BeautifulSoup
from urllib.request import urlopen

prs = Presentation()
BLANK_LAYOUT = prs.slide_layouts[6]

def print_bad_formatted_rooms():
    update_professor_file()
    old_p = pull_professor_data_old()
    professors = parse_professor_data()
    for old, new in zip(old_p, professors):
        if old.room != (str(new.room)[3:]):
            print(old)
    print("Done!")
    #print(*(f'{n.room}, {o.room}' for o, n in zip(old, professors)), sep='\n')

def add_slide(prof_name):
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    textbox_height = Inches(1.58)
    name_textbox = slide.shapes.add_textbox(left=0, top=prs.slide_height-textbox_height,
                                            width=prs.slide_width, height=textbox_height)
    frame = name_textbox.text_frame
    frame.text = prof_name
    frame.auto_size = MSO_AUTO_SIZE.NONE
    frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    font = frame.paragraphs[0].font
    font.size = Pt(88)
    font.color.rgb = RGBColor(255,0,0)


def pull_professor_data(url="https://religion.byu.edu/directory"):
    html_data = ""
    with urlopen(url) as request:
        html_data = request.read().decode("utf-8")
    bs = BeautifulSoup(html_data, 'html.parser')

    professors = []
    for tag in bs.find_all('div', class_='PromoVerticalImage-content'):
        room = ''
        try:
            room = tag.find_all('p')[0].contents[0].string.strip()
            room = RoomAddress.from_string(room)
        except IndexError:
            pass
        name = tag.find_all(class_='PromoVerticalImage-title promo-title')[0].find('a').string
        professors.append(Professor(str(name), room))

    return professors


def pull_professor_data_old(url="https://religion.byu.edu/directory"):
    html_data = ""
    with urlopen(url) as request:
        html_data = request.read().decode("utf-8")
    bs = BeautifulSoup(html_data, 'html.parser')

    professors = []
    for tag in bs.find_all('div', class_='PromoVerticalImage-content'):
        room = ''
        try:
            room = tag.find_all('p')[0].contents[0].string.strip()
            # room = RoomAddress.from_string(room)
        except IndexError:
            pass
        name = tag.find_all(class_='PromoVerticalImage-title promo-title')[0].find('a').string
        professors.append(Professor(name, room))

    return professors


class RoomAddress:
    def __init__(self, building, floor, rm_num, rm_letter=''):
        self.floor = floor
        self.rm_num = rm_num
        self.rm_letter = rm_letter
        self.building = building

    def __str__(self):
        output = ''
        if self.floor:
            output += f'{self.floor}f'
        if self.rm_num:
            output += f' {self.rm_num}{self.rm_letter}'
        if self.building:
            output += f' {self.building}'
        return output.strip()

    def __repr__(self):
        return self.building, self.floor, self.rm_num, self.rm_letter

    def __bool__(self):
        return any(self.building, self.floor, self.rm_num)

    @staticmethod
    def _clean_string(string):
        clean_string = string.strip()
        clean_string = re.sub(r'-', ' ', clean_string)
        clean_string = re.sub(r'Office(:\s)*', '', clean_string)
        clean_string = re.sub(r'Joseph.*', 'JSB', clean_string)
        clean_string = re.sub(r'Heber.*', 'HGB', clean_string)
        clean_string = re.sub(r'(?<=\d)\s*([^\d\s])(?!\w)', r'\g<1>', clean_string)
        # clean_string = re.sub('(?!\d+ +)([^\d\s]){1} ', ' \g<1>', clean_string)
        # clean_string = re.sub(' +', ' ', clean_string)
        return clean_string

    @staticmethod
    def _split_string(string):

        building = re.search(r'[^\d\s]{2,}', string)
        building = "" if not building else building.group(0)
        rm_num = re.search(r'\d{2,}', string)
        rm_num = "" if not rm_num else rm_num.group(0)
        rm_letter = re.search(r'(?<=\d{2})([^\d\s])(?!\w)', string)
        rm_letter = "" if not rm_letter else rm_letter.group(0)
        floor = rm_num[0] if rm_num else ""

        return building, floor, rm_num, rm_letter

    @classmethod
    def from_string(cls, string):
        # building, floor, rm_num, rm_letter = RoomAddress._split_string(room_string)
        # floor = rm_num[0]
        # cls = RoomAddress(building, floor, rm_num, rm_letter)
        string = RoomAddress._clean_string(string)
        cls = RoomAddress(*RoomAddress._split_string(string))
        return cls

    @staticmethod
    def from_string_iter(string_iter):
        clean_string = '\n'.join(string_iter)
        # scrub data
        clean_string = RoomAddress._clean_string(clean_string)
        new_string_iter = clean_string.split('\n')
        # print(new_string_iter)

        return [RoomAddress(*RoomAddress._split_string(room_string))
                for room_string in new_string_iter]
        '''
        output = []
        for room_string in new_string_iter:
            #building, floor, rm_num, rm_letter = RoomAddress._split_string(room_string)
            #floor = rm_num[0]
            #output.append(RoomAddress(building, floor, rm_num, rm_letter))
            output.append(RoomAddress(*RoomAddress._split_string(room_string)))

        return output
        #'''


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
        cls = Professor(', '.join(name), RoomAddress.from_string(room))
        return cls


def update_professor_file(file_name='professors.txt', professors=None):
    if not professors:
        professors = pull_professor_data(url="https://religion.byu.edu/directory")
    new_prof_dict = dict(zip((x.name for x in professors), professors))
    old_professors = parse_professor_data(file_name)
    old_prof_dict = dict(zip((x.name for x in old_professors), old_professors))
    old_prof_dict.update(new_prof_dict)
    for name, prof in old_prof_dict.items():
        prof.name = name

    with open(file_name, 'w') as file:
        file.write(('\n'.join((str(p) for p in old_prof_dict.values()))))

    return old_prof_dict.values()

def parse_professor_data(file_name='professors.txt'):
    with open(file_name, 'r') as file:
        return [Professor.from_string(line) for line in file]

#professors = update_professor_file()
os.listdir()
print_bad_formatted_rooms()

for n in names:
    add_slide(n)
prs.save("Testing2.pptx")

#professors = pull_professor_data()
#print(*professors, sep='\n')

#rooms = RoomAddress.from_string_iter(rooms)
#print(len(names), len(rooms))
#print(*(f'{name:25}={str(room)}' for name, room in zip(names, rooms)), sep='\n')

#names, rooms = pull_professor_data()
#print(*(r for r in rooms), sep='\n')
#print(*(r for r in RoomAddress.from_string_iter(rooms)), sep='\n')
#rooms = RoomAddress.from_string_iter(rooms)
#print(len(names), len(rooms))
#print(*(f'{name:25}={str(room)}' for name, room in zip(names, rooms)), sep='\n')

#names, rooms = pull_professor_data()
#print(*(f'{n:35} = {r}' for n, r in zip(names, rooms)), sep='\n')
#print(*(r for r in rooms), sep='\n')

#add_slide("Richard Crookston")
#prs.save("Testing.pptx")