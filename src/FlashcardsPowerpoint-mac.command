#!/bin/sh
echo
echo
echo "This file can also be run using command line arguments. Use -h for help"
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "${DIR}"
source ./venv/bin/activate

cd ./src
echo "Running employeeFlashcards.py with supplied arguments"
echo "It may take a couple minutes if re-downloading photos"
python -m employeeFlashcards "$@"
deactivate
echo