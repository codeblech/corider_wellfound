FROM python:3.10-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . .

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]