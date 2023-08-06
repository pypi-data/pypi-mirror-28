#!/usr/bin/env bash

# Script to build the docker image

set -e
[ -n "$DEBUG" ] && set -x

hash aws || {
      printf "Install the AWS CLI, e.g. with \`brew install awscli\`\n"
      exit 1
}

docker build -t "${MENHIR_TAG}" "$@" .
