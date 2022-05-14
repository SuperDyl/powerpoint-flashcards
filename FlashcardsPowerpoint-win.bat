@echo off
@echo "This file can also be run using command line arguments. Use -h for help"
call .\venv\Scripts\activate.bat
cd src
@echo "Running professorFlashcards.py with supplied arguments"
python -m professorFlashcards %*
cd ..
deactivate
@echo "Done"
pause
