FROM python:3.12

WORKDIR /app

COPY requirements/dev.txt .
RUN pip install -r dev.txt --no-cache-dir

# Copy source code
COPY . .

WORKDIR ./src

RUN export RUN_BOT=true

CMD ["uvicorn", "core.asgi_dev:application", "--lifespan", "on", "--host", "0.0.0.0", "--port", "8000"]
