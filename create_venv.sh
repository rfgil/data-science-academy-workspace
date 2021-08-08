#! /bin/bash

venv_dir="/Users/rafael.gil/.virtualenvs/$1"

if [ ! -d "$venv_dir" ]; then
  /usr/local/opt/python@3.7/bin/python3.7 -m venv $venv_dir
  echo "Created enviornment: $venv_dir"
fi

source "$venv_dir/bin/activate"
python -m pip install --upgrade pip
