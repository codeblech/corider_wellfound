# syntax=docker/dockerfile:1
FROM python:3.10-slim

# for gcc, cryptographic dependincies, c extensions
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -


WORKDIR /app
COPY . /app

# Virtual environment not needed
RUN poetry config virtualenvs.create false
RUN poetry install $(test "$FLASK_ENV" == production && echo "--only=main") --no-interaction --no-ansi

# Expose the port your Flask app runs on
EXPOSE 8000

# Define the command to run your application
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
