"""
Build text boxes as a template for use with python-pptx
"""
from pptx import slide as pptx_slide
from pptx.shapes import autoshape as pptx_textbox
from pptx.util import Emu

from typing import NamedTuple


class Position(NamedTuple):
    left: Emu
    top: Emu


class Dimension(NamedTuple):
    width: Emu
    height: Emu


class TextboxTemplate:
    """
    Build text boxes using this instances data as a template

    """
    def __init__(self, position: Position, dimensions: Dimension):
        self.left, self.top = position
        self.width, self.height = dimensions

    @property
    def position(self) -> Position:
        return Position(self.left, self.top)

    @position.setter
    def position(self, new_position: Position):
        self.left, self.top = new_position

    @property
    def dimensions(self) -> Dimension:
        return Dimension(self.width, self.height)

    @dimensions.setter
    def dimensions(self, new_dimensions: Dimension):
        self.width, self.height = new_dimensions

    def add_textbox(self, slide: pptx_slide) -> pptx_textbox:
        """Add a textbox to slide following the template and using these given details"""
        return slide.shapes.add_textbox(self.left, self.top, self.width, self.height)

    def __copy__(self):
        return TextboxTemplate(self.position, self.dimensions)
