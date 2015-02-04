# DirectoryOfRepositories

To install, clone [this](https://github.com/mfraezz/DirectoryOfRepositories) repository and run:

```bash
pip install -Ur requirements.txt
```

To build the database, run:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py buildtables
```

Then, to start the server:

```bash
python manage.py runserver
```

Alternatively, if the database is broken or nonexistant, run:

```bash
sh clean_build.sh
```

which will delete the database, make a new one, and start the server
