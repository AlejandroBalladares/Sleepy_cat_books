#! /usr/bin/env bash
set -e
set -x

export AUTOMATED_TESTS=1

coverage run --source=app -m pytest app/
coverage report --show-missing
coverage html --title "${@-coverage}"