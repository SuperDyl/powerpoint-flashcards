@echo "This file can also be run using command line arguments. Use -h for help"
.\venv\Scripts\activate.path
cd src
@echo "Running professorFlashcards.py with supplied arguments"
python -m professorFlashcards "%*"
@echo "Done"
