FROM python:3.12.4-slim-bookworm
WORKDIR /ai_blog
# Copying shell scripts
COPY compose/local/ ./

COPY ./src/ ./

COPY requirements.txt ./


RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get -y install gcc \
    && pip install psycopg2

# Poetry is inconvinient to use in docker. Run pip freeze > requirements.txt before running docker-compose up
RUN pip install -r requirements.txt

RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod 777 ./entrypoint.sh

RUN sed -i 's/\r$//g' start
RUN chmod 777 ./start
ENTRYPOINT ["./entrypoint.sh"]
