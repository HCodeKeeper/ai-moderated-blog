FROM python:3.12.4-slim-bookworm
WORKDIR /ai_blog

COPY src/* ./

COPY requirements.txt ./

ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # Install poetry
  && pip install --no-cache-dir poetry

# Copy pyproject.toml
COPY pyproject.toml ./

# Install dependencies using poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

#RUN apt-get update \
#  && apt-get install --no-install-recommends -y \
#    libpq-dev \
#    gettext \
#  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
#  && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get -y install gcc \
    && pip install psycopg2 \
    && pip install --no-cache-dir poetry

RUN pip install --upgrade pip




# Poetry is inconvinient to use in docker. Run pip freeze > requirements.txt before running docker-compose up

# Copying shell scripts
COPY ./compose/local/entrypoint.sh ./entrypoint.sh
COPY ./compose/local/start ./start


RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod 777 ./entrypoint.sh

RUN sed -i 's/\r$//g' start
RUN chmod 777 ./start
