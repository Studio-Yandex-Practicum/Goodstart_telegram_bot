# Goodstart_telegram_bot

Чат-бот в Телеграм для удобного и эффективного взаимодействия преподавателей и учеников онлайн школы.
CMS для управления пользователями и расписанием.

# Содержание

1. [ТЗ](https://docs.google.com/document/d/1VUSzwJ_7xS27LN53y2hdO5wPQ6rMDnPr/edit)

   1.1. [ER - диаграмма сущностей](docs/Goodstart%20ER%20diagram.jpg)

   1.2. [Схема работы бота (в разработке)](https://miro.com/app/board/uXjVKTz7zLw=/)

   1.3. [BPMN диаграмма (кейс регистрации пользователя)](docs/bpmn/registration.jpg)

   1.4. [BPMN диаграмма (кейс взаимодействия с преподавателем)](docs/bpmn/teacher_interaction.jpg)

   1.5. [BPMN диаграмма (кейс взаимодействия с учеником)](docs/bpmn/student_interaction.jpg)

2. [Используемые технологий](#technologies-project)

3. [Правила работы с git](#git)

4. [Получение SSL сертификатов для разработки](#ssl)

5. [Конфигурация админ панели на основе django-admin-material](#dma)

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


## Установка проекта на LINUX(на примере Ubuntu 22.04/WSL)
1. Перейдите в свою директорию с проектами
  ```
  cd ~/<path_to_dev_directory>
  ```
  где <path_to_dev_directory> - название вашей директории с проектами.
  Либо, если у вас она расположена в ином месте, то пропишите необходимый путь
  ```
  cd /path/to/dev/directory
  ```

2. Клонируйте репозиторий с проектом
  ```
  git clone git@github.com:Studio-Yandex-Practicum/Goodstart_telegram_bot.git
  ```

3. Перейдите в домашнюю директорию
  ```
  cd ~
  ```

4. Необходимо проверить установленную версию Python.
  ```
  python3 -V
  ```
  Если у вас версия 3.12.*, то можно переходить к шагу 6.

5. Если версия не 3.12.*, то необходимо её установить. Мы рекомендуем использовать
  pyenv, на его примере и рассмотрим установку дополнительной версии.
  Необходимо установить pyenv.
  ```
  sudo apt update
  ```
  ```
  curl https://pyenv.run | bash
  ```
  Ожидайте окончания установки.
  Добавьте следующие строки в ваш файл ~/.bashrc (если вы используете Bash)
  или в ~/.zshrc (если вы используете Zsh). Если они там уже есть(или похожие),
  то можно пропустить шаг.
  Открыть файл
  ```
  nano ~/.bashrc
  ```
  Эти строки скопировать и добавить в конец файла
  ```
  export PATH="$HOME/.pyenv/bin:$PATH"
  eval "$(pyenv init --path)"
  ```
  Эти строки должны работать в большинстве случаев, если же что-то пошло не так - 
  почитайте документацию.
  Перезапустите ваш терминал, либо выполните команду в терминале(если используете bash)
  ```
  source ~/.bashrc
  ```
  чтобы изменения вступили в силу.
  Проверьте, что pyenv установлен правильно.
  ```
  pyenv --version
  ```
  Если терминал вывел в ответ 'pyenv 2.4.3'(цифры могут отличаться), то всё сделано верно.
  Теперь необходимо в pyenv установить нужную версию Python, например, 3.12.4
  ```
  pyenv install 3.12.4
  ```
  Проверяем, что нужная версия установлена
  ```
  pyenv versions
  ```
  Если терминал вывел список примерно такого содержания и в нём есть указанная
  ранее версия - всё сделано правильно.
  ```
  * system (set by /home/user/.pyenv/version)
  3.9.19
  3.12.4
  ```

6. Необходимо создать виртуальное окружение проекта.
  Перейдите в директорию проекта Goodstart.
  ```
  cd ~/path/to/dir/Goodstart_telegram_bot
  ```
  Если у вас была подходящая версия Python и вы пропустили шаг 5, то сразу
  приступайте к созданию окружения
  ```
  pip install poetry
  ```
  ```
  poetry shell
  ```
  ```
  poetry install
  ```
  Дождитесь окончания установки. Если всё прошло удачно, то ваш терминал будет
  ожидать ввод примерно с таким текстом '(poetry-goodstart-py3.12) user@pc:'

  Если у вас не было подхлдящей версии Python и вы устанавливали pyenv, то назначьте
  локальную(для проекта) версию Python из pyenv
  ```
  pyenv local 3.12.4
  ```
  В корневой директории вашего проекта должен появиться файл '.python-version',
  в котором будет строка с версией.
  Теперь можно установить зависимости
  ```
  pip install poetry
  ```
  ```
  poetry shell
  ```
  ```
  poetry install
  ```
  Дождитесь окончания установки. Если всё прошло удачно, то ваш терминал будет
  ожидать ввод примерно с таким текстом '(poetry-goodstart-py3.12) user@pc:'

7. Создайте файл с переменными окружения '.env' в корне проекта. Структура файла:
  ```
   # Название, логин и пароль для БД postgres
   POSTGRES_DB=postgres <-- это значение можно поменять
   POSTGRES_USER=postgres <-- это значение можно поменять
   POSTGRES_PASSWORD=postgres <-- это значение можно поменять
   DB_ENGINE=django.db.backends.postgresql_psycopg2
   # Данные для подключения к БД
   DB_HOST=localhost
   DB_PORT=5432

   # Переменные Django
   # Базовый URL
   BASE_URL=https://127.0.0.1:8000
   # ПРЕДУПРЕЖДЕНИЕ: Хранить секретный ключ не должен попадать в общий доступ
   SECRET_KEY=top_secret_key <-- это значение можно поменять
   # ПРЕДУПРЕЖДЕНИЕ: Debug = true использовать только при разработке
   DEBUG=false <-- это значение можно поменять
   # Список разрешенных хостов
   ALLOWED_HOSTS=localhost,127.0.0.1
   CSRF_TRUSTED_ORIGINS=https://yourdomain.org

   # Переменные бота
   # Токен для подключения к Telegram API
   TELEGRAM_TOKEN=<bot_token> <-- здесь должен быть ваш токен

   # Конфигурация superuser django
   DJANGO_SUPERUSER_USERNAME=admin <-- это значение можно поменять
   DJANGO_SUPERUSER_EMAIL=admin@ad.ad <-- это значение можно поменять
   DJANGO_SUPERUSER_PASSWORD=admin <-- это значение можно поменять
   DJANGO_SUPERUSER_FIRSTNAME=Admin <-- это значение можно поменять
   DJANGO_SUPERUSER_LASTNAME=User <-- это значение можно поменять
   DJANGO_SUPERUSER_PHONE=+74950000000

   # Конфигурация почтового агента
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   EMAIL_HOST=smtp.yandex.ru
   EMAIL_PORT=465
   # реквизиты для аутентификации в почтовом сервисе
   EMAIL_ACCOUNT=your_email@yandex.ru
   EMAIL_PASSWORD=your_yandex_smtp_password
   # в настройках аккаунта откуда отправляется письмо подключите протокол IMAP
   # адрес по умолчанию для отправки вопросов от пользователей
   DEFAULT_EMAIL_ADDRESS=NOT_SET
   # Запустить бота
   RUN_BOT=false <-- для локального запуска значение должно быть false
  ```

8. Установите mkcert
  ```
  sudo apt install mkcert
  ```
  Дождитесь окончания установки. Проверьте:
  ```
  mkcert --version
  ```
  Если терминал ответил '1.4.3'(цифры могут отличаться), то всё сделано верно.

9. Установите сертификаты. Из корневой директории проекта
  ```
  make create-ssl
  ```
  В ответе терминала, помимо прочего, должны быть строки
  ```
  Created a new certificate valid for the following names 📜
  - "localhost"
  - "127.0.0.1"

  The certificate is at "cert.pem" and the key at "key.pem" ✅
  ```
  Также в директории Goodstart_telegram_bot/infra/dev/ должны появится файлы
  cert.pem и key.pem. Если всё так, то можно переходить к следующему шагу.

10. Разверните проект. Из корневой директории проекта выполните команды
  ```
  make start-db
  ```
  Дождитесь сборки контейнера. Далее введите команду
  ```
  make init-app
  ```
  Дождитесь окончания всех процедур. Должны выполниться миграции и создаться 
  superuser. Далее введите команду
  ```
  make run-dev
  ```
  Эта команда запустит сервис, в терминале должен быть примерно такой вывод
  ```
    export RUN_BOT=true; cd /home/user/dev/Goodstart_telegram_bot/src && poetry run uvicorn core.asgi_dev:application --reload --ssl-keyfile=../infra/dev/key.pem --ssl-certfile=../infra/dev/cert.pem --lifespan on
    INFO:     Will watch for changes in these directories: ['/home/user/dev/Goodstart_telegram_bot/src']
    INFO:     Uvicorn running on https://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [43863] using StatReload
    2024-06-25 22:29:32.964 | INFO     | bot.bot_interface:__init__:44 - Bot instance created.
    2024-06-25 22:29:32.965 | INFO     | bot.bot_interface:start:48 - Bot starting...
    2024-06-25 22:29:32.966 | INFO     | bot.bot_interface:_run:90 - Bot event loop created and started.
    2024-06-25 22:29:32.966 | INFO     | bot.bot_interface:start:52 - Bot started in a new thread.
    INFO:     Started server process [43867]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    /home/user/dev/Goodstart_telegram_bot/src/bot/bot_interface.py:120: PTBUserWarning: If 'per_message=False', 'CallbackQueryHandler' will not be tracked for every message. Read this FAQ entry to learn more about the per_* settings: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Frequently-Asked-Questions#what-do-the-per_-settings-in-conversationhandler-do.
      return ConversationHandler
    2024-06-25 22:29:33.042 | INFO     | bot.bot_interface:_build_app:84 - Bot application built with handlers.
    2024-06-25 22:29:33.325 | INFO     | bot.bot_interface:_start_bot:104 - Bot is running.
  ```

11. Проверьте работоспособность проекта. В браузере перейдите по адресу
  ```
  https://localhost:8000/admin/
  ```
  Если https зачёркнуто и слева предупреждение 'Не защищено', то в центре страницы
  нажмите кнопку 'Дополнительные', затем ниже 'Перейти на сайт localhost (небезопасно)'.
  После этого вы должны увидеть форму входа в админпанель, туда можно попасть, если
  ввести данные админа из файла .env

  Проверьте работоспособность бота. Установите десктопную версию Telegram, в нём
  перейдите в бот, токен которого указали в файле .env. Нажмите START. Бот должен
  прислать приветственное сообщение, снизу должна появиться кнопка 'Открыть форму регистрации'.
  Кликните по ней. Если ранее у вас было предупреждение 'Не защищено', то в боте
  оно тоже будет. Снизу открывшегося окошка нажмите 'Дополнительные', затем
  'Перейти на сайт localhost (небезопасно)'. Должна открыться форма регистрации.


## Получение SSL сертификатов для разработки<a id="ssl"></a>:

Для начала нужно убедиться, что в `.env` задана переменная `BASE_URL=https://127.0.0.1:8000`

1. Установить [mkcert](https://github.com/FiloSottile/mkcert). Для прльзователей Windows используется `choco`.
2. Командой `make create-ssl` создать сертификаты.
3. Теперь локальный сервер имеет доверенный сертификат и никаких ошибок и предупреждений о "мошеннических" действиях не появляется.
4. Если Браузер ругается на сертификат (при этом серификат явно присутствует) выполнить `mkcert -install`, а затем снова п.2

## Конфигурация админ панели на основе django-admin-material<a id="dma"></a>:

Cписок всех настроек.

```
MATERIAL_ADMIN_SITE = {
'HEADER': _('Your site header'), # Admin site header
'TITLE': _('Your site title'), # Admin site title
'FAVICON': 'path/to/favicon', # Admin site favicon (path to static should be specified)
'MAIN_BG_COLOR': 'color', # Admin site main color, css color should be specified
'MAIN_HOVER_COLOR': 'color', # Admin site main hover color, css color should be specified
'PROFILE_PICTURE': 'path/to/image', # Admin site profile picture (path to static should be specified)
'PROFILE_BG': 'path/to/image', # Admin site profile background (path to static should be specified)
'LOGIN_LOGO': 'path/to/image', # Admin site logo on login page (path to static should be specified)
'LOGOUT_BG': 'path/to/image', # Admin site background on login/logout pages (path to static should be specified)
'SHOW_THEMES': True, # Show default admin themes button
'TRAY_REVERSE': True, # Hide object-tools and additional-submit-line by default
'NAVBAR_REVERSE': True, # Hide side navbar by default
'SHOW_COUNTS': True, # Show instances counts for each model
'APP_ICONS': { # Set icons for applications(lowercase), including 3rd party apps, {'application_name': 'material_icon_name', ...}
'sites': 'send',
},
'MODEL_ICONS': { # Set icons for models(lowercase), including 3rd party models, {'model_name': 'material_icon_name', ...}
'site': 'contact_mail',
}
}
```
Вот тут подробно показаны:
https://www.youtube.com/watch?v=_ifWi-a1z6M&ab_channel=AntonMaistrenko

## Деплой на сервер
1. Создать на сервере папку /home/username/Goodstart_telegram_bot
2. В папку Goodstart_telegram_bot положить: 
- заполненый файл .env (см. .env.example)
- файл docker-compose.dev.yaml
- папку infra\dev (с сохранением иерархии)
3. Запуск проекта
```
sudo docker compose -f docker-compose.dev.yaml up -d```
```
4. Остановка контейнера
```
sudo docker compose -f docker-compose.dev.yaml down
```
5. Создать суперпользователя
```
sudo docker compose -f docker-compose.dev.yaml exec backend export RUN_BOT=false
sudo docker compose -f docker-compose.dev.yaml exec backend python manage.py createsuperuser
```
## Настройка CD
В настройках репозитория (settings->secrets and variables->Actions->Repository secrets) настроить все переменные из .env.example