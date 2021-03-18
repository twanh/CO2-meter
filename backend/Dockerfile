FROM python:3.9-slim

# Have this be cached
COPY requirements.txt /
RUN pip install -r /requirements.txt

ADD . /app
WORKDIR /app

ENV FLASK_ENV=production

ENTRYPOINT gunicorn -b 0.0.0.0:8008 app.__main__:flask_app

