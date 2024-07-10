# ai-moderated-blog

## Important!

Gemini API doesnt work in Ukrainian region, thus if you want to test out the ai functionality, you need to use a VPN.
Personally, I used ClearVPN because it gives free premium tier for forever for auth'ing with diia.
Tested in Turkish region.

The regions with free gemini api tier are listed without ```[1]``` mark here: https://ai.google.dev/gemini-api/docs/available-regions

Keep in mind that response time can be slow due to the reasons described earlier.

## Table of Contents
- [Introduction](#introduction)
- [Setup](#setup):
  - [Manual](#manual)
  - [Docker](#docker) (Preferred)
- [Usage](#usage)

## Introduction
This project was made using Django, djano-ninja, django-ninja-extra, pydantic, gemini api, celery, redis, postgres.
Tested with pytest, pytest-django, faker.
While developing pre-commits, linters, and formatters were used.

## Setup
### Manual
1. Clone the repository
2. Download poetry for virtual environment management (https://python-poetry.org/docs/)
3. Install Python 3.12
4. Install redis server
5. Install postgres
6. Create a database in postgres named `ai_blog`
7. Run poetry install in the root directory
8. Start the virtual environment with `poetry shell`
8. Run `python manage.py migrate`
9. Run `python manage.py createsuperuser` to create admin
10. Run `python manage.py runserver` to start the server
11. Run `redis-server` to start redis server
12. Run `celery -A api worker --pool solo -l info` in src folder
13. Ensure that POSTGRES_HOST is set to `localhost` in the .env file

Run tests with `pytest`

### Docker
1. Clone the repository
2. Ensure that docker and docker compose are installed
3. Run `docker-compose -f local.yml up` in the root directory
4. Run `docker-compose -f tests.yml up` in the root directory to run tests

## Usage
Visit `http://localhost:8000/api/docs` to view the API documentation

- Most resources (like POST/PUT/DELETE) are protected and require authentication. To authenticate, use /auth/login, copy the access token and insert in Authorize

- Admin is created by default if using docker. It's credentials are: ```admin@gmail.com, 1234```

- PUT / DELETE requests require the user to be either an admin or the author of the protected subject

- Analytics can be run only by an admin, thus login as an admin is required
- You can see request schemas at the bottom of the page, they describe which fields are required and which are not. If the field is not required, you can simply delete it from try request or set to null.
