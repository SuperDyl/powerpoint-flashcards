"""
Setup and create get-to-know-you flashcards using PowerPoint
"""

from pptxtemplate import DEFAULT_BLANK_LAYOUT
from person import Person
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_AUTO_SIZE, PP_PARAGRAPH_ALIGNMENT

# FONT_COLOR_MODE = {"RGB": "rgb"}
BLANK_LAYOUT = DEFAULT_BLANK_LAYOUT


class FlashcardPowerPoint:
    def __init__(self, people: list = None):
        self.people = list(people) if people is not None else list()
        self.name_bottom_padding = Inches(1.58)
        self.font_size = Pt(88)
        self.font_color = RGBColor(255, 0, 0)
        self.font_color_mode = "rgb"

    def _add_default_slide(self, presentation: Presentation, person_name: str):
        slide = presentation.slides.add_slide(BLANK_LAYOUT)
        textbox_height = self.name_bottom_padding
        name_textbox = slide.shapes.add_textbox(left=0, top=presentation.height - textbox_height,
                                                width=presentation.width, height=textbox_height)
        frame = name_textbox.text_frame
        frame.text = person_name
        frame.auto_size = MSO_AUTO_SIZE.NONE
        frame.paragraphs[0].alignment = PP_PARAGRAPH_ALIGNMENT.CENTER
        font = frame.paragraphs[0].font
        font.size = self.font_size
        setattr(font.color, self.font_color_mode, self.font_color)
        return slide

    def _add_room_slide(self, presentation: Presentation, person: Person, base_slide=None):
        if base_slide is None:
            base_slide = self._add_default_slide
        slide = base_slide(presentation, person.name)
        return slide

    def _add_picture_slide(self, presentation: Presentation, person: Person, base_slide=None):
        if base_slide is None:
            base_slide = self._add_default_slide
        slide = base_slide(presentation, person.name)
        return slide

    def _add_slides(self, presentation: Presentation, person: Person, room_slide=None, picture_slide=None):
        if room_slide is None:
            room_slide = self._add_room_slide
        if picture_slide is None:
            picture_slide = self._add_picture_slide

        if person.name and person.picture:
            room_slide(presentation, person)
        if person.name and person.room:
            picture_slide(presentation, person)

    def add_person(self, person: Person):
        self.people.append(person)

    def export_powerpoint(self, file_name):
        presentation = Presentation()
        for person in self.people:
            self._add_slides(presentation, person)

        presentation.save(file_name)
