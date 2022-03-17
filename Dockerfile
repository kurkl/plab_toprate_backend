FROM python:3.10-buster as builder

WORKDIR /app

RUN apt-get -y update && \
    apt-get -y upgrade

COPY pyproject.toml poetry.lock ./
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN poetry install --no-root --no-dev

COPY ./app ./
ENV PYTHONPATH=.
CMD ["sh", "-c", "uvicorn app.main:get_app"]


FROM builder as dev

COPY ./tests ./tests

RUN poetry install --no-root
