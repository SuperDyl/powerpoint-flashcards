#!/bin/sh
echo
echo
echo "This file can also be run using command line arguments. Use -h for help"
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "${DIR}"
source ./venv/bin/activate

cd ./src
echo "Running professorFlashcards.py with supplied arguments"
python -m professorFlashcards "$@"
echo