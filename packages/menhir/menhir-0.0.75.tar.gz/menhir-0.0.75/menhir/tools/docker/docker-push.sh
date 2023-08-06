#!/usr/bin/env bash

# Script to deploy the docker image

set -e
[ -n "$DEBUG" ] && set -x

hash aws || {
      printf "Install the AWS CLI, e.g. with \`brew install awscli\`\n"
      exit 1
}

docker tag "${MENHIR_TAG}" "${MENHIR_BRANCH_TAG}"
docker tag "${MENHIR_TAG}" "${MENHIR_SHA_TAG}"

# log into docker registry
# shellcheck disable=2091
printf "Pushing %s\n" "${MENHIR_BRANCH_TAG}"
docker push "${MENHIR_BRANCH_TAG}"
printf "Pushing %s\n" "${MENHIR_SHA_TAG}"
docker push "${MENHIR_SHA_TAG}"
