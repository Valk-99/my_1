# pull official base image
FROM python:3.9.0-alpine
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1
# install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add libffi-dev openssl-dev cargo \
    && apk add jpeg-dev zlib-dev

RUN pip install --upgrade pip
RUN pip install pyyaml ua-parser user-agents
RUN pip install Pillow
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/bin/sh","/usr/src/app/entrypoint.sh"]
