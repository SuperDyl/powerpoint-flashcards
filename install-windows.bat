@echo off
@echo Before continuing, ensure that the listed version is not Python3.10 (Python3.6 is preferred)
python --version
pause
@echo Setting up or re-setting up Python libraries in a virtual environment
rmdir .\venv /s /q
python -m venv venv

.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install --upgrade setuptools
.\venv\Scripts\python.exe -m pip install --upgrade wheel

.\venv\Scripts\python.exe -m pip install -r src\requirements.txt
copy /y .\src\FlashcardsPowerpoint-win.bat .\
@echo Done setting up the environment
@echo Use FlashcardsPowerpoint-win.bat to create powerpoints
pause
