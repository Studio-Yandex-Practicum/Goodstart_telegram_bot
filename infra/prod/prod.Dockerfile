FROM python:3.12

WORKDIR /app

COPY requirements/prod.txt .
RUN pip install -r prod.txt --no-cache-dir

# Copy source code
COPY . .

WORKDIR ./src

RUN export RUN_BOT=true

CMD ["uvicorn", "core.asgi_prod:application", "--lifespan", "on", "--host", "0.0.0.0", "--port", "8000"]
