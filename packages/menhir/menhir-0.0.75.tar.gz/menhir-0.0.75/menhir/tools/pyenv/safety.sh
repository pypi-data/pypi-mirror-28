#!/usr/bin/env bash

set -e
[ -n "$DEBUG" ] && set -x

export PYENV_VIRTUALENV_DISABLE_PROMPT=1

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

echo "Checking vulnerabilities..."
pip install -q -U safety
safety check
