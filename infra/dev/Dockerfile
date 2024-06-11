FROM python:3.12

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

# Copy source code
COPY /src /app/

RUN poetry install
WORKDIR /app

CMD ["poetry", "run", "uvicorn", "core.asgi_dev:application", "--reload", "--lifespan", "on", "--host", "0.0.0.0", "--port", "8000"]
