FROM python:3.11
WORKDIR /tmp/
RUN apt-get update \
    && apt-get install -y libldap2-dev libsasl2-dev \
    && apt-get install -y postgresql-client \
    && apt-get clean
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
RUN apt-get install -y nodejs
COPY docker/django/django_init.sh /usr/local/bin
WORKDIR /opt/happyschool
COPY pyproject.toml .
COPY package.json .
RUN npm install
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN ~/.local/bin/uv sync
CMD ["/usr/local/bin/django_init.sh"]
