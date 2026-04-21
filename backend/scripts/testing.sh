#! /usr/bin/env bash
set -e
set -x

export TESTING=1

docker compose up sleepy-cat-books-backend --build
