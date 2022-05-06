#!/usr/bin/python3.6
"""
A flashcards PowerPoint builder

Constants:
X_FRM: XML for a group_shape. Necessary for adding animations to the PowerPoint
TIMING: XML for animation timings. Necessary for adding animations to the PowerPoint
"""

from templates import build_professor_slide_func
from pptxtemplate import SlideTemplate

from professor import Professor

from pptx import Presentation

from os import scandir, getcwd, path, PathLike
from pathlib import Path
from typing import Optional, Iterable
from zipfile import ZipFile
from tempfile import TemporaryDirectory
import shutil
import re

X_FRM = r'<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>' \
        r'<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'

TIMING = r'</p:clrMapOvr><p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">' \
         r'<p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq">' \
         r'<p:childTnLst><p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>' \
         r'<p:childTnLst><p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/>' \
         r'</p:stCondLst><p:childTnLst><p:par>' \
         r'<p:cTn id="5" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" grpId="0" ' \
         r'nodeType="clickEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:set><p:cBhvr>' \
         r'<p:cTn id="6" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl>' \
         r'<p:spTgt spid="2"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>' \
         r'</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set></p:childTnLst></p:cTn></p:par></p:childTnLst>' \
         r'</p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn><p:prevCondLst>' \
         r'<p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst>' \
         r'<p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>' \
         r'</p:childTnLst></p:cTn></p:par></p:tnLst><p:bldLst><p:bldP spid="2" grpId="0"/></p:bldLst></p:timing>'


def add_animations(pptx_file: PathLike, start_slide: int = 0) -> None:
    """
    Add animations to the PowerPoint.
    This is a duck-tape solution:
    it only exists this way because no open-source library allows editing PowerPoint animations.

    :param pptx_file: file path for flashcards PowerPoint to add animations to
    :param start_slide: all slides > this number get animations added to them
    """
    with ZipFile(pptx_file) as zipfile, TemporaryDirectory() as temp_dir:
        zipfile.extractall(temp_dir)
        slides_path = path.join(temp_dir, 'ppt', 'slides')
        with scandir(slides_path) as slides_dir:
            for item in slides_dir:
                slide_num_match = re.search(r'\d+', item.name)
                if item.is_file() and int(slide_num_match[0]) > start_slide:
                    with open(item, 'r+') as slide_file:
                        file_text = slide_file.read()
                        file_text = file_text.replace(r'<p:grpSpPr/>', X_FRM)
                        file_text = file_text.replace(r'</p:clrMapOvr>', TIMING)
                        slide_file.seek(0)
                        slide_file.write(file_text)
        shutil.make_archive(str(pptx_file), 'zip', temp_dir)
        shutil.move(str(pptx_file) + '.zip', pptx_file)


def find_file_extension(file_name: str, directory: Optional[PathLike] = None) -> Optional[str]:
    """
    Find the file name with its extension knowing only the file name.

    :param file_name: file_name with file extension
    :param directory: directory to search in. Defaults to working directory
    :returns: path to file name with extension OR None if no matching file was found
    """
    if directory is None:
        directory = getcwd()

    with scandir(directory) as dir_items:
        for item in dir_items:
            if not item.is_file():
                continue

            file_without_extension = path.splitext(item.name)[0]

            if file_without_extension == file_name:
                return item.path
        return None


def build_presentation(file_name: PathLike, all_professors: Iterable[Professor],
                       start_file: Optional[PathLike] = None) -> None:
    """
    Create a flashcards pptx of each professor in all_professors.

    :param file_name: name to save the flashcards PowerPoint as
    :param all_professors: all professors to have slides in the PowerPoint
    :param start_file: file to be appended to. If None, creates a new file from scratch
    """
    presentation = Presentation(start_file)
    slides_count = len(presentation.slides)
    add_prof_slide = build_professor_slide_func(SlideTemplate())

    for prof in all_professors:
        picture = find_file_extension(prof.full_name, Path('pictures'))
        add_prof_slide(presentation, prof.full_name, str(picture))

    presentation.save(file_name)
    add_animations(file_name, slides_count)


if __name__ == "__main__":
    all_profs = Professor.from_website()
    filtered_profs = (prof for prof in all_profs
                      if prof.job_title not in ('Adjunct Instructor', 'Visiting Instructor', 'Preservice', 'On Leave')
                      if prof.department not in ('Salt Lake Center',)
                      )

    build_presentation(Path('Example.pptm'), filtered_profs, Path('FlashcardStartingPowerpoint.pptm'))
