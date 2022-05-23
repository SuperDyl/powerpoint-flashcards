@echo off
@echo This file can also be run using command line arguments. Use -h for help
call .\venv\Scripts\activate.bat
cd src
@echo Running employeeFlashcards.py with supplied arguments
@echo It may take a couple minutes if re-downloading photos
python -m employeeFlashcards %1 %*
cd ..
@echo Done
pause
deactivate
