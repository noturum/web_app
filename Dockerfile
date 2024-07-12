FROM python:latest
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
WORKDIR /web_app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /web_app
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]