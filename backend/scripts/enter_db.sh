#!/bin/bash

# scb-db must be running
docker exec -it scb-db psql sleepy-cat-books -U postgres
