#!/bin/sh
echo
echo
echo "This file can be run using command line arguments. Use -h for help"
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "${DIR}"
source ./venv/bin/activate

cd ./src
python -m professorFlashcards "$@"
echo