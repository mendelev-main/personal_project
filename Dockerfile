FROM python:3.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip3 install poetry

COPY  ./pyproject.toml ./poetry.lock ./
RUN poetry install

COPY ./weatherbot ./weatherbot
ENTRYPOINT ["poetry", "run"]
