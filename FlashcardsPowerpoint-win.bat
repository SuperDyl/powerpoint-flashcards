@echo "This file can be run using command line arguments. Use -h for help"
.\venv\Scripts\activate.path
cd src
python -m professorFlashcards "%*"
@echo "Done"
