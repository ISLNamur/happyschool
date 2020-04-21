#!/bin/bash

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d 'template1' -c 'CREATE EXTENSION unaccent;'
