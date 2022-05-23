#!/bin/sh
echo
echo
echo
echo "Setting up or re-setting up Python libraries in a virtual environment"
echo "Program will fail if Python3.6 is not installed"
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "${DIR}"
rm -rf ./venv
python3.6 -m venv venv
source ./venv/bin/activate

python -m pip install --upgrade pip
python -m pip install --upgrade setuptools
python -m pip install --upgrade wheel

python -m pip install -r src/requirements.txt
deactivate
cp ./src/FlashcardsPowerpoint-mac.command ./
echo
echo
echo "Done setting up the environment"
echo "Use FlashcardsPowerpoint-mac.command to create powerpoints"
echo
echo
