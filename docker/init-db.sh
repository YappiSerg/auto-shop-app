#!/bin/sh
set -e

pg_restore \
  --dbname="$POSTGRES_DB" \
  --no-owner \
  --no-privileges \
  /docker-entrypoint-initdb.d/dataset.dump
