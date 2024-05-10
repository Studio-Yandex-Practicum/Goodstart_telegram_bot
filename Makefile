# Определение переменных
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
MANAGE_DIR := $(PROJECT_DIR)/src/manage.py
DJANGO_DIR := $(PROJECT_DIR)/src
POETRY_RUN := poetry run python
DJANGO_RUN := $(POETRY_RUN) $(MANAGE_DIR)
DEV_DOCK_FILE := $(PROJECT_DIR)/infra/dev/docker-compose_local.yaml
SHELL_GREEN = \033[32m
SHELL_YELLOW = \033[33m
SHELL_NC := \033[0m


# Команда выполняемая по умолчанию.
.DEFAULT_GOAL := help


# Вызов документации.
help:
	@echo "$(SHELL_YELLOW)Список полезных функций:$(SHELL_NC)"
	@echo "	init-app        - $(SHELL_GREEN)Команда для автоустановки статики, миграций и регистрации супер-юзера.$(SHELL_NC)"
	@echo "	start-db        - $(SHELL_GREEN)Команда для запуска локального контейнера postgres.$(SHELL_NC)"
	@echo "	stop-db         - $(SHELL_GREEN)Команда для остановки локального контейнера postgres.$(SHELL_NC)"
	@echo "	clear-db        - $(SHELL_GREEN)Команда для очистки volume локального контейнера postgres.$(SHELL_NC)"
	@echo "	run             - $(SHELL_GREEN)Команда для локального запуска проекта.$(SHELL_NC)"
	@echo "	help            - $(SHELL_GREEN)Команда вызова справки.$(SHELL_NC)"
	@echo "$(SHELL_YELLOW)Для запуска исполнения команд используйте данные ключи совместно с командой 'make', например 'make init-app'."
	@echo "При запуске команды 'make' без какого либо ключа, происходит вызов справки.$(SHELL_NC)"


# Подготовка проекта к локальному запуску
init-app: collectstatic migrate createsuperuser


# Сбор статических файлов проекта.
collectstatic:
	cd $(PROJECT_DIR) && $(DJANGO_RUN) collectstatic --no-input


# Применение собранных миграций к базе данных, на основе сформированных моделей.
migrate:
	cd $(PROJECT_DIR) && $(DJANGO_RUN) migrate --no-input


# Создание новых миграций на основе сформированных моделей.
makemigrations:
	cd $(PROJECT_DIR) && $(DJANGO_RUN) makemigrations --no-input


# Создание супер-юзера.
createsuperuser:
	cd $(PROJECT_DIR) && $(DJANGO_RUN) createsuperuser --no-input


create_test_admins:
	cd $(PROJECT_DIR) && $(DJANGO_RUN) create_test_admins


# Запуск локального контейнера Postgres
start-db:
	docker-compose -f $(DEV_DOCK_FILE) up -d; \
	if [ $$? -ne 0 ]; \
    then \
        docker compose -f $(DEV_DOCK_FILE) up -d; \
    fi

# Остановка контейнера Postgres
stop-db:
	docker-compose -f $(DEV_DOCK_FILE) down; \
	if [ $$? -ne 0 ]; \
    then \
		docker compose -f $(DEV_DOCK_FILE) down; \
	fi

# Очистка БД Postgres
clear-db:
	docker-compose -f $(DEV_DOCK_FILE) down --volumes; \
	if [ $$? -ne 0 ]; \
    then \
		docker compose -f $(DEV_DOCK_FILE) down --volumes; \
	fi


# Локальный запуск сервера разработки.
run:
	cd $(PROJECT_DIR) && $(DJANGO_RUN) runserver
