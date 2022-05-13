echo
echo
echo
echo "Setting up Python libraries in a virtual environment"
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "${DIR}"
python3 -m venv venv
source ./venv/bin/activate
python -m pip install -r src/requirements.txt
echo "Done setting up the environment"
echo
echo
