@echo off
@echo "Before continuing, ensure that you have Python3.6 downloaded from Python.org"
pause
@echo "Setting up Python libraries in a virtual environment"
python -m venv venv
call .\venv\Scripts\activate.bat

python -m pip install --upgrade pip
python -m pip install --upgrade setuptools
python -m pip install --upgrade wheel

python -m pip install -r src\requirements.txt
deactivate
@echo "Done setting up the environment"
pause
