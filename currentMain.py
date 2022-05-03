#!/usr/bin/python3.6
"""
A flashcards PowerPoint builder
"""
from templates import build_professor_slide_func
from pptxtemplate import SlideTemplate

from professor import Professor

from pptx import Presentation

from os import scandir, getcwd, path, PathLike
from pathlib import Path
from typing import Optional, List


def find_professor_picture(prof_full_name: str, directory: Optional[PathLike] = None) -> Optional[PathLike]:
    if directory is None:
        directory = getcwd()

    with scandir(directory) as dir_items:
        for item in dir_items:
            if not item.is_file():
                continue

            file_without_extension = path.splitext(item.name)[0]

            if file_without_extension == prof_full_name:
                return item.path
        return None


def build_presentation(file_name: str, all_professors: List[Professor]):
    presentation = Presentation()
    add_prof_slide = build_professor_slide_func(SlideTemplate())

    for prof in all_professors:
        picture = find_professor_picture(prof.full_name, Path('pictures'))
        add_prof_slide(presentation, prof.full_name, str(picture))

    presentation.save(file_name)


if __name__ == "__main__":
    all_profs = Professor.from_website()
    build_presentation('Example.pptx', all_profs)
