FROM python:3.12-slim

EXPOSE 9000

RUN apt-get update \
    && apt-get install -y gettext git

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
COPY .env.example .env
RUN python manage.py collectstatic --noinput --no-post-process

RUN rm .env
RUN touch .env

RUN git log -1 --pretty='format:%h' HEAD > .git-rev-hash
RUN git log -1 --pretty='format:%ai' HEAD > .git-rev-date
RUN rm -rf .git

RUN apt purge -y git

CMD ["gunicorn", "project.wsgi", "-k" , "gevent", "-b", "0.0.0.0:9000"]
