#!/bin/sh

set -e

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" "$POSTGRES_DB" -c '\l'; do
	echo "Waiting for PostgreSQL to get ready..." && sleep 1
done

/home/app/src/coronavirus/manage.py collectstatic --no-input
/home/app/src/coronavirus/manage.py migrate
exec "$@"
