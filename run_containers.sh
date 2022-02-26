#! /usr/bin/env sh

set -e
docker-compose build
docker-compose down -v --remove-orphans
docker-compose up -d