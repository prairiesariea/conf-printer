#!/bin/bash

declare -r  thisDir="$( dirname "$( readlink -f "${0}" )" )"

python "${thisDir}/../src/conf-printer.py" test "${@}"
