#!/usr/bin/env bash

set -e
[ -n "$DEBUG" ] && set -x

env_name=${MENHIR_PROJECT}

export PYENV_VIRTUALENV_DISABLE_PROMPT=1

if command -v pyenv; then
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"

    pyenv activate "${env_name}"
fi

pytest "$@"
