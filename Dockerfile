FROM python:3.11-alpine

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN apk add gcc libc-dev libffi-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./src /code/src
COPY ./alembic /code/alembic
COPY ./alembic.ini /code/alembic.ini
COPY ./fixtures /code/fixtures
COPY ./loadfixtures.py /code/loadfixtures.py
COPY ./add_user_to_role.py /code/add_user_to_role.py
COPY ./certs /code/certs
COPY ./docker.env /code/.env
COPY ./docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY ./load_demo_data.py /code/load_demo_data.py

RUN sed -i 's/\r$//g' /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin//docker-entrypoint.sh
