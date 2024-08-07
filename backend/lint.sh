. venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install flake8
flake8 . --exclude=venv
