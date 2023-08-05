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
pyenv which python

# pip install --upgrade pip

PIP_OPTIONS=""  # "--upgrade"
PIP_ARGS=""
for f in requirements.txt requirements-tests.txt; do
    if [ -s "${f}" ]; then
        PIP_ARGS="${PIP_ARGS} -r ${f}"
    fi
done

if [ -f setup.py ]; then
    PIP_ARGS="${PIP_ARGS} -e ."
fi

if [ ! -z "${PIP_ARGS}" ]; then
    printf "Running: pip install %s %s\n" "$PIP_OPTIONS" "$PIP_ARGS"
    pip install $PIP_OPTIONS $PIP_ARGS
fi
