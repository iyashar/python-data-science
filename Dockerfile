# FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
# FROM tiangolo/uwsgi-nginx-flask:python3.7-alpine3.8
# FROM decibel/uwsgi-nginx-flask-docker:python3.7-alpine3.9-pandas
FROM tiangolo/uwsgi-nginx-flask


WORKDIR /app
COPY . /app


# ENV STATIC_INDEX 1
# ENV LISTEN_PORT 8080
# EXPOSE 8080

# ENV STATIC_URL /static
# ENV STATIC_PATH /app/static


RUN pip3 install --no-cache-dir -U pip
RUN pip3 install -r requirements.txt

