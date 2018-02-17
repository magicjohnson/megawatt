#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput

# Prepare log files and start outputting logs to stdout
touch /project/logs/gunicorn.log
touch /project/logs/gaccess.log
tail -n 0 -f /project/logs/*.log &

echo Starting Gunicorn.
exec gunicorn megawatt.wsgi:application \
    --name hello_django \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --log-file=/project/logs/gunicorn.log \
    --access-logfile=/project/logs/access.log \
    "$@"
