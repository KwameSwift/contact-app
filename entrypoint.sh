#!/bin/sh


# echo "Initializing postgres db..."

# while ! nc -z $DB_HOST $DB_PORT; do
#   sleep 1
# done

python manage.py makemigrations 
python manage.py migrate

# python manage.py runserver [::]:80

# touch logs/gunicorn/error.log
# touch logs/gunicorn/access.log

# gunicorn aegis_root_project.wsgi:application \
# --workers 10 \
# --bind [::]:8000 \
# --timeout 1800 \
# --error-logfile logs/gunicorn/error.log \
# --access-logfile logs/gunicorn/access.log

gunicorn contacts_project.wsgi:application --workers 10 --bind [::]:7000 --timeout 7200 

# nginx -g daemon off

# echo "postgres database has initialized successfully"

# docker tag aegisbackenddev:latest aegiscontainerregistry.azurecr.io/aegis-rider-development:latest
# docker push aegiscontainerregistry.azurecr.io/aegis-rider-development:latest

exec "$@"
