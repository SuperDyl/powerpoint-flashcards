"""
Templates used to create each PowerPoint slide
"""

from pptxtemplate import SlideTemplate, TextboxTemplate, Position, Dimension, pptx_presentation
from pptx import slide as pptx_slide
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_AUTO_SIZE, PP_PARAGRAPH_ALIGNMENT


class PowerpointTextboxBaseTemplate:
    """
    Base formatting for all text boxes in PowerPoint Flashcards

    """
    def __init__(self, template: TextboxTemplate):
        self.template = template
        self.font_size = Pt(72)
        self.font_color = RGBColor(255, 0, 0)
        self.font_color_mode = "rgb"  # FONT_COLOR_MODE["RGB"]

    def add_base_textbox(self, slide: pptx_slide):
        """Add to slide and return a textbox with default formatting"""
        textbox = self.template.add_textbox(slide)

        frame = textbox.text_frame
        frame.auto_size = MSO_AUTO_SIZE.NONE
        frame.paragraphs[0].alignment = PP_PARAGRAPH_ALIGNMENT.CENTER

        font = frame.paragraphs[0].font
        font.size = self.font_size
        setattr(font.color, self.font_color_mode, self.font_color)

        return textbox


def professor_name_textbox_template(template: TextboxTemplate):
    """Return a function to format, add, and return a textbox formatted for a professor's name"""
    base_template = PowerpointTextboxBaseTemplate(template)

    def add_professor_name_textbox(slide: pptx_slide, professor_name: str):
        """Add to slide and then return a default formatted textbox"""
        textbox = base_template.add_base_textbox(slide)
        textbox.text_frame.paragraphs[0].add_run().text = professor_name
        return textbox

    return add_professor_name_textbox


def room_number_textbox_template(template: TextboxTemplate):
    """Return a function to format, add, and return a textbox formatted for a room number"""
    base_template = PowerpointTextboxBaseTemplate(template)

    def add_room_number_textbox(slide: pptx_slide, room_number: str):
        """Add to slide and then return a default formatted textbox"""
        textbox = base_template.add_base_textbox(slide)
        textbox.text_frame.paragraphs[0].add_run().text = room_number
        return textbox

    return add_room_number_textbox


class BaseSlideTemplate:
    """
    Add and return a new slide formatted for a room
    """
    def __init__(self, slide_template: SlideTemplate):
        self.slide_template = slide_template
        self.name_bottom_padding = Inches(1.58)

        left = Inches(0)
        top = Inches(0)  # presentation.height - textbox_height
        width = Inches(10)  # presentation.width
        height = Inches(1)  # textbox_height

        self.professor_base_template = TextboxTemplate(Position(left=left, top=top),
                                                       Dimension(width=width, height=height))
        self.professor_name_template = professor_name_textbox_template(self.professor_base_template)

    def add_base_slide(self, presentation: pptx_presentation, professor_name: str):
        """Create, add, and return a new slide formatted with base conditions"""
        slide = self.slide_template.add_slide(presentation)
        self.professor_name_template(slide, professor_name)
        return slide


def room_slide_template(slide_template: SlideTemplate):
    """Return a template which adds and returns a new slide formatted for a room"""
    base_slide_template = BaseSlideTemplate(slide_template)

    left, top = base_slide_template.professor_base_template.position
    width, height = base_slide_template.professor_base_template.dimensions

    room_defaults = TextboxTemplate(Position(left=left, top=top), Dimension(width=width, height=height))
    room_number_template = room_number_textbox_template(room_defaults)

    def add_room_slide(presentation: pptx_presentation, professor_name: str, room_num: str,
                       room_pos: Position, room_dimensions: Dimension, floor_pic: str):
        """Create, add, and return a new slide formatted for a room flashcard"""
        slide = base_slide_template.add_base_slide(presentation, professor_name)
        room_number_template(slide, room_num)
        return slide

    return add_room_slide


def professor_slide_template(slide_template: SlideTemplate):
    """Return a template which adds and returns a new slide formatted for a professor picture"""
    base_slide_template = BaseSlideTemplate(slide_template)

    left, top = base_slide_template.professor_base_template.position
    width, height = base_slide_template.professor_base_template.dimensions

    room_defaults = TextboxTemplate(Position(left=left, top=top), Dimension(width=width, height=height))
    base_slide_template.room_number_template = room_number_textbox_template(room_defaults)

    def add_professor_slide(presentation: pptx_presentation, professor_name: str, professor_pic: str):
        """Create, add, and return a new slide formatted for a professor picture flashcard"""
        slide = base_slide_template.add_base_slide(presentation, professor_name)
        return slide

    return add_professor_slide
