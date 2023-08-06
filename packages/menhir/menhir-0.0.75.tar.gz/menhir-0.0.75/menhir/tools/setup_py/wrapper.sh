#!/usr/bin/env bash

# Wrapper to activate pyenv

if command -v pyenv > /dev/null; then
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
fi

exec "$@"
