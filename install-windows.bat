@echo "Setting up Python libraries in a virtual environment"
python3 -m venv .venv
.venv\Scripts\activate.path
python -m pip install -r src\requirements.txt
echo "Done setting up the environment"
