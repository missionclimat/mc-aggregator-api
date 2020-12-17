#!/bin/bash

echo "Collecting static files"
python manage.py collectstatic --no-input --clear


exec "$@"