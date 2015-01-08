#!/usr/bin/sh
sudo rm -rf dor/migrations/*
rm -rf db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py index_terms
