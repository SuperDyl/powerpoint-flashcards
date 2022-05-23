@echo off
@echo Before continuing, ensure that the listed version is not Python3.10 (Python3.6 is preferred)
python --version
pause
@echo Setting up or re-setting up Python libraries in a virtual environment
rmdir .\venv /s /q
python -m venv venv
call .\venv\Scripts\activate.bat

python -m pip install --upgrade pip
python -m pip install --upgrade setuptools
python -m pip install --upgrade wheel

python -m pip install -r src\requirements.txt
copy /y .\src\FlashcardsPowerpoint-win.bat .\
@echo Done setting up the environment
@echo Use FlashcardsPowerpoint-win.bat to create powerpoints
pause
deactivate
