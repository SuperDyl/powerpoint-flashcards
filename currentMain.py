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
from zipfile import ZipFile
from tempfile import TemporaryDirectory
import shutil

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


def add_animations(pptx_file: PathLike):
    with ZipFile(pptx_file) as zipfile, TemporaryDirectory() as temp_dir:
        zipfile.extractall(temp_dir)
        slides_path = path.join(temp_dir, 'ppt', 'slides')
        with scandir(slides_path) as slides_dir:
            for item in slides_dir:
                if item.is_file():
                    with open(item, 'r+') as slide_file:
                        file_text = slide_file.read()
                        file_text = file_text.replace(r'<p:grpSpPr/>', X_FRM)
                        file_text = file_text.replace(r'</p:clrMapOvr>', TIMING)
                        slide_file.seek(0)
                        slide_file.write(file_text)
        shutil.make_archive(str(pptx_file), 'zip', temp_dir)
        shutil.move(str(pptx_file) + '.zip', pptx_file)


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


def build_presentation(file_path: PathLike, all_professors: List[Professor]):
    presentation = Presentation()
    add_prof_slide = build_professor_slide_func(SlideTemplate())

    for prof in all_professors:
        picture = find_professor_picture(prof.full_name, Path('pictures'))
        add_prof_slide(presentation, prof.full_name, str(picture))

    presentation.save(file_path)
    add_animations(file_path)


if __name__ == "__main__":
    all_profs = Professor.from_website()
    build_presentation(Path('Example.pptx'), all_profs)
