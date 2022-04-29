#!/usr/bin/python3.6
"""
A flashcards PowerPoint builder
"""

from templates import build_professor_slide_func
from pptxtemplate import SlideTemplate

from professor import Professor

from pptx import Presentation

if __name__ == "__main__":
    presentation = Presentation()
    prof_layout = build_professor_slide_func(SlideTemplate())

    all_profs = Professor.from_website()

    for prof in all_profs:
        prof_layout(presentation, prof.full_name, ''.join(('pictures/', prof.full_name, '.png')))

    presentation.save('Example.pptx')
