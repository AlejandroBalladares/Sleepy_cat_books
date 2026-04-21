#!/bin/bash

set -e
set -x

msg=$1
container_name="scb-revision-db"

if [[ -z "${msg}" ]]; then
    echo "Please provide a message to create the revision"
    echo "Usage: ./add_revision.sh \"<message>\""
    exit 1
fi

export REVISION_DB=1

docker run --rm --detach -p 5432:5432 --env-file ../.env --name "${container_name}" postgres:17.0-alpine3.20 || exit 1

timeout 10s bash -c "until docker exec ${container_name} pg_isready ; do sleep 2 ; done" || exit 1

alembic upgrade head || (docker stop "${container_name}" && exit 1)

alembic revision --autogenerate -m "${1}" || (docker stop "${container_name}" && exit 1)

docker stop "${container_name}"
