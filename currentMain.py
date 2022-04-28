#!/usr/bin/python3.6
"""
A flashcards PowerPoint builder
"""

from templates import professor_slide_template
from pptxtemplate import SlideTemplate

from professor import Professor

from pptx import Presentation

if __name__ == "__main__":
    presentation = Presentation()
    prof_layout = professor_slide_template(SlideTemplate())

    all_profs = Professor.from_website()

    for prof in all_profs:
        prof_layout(presentation, prof.full_name, ''.join(('pictures/', prof.full_name, '.png')))

    presentation.save('Example.pptx')
