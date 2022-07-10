#!/bin/sh


# echo "Initializing postgres db..."

# while ! nc -z $DB_HOST $DB_PORT; do
#   sleep 1
# done

python manage.py makemigrations 
python manage.py migrate

gunicorn contacts_project.wsgi:application --workers 10 --bind [::]:8001 --timeout 7200 

exec "$@"
