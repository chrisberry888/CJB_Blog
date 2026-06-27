#!/bin/sh
set -e

: "${SQLITE_PATH:=/app/data/db.sqlite3}"
: "${DJANGO_MEDIA_ROOT:=/app/media}"
: "${DJANGO_STATIC_ROOT:=/app/staticfiles}"

export SQLITE_PATH DJANGO_MEDIA_ROOT DJANGO_STATIC_ROOT

mkdir -p "$(dirname "$SQLITE_PATH")" "$DJANGO_MEDIA_ROOT" "$DJANGO_STATIC_ROOT"

if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
    python manage.py migrate --noinput
fi

if [ "${COLLECT_STATIC:-1}" = "1" ]; then
    python manage.py collectstatic --noinput
fi

if [ "${SEED_INITIAL_DATA:-0}" = "1" ]; then
    python manage.py seed_initial_data
fi

exec "$@"
