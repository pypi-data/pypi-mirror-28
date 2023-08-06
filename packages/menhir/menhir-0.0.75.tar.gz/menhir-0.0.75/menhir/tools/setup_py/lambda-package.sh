#!/usr/bin/env bash

set -e
[ -n "$DEBUG" ] && set -x


tmpdir=$(mktemp -d packageXXXX)

cleanup() {
  ls -l "${tmpdir}"
  rm -rf "${tmpdir}"
}
trap cleanup EXIT

export PYENV_VIRTUALENV_DISABLE_PROMPT=1

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pip install -r requirements.txt -t "${tmpdir}" -U
rm -rf dist
python setup.py sdist
pip install -U --no-deps -t "${tmpdir}" dist/*
(
    cd "${tmpdir}"
    find . -name "*.pyc" -delete
    rm -fr setuptools*
    rm -f ../package.zip
    zip -q -r ../package.zip .
) > /dev/null
