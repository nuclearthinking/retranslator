FROM python:3.10.6-slim-bullseye

RUN mkdir /app \
    && apt update \
    && pip install -U pip \
    && pip install poetry 

WORKDIR /app

COPY [ \
  "poetry.lock", \
  "pyproject.toml", \
  "/app/"]

RUN poetry config virtualenvs.create false \
  && poetry config installer.parallel false \
  && poetry install --no-dev --no-interaction --no-ansi 


COPY . /app

CMD ["python", "src/retranslator/app.py", "start"]