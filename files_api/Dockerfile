FROM python:3.8-slim-bullseye

RUN mkdir /app
ADD . /app
#ENV PYTHONPATH=/app
WORKDIR /app

ENV TZ=Europe/Bucharest

RUN pip install -r files_api/requirements.txt
RUN pwd
RUN ls .

CMD python events_api/main.py