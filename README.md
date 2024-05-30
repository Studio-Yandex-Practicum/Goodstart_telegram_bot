# Goodstart_telegram_bot

Чат-бот в Телеграм для удобного и эффективного взаимодействия преподавателей и учеников онлайн школы.
CMS для управления пользователями и расписанием.

# Содержание

1. [ТЗ](https://docs.google.com/document/d/1VUSzwJ_7xS27LN53y2hdO5wPQ6rMDnPr/edit)

   1.1. [ER - диаграмма сущностей](docs/Goodstart%20ER%20diagram.jpg)

   1.2. [Схема работы бота (в разработке)](https://miro.com/app/board/uXjVKTz7zLw=/)

   1.3. [BPMN диаграмма (кейс регистрации пользователя)](docs/bpmn/registration.jpg)

   1.4. [BPMN диаграмма (кейс взаимодействия с преподавателем)](docs/bpmn/teacher_interaction.jpg)

2. [Используемые технологий](#technologies-project)

3. [Правила работы с git](#git)

4. [Получение SSL сертификатов для разработки](#ssl)

## Используемые технологии<a id="technologies-project"></a>:

![Python 3.12](https://img.shields.io/badge/Python-3.12-brightgreen.svg?style=flat&logo=python&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-brightgreen.svg?style=flat&logo=poetry&logoColor=white&color=blue)
![Pre-commit](https://img.shields.io/badge/pre--commit-brightgreen.svg?style=flat&logo=pre-commit&logoColor=white&color=blue)
![Python-telegram-bot 21.1.1](https://img.shields.io/badge/python--telegram--bot-21.1.1-brightgreen.svg?style=flat&logo=python&logoColor=white)
![Django 5.0.4](https://img.shields.io/badge/Django-5.0.4-brightgreen.svg?style=flat&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-brightgreen.svg?style=flat&logo=docker&logoColor=white&color=blue)
![Postgres](https://img.shields.io/badge/Postgres-brightgreen.svg?style=flat&logo=postgresql&logoColor=white&color=blue)
![Redis](https://img.shields.io/badge/Redis-brightgreen.svg?style=flat&logo=redis&logoColor=white&color=blue)


## Правила работы с git<a id="git"></a>:

1. Основные ветки:
- `master` - "продуктовая" версия кода.
- `dev` — “предрелизная” ветка, в которой должен находиться рабочий и проверенный код.
2. Создавая новую ветку, наследуйтесь от ветки `dev`:
    ```
    git checkout dev
    ```
    ```
    git checkout -b имя_новой_ветки
    ```
3. Правила именования веток
   - разработка нового функционала:
     ```
     git checkout -b feature/название_функционала
     ```
   - ловля и исправление багов:
     ```
     git checkout -b bugfix/название_багфикса
     ```
4. Прежде чем смержить ветку нового функционала/багфикса
с веткой `dev`, запуште её в репозиторий и инициируйте <b>Pull Request</b>:
- вкладка <b>Pull requests</b> репозитория на <b>GitHub</b> -> <b>New pull request</b>.
- необходимо указать целевую ветку и исходную ветку для изменений.


## Получение SSL сертификатов для разработки<a id="ssl"></a>:

Для начала нужно убедиться, что в `.env` задана переменная `BASE_URL=https://127.0.0.1:8000`

1. Установить [mkcert](https://github.com/FiloSottile/mkcert). Для прльзователей Windows используется `choco`.
2.  Командой `make create-ssl` создать сертификаты.
3. Теперь локальный сервер имеет доверенный сертификат и никаких ошибок и предупреждений о "мошеннических" действиях не появляется.
