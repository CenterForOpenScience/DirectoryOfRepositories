# DirectoryOfRepositories

To install, clone [this](https://github.com/mfraezz/DirectoryOfRepositories) repository and run:

<code> pip install -Ur requirements.txt </code>

To build the database, run:

<code>
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py buildtables
</code>

Then, to start the server:

<code>
python manage.py runserver
</code>

Alternatively, if the database is broken or nonexistant, run:

<code>
sh clean_build.sh
</code>

which will delete the database, make a new one, and start the server
