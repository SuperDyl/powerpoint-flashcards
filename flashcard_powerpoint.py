"""
Setup and create get-to-know-you flashcards using PowerPoint
"""

from person import Person
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_AUTO_SIZE, PP_PARAGRAPH_ALIGNMENT

BLANK_LAYOUT = 6
# FONT_COLOR_MODE = {"RGB": "rgb"}


class SlideTemplate:
    def __init__(self, **kwargs):
        pass


class FlashcardPowerPoint:
    def __init__(self):
        self.people = list()
        self.name_bottom_padding = Inches(1.58)
        self.font_size = Pt(88)
        self.font_color = RGBColor(255, 0, 0)
        self.font_color_mode = "rgb"  # FONT_COLOR_MODE["RGB"]

    def add_person(self, person: Person):
        self.people.append(person)

    def _add_room_slide(self, presentation: Presentation, person: Person):
        pass

    def _add_picture_slide(self, presentation: Presentation, person: Person):
        slide = presentation.slides.add_slide(BLANK_LAYOUT)
        textbox_height = self.name_bottom_padding
        name_textbox = slide.shapes.add_textbox(left=0, top=presentation.slide_height - textbox_height,
                                                width=presentation.slide_width, height=textbox_height)
        frame = name_textbox.text_frame
        frame.text = person.name
        frame.auto_size = MSO_AUTO_SIZE.NONE
        frame.paragraphs[0].alignment = PP_PARAGRAPH_ALIGNMENT.CENTER
        font = frame.paragraphs[0].font
        font.size = self.font_size
        setattr(font.color, self.font_color_mode, self.font_color)

    def _add_slides(self, presentation: Presentation, person: Person):
        if person.name and person.picture:
            self._add_picture_slide(presentation, person)
        if person.name and person.room:
            self._add_room_slide(presentation, person)

    def export_powerpoint(self, file_name):
        presentation = Presentation()
        for person in self.people:
            self._add_slides(presentation, person)

        presentation.save(file_name)
