# Mkdev2
How to start it?

1. git clone https://github.com/Valk-99/my_1.git
2. add file ".env.dev" in base project(mkdev)
3. what you need to write in .env.dev file?

DEBUG=1 <br>
SECRET_KEY=foo<br>
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]<br>
SQL_ENGINE=django.db.backends.postgresql<br>
SQL_DATABASE_NAME= your db name<br>
SQL_USER= your db user<br>
SQL_PASSWORD= your db password<br>
SQL_HOST= db<br>
SQL_PORT= 5432<br>
DATABASE= postgres<br>

4. run Dockerfile and docker-compose
