FROM python:3.12

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

# Copy source code
COPY /src /app/
COPY infra/entrypoint.sh .

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root
ENTRYPOINT ["bash", "entrypoint.sh"]
ENV RUN_BOT true

CMD ["poetry", "run", "uvicorn", "core.asgi_prod:application", "--reload", "--lifespan", "on", "--host", "0.0.0.0", "--port", "8000"]
