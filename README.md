# Mkdev2
How to start it?

1. git clone https://github.com/Valk-99/my_1.git
2. add file ".env.dev" in base project(mkdev)
3. what you need to write in .env.dev file?

DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE_NAME= your db name
SQL_USER= your db user
SQL_PASSWORD= your db password
SQL_HOST= your db host
SQL_PORT= your db port
DATABASE= your db

4. run Dockerfile and docker-compose
