FROM python:3.7
WORKDIR /tmp/
RUN apt-get update \
    && apt-get install -y libldap2-dev libsasl2-dev \
    && apt-get install -y postgresql-client \
    && apt-get install -y npm \
    && apt-get install -y pipenv \
    && apt-get clean
COPY docker/django/django_init /usr/local/bin
WORKDIR /opt/happyschool
COPY Pipfile .
COPY package.json .
RUN pipenv install
CMD ["/usr/local/bin/django_init"]
