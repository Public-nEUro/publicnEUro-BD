# This script requires pyenv to be installed on your machine

pyenv install --skip-existing 3.12
pyenv global 3.12

python3 -m venv venv
. venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r ./requirements.txt

pip install -e .

python3 -m pip install --upgrade --cache-dir .cache/pip ruff pylint vulture mypy pyright types-requests types-paramiko sqlalchemy-stubs flask-sqlalchemy-stubs types-python-dateutil types-flask-cors types-pytz types-cryptography pytest pytest-watch
