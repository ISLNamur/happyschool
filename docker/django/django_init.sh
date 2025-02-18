#!/bin/bash

cd /opt/happyschool

(( MAX_RETRIES=30 ))
(( CPT=0 ))
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -c "\q"; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 5
    (( CPT ++ ))
    (( CPT == MAX_RETRIES )) && exit 1
done

PATH=$PATH:~/.local/bin

if [ ! -d "/opt/happyschool/static/" ]; then
    uv run python3 manage.py migrate
    uv run python3 manage.py creategroups;
    uv run python3 manage.py shell -c 'from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser("admin", "admin@localhost", "admin")'
fi

uv run python3 manage.py runserver 0.0.0.0:8000 

