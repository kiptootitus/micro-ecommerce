#!/bin/sh

if [ "$DATABASE" = "naruto" ]
then
    echo "Waiting for tutorial..."
    while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
      sleep 0.1
    done
    echo "PostgresSQL started"
fi

python manage.py migrate

exec "$@"