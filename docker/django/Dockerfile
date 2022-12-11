FROM python:3.8
WORKDIR /tmp/
RUN apt-get update \
    && apt-get install -y libldap2-dev libsasl2-dev \
    && apt-get install -y postgresql-client \
    && apt-get clean
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
RUN apt-get install -y nodejs
COPY docker/django/django_init /usr/local/bin
WORKDIR /opt/happyschool
COPY Pipfile .
COPY package.json .
RUN python3 -m pip install pipenv
RUN pipenv install
CMD ["/usr/local/bin/django_init"]
