#!/bin/bash
set -e
[ -n "$DEBUG" ] && set -x

set -x

coverage xml -i

bash <(curl -s https://codecov.io/bash) \
     -cF "${MENHIR_CODECOV_FLAGS}" \
     -f "$(pwd)/coverage.xml"
