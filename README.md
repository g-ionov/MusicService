#Music Service
This project provides a music service API created using Django REST Framework, Celery with Redis and Docker for containerization.
The user module is covered by tests.
This API also provides the ability to authenticate with OAuth2, JWT token and session.


The following commands must be executed to install the project:
```
git clone https://github.com/g-ionov/MusicService.git
cd MusicService
docker-compose build
docker-compose up
```

At the first startup you must execute the following commands:
```
docker-compose run --rm web-app sh -c "python manage.py makemigrations"
docker-compose run --rm web-app sh -c "python manage.py migrate"
docker-compose run --rm web-app sh -c "python manage.py createsuperuser"
```

To avoid writing such long commands, you can use the terminal of the web-app service inside Docker Desctop.
In this case, the commands will look like this:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

The default setting of this project is DEBUG=True, which can be changed to False. In this case you should also change the dev server to prod.
