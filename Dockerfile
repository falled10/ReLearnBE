FROM python:3.8


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


ADD ./requirements.txt /usr/src/app/requirements.txt


RUN pip install -r requirements.txt


ADD . /usr/src/app


CMD uvicorn --host 0.0.0.0 --port 8000 main:app