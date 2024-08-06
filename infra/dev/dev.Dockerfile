FROM python:3.12

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

# Copy source code
COPY src/. /app/

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root

CMD ["poetry", "run", "uvicorn", "core.asgi_prod:application", "--lifespan", "on", "--host", "0.0.0.0", "--port", "8000"]
