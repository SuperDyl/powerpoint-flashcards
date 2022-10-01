#!/bin/sh
echo
echo
echo
echo "Setting up or re-setting up Python3 libraries in a virtual environment"
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "${DIR}"
rm -rf ./venv
python3 -m venv venv

./venv/bin/python3 -m pip install --upgrade pip
./venv/bin/python3 -m pip install --upgrade setuptools
./venv/bin/python3 -m pip install --upgrade wheel

./venv/bin/python3 -m pip install -r src/requirements.txt
cp ./src/FlashcardsPowerpoint-mac.command ./
echo
echo
echo "Done setting up the environment"
echo "Use FlashcardsPowerpoint-mac.command to create powerpoints"
echo
echo
