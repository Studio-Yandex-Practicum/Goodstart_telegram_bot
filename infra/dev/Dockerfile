FROM python:3.12

ENV PYTHONUNBUFFERED=1 \
POETRY_HOME="/opt/poetry" \
POETRY_VIRTUALENVS_IN_PROJECT=true \
POETRY_NO_INTERACTION=1 \
PYSETUP_PATH="/opt/pysetup" \
VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry install

RUN . .venv/bin/activate

RUN poetry update

RUN poetry export -f requirements.txt > requirements.txt

RUN pip install -r requirements.txt

COPY . .

# При старте контейнера запустить сервер разработки.
CMD ["poetry", "run", "uvicorn", "core.asgi_dev:application", "--reload"]
