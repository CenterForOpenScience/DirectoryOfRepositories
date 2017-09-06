#!/usr/bin/sh
sudo rm -rf dor/migrations
rm -rf db.sqlite3
mkdir dor/migrations
touch dor/migrations/__init__.py
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py buildtables
python manage.py runserver
