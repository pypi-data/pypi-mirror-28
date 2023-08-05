#!/bin/bash
set -e
[ -n "$DEBUG" ] && set -x

project_path="$1"
env_name="$2"

export PYENV_VIRTUALENV_DISABLE_PROMPT=1

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

if ! pyenv virtualenvs --bare | egrep -e "^${env_name}$"  > /dev/null; then
    printf "Create pyenv virtualenv '%s'\n" "${env_name}"
    pyenv virtualenv ${PYTHON_VERSION} "${env_name}"
else
    printf "Using existing pyenv virtualenv '%s'\n" "${env_name}"
fi

pyenv local "${env_name}"
pyenv activate "${env_name}"
pyenv rehash

python --version

pip install --upgrade pip

for f in requirements*.txt; do
    if [ -s "${f}" ]; then
        pip install --upgrade -r "${f}"
    fi
done

if [ -f setup.py ]; then
    pip install --upgrade -e .
fi
