FROM python:3.12

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

# Copy source code
COPY src/. /app/

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root


RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure locales

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

CMD ["poetry", "run", "uvicorn", "core.asgi_prod:application", "--lifespan", "on", "--host", "0.0.0.0", "--port", "8000"]
