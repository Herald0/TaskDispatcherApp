# Task Dispatcher — FastAPI приложение

Приложение для управления задачами с авторизацией по JWT, веб-интерфейсом, и каналом WebSocket для обновлений в реальном времени.

**Ключевые возможности**
- Авторизация и регистрация пользователей: [users.py](/app/api/endpoints/users.py)
- CRUD операций над задачами: [tasks.py](/app/api/endpoints/tasks.py)
- Защищённая страница со списком задач: [main.py](/main.py)
- WebSocket-канал для рассылки событий: [websocket.py](app/api/endpoints/websocket.py)
- UI-страницы и статика: [templates](app/templates), [static](app/static)

**Структура проекта**
- Приложение: [main.py](/main.py)
- Эндпоинты: [users.py](/app/api/endpoints/users.py), [tasks.py](/app/api/endpoints/tasks.py), [websocket.py](/app/api/endpoints/websocket.py)
- Модели БД: [models.py](/app/db/models.py), сессия: [database.py](/app/db/database.py)
- Конфиг и секреты: [config.py](/app/core/config.py), [security.py](/app/core/security.py)
- Миграции Alembic: [alembic.ini](/alembic.ini), [env.py](/alembic/env.py)
- Тесты: [tests](/tests)

## Переменные окружения
Задаются через `.env`.

- `DB_HOST` — хост базы данных
- `DB_PORT` — порт базы данных
- `DB_USER` — пользователь БД
- `DB_PASS` — пароль пользователя
- `DB_NAME` — имя базы

## Локальный запуск (без Docker)

1. Создать и активировать виртуальное окружение:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Установить зависимости:

```bash
pip install -r requirements.txt
```

3. Настроить переменные окружения:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=TaskDSP_DB
```

4. Применить миграции:

```bash
alembic upgrade head
```

5. Запустить приложение:

```bash
uvicorn main:app --reload
```

Откройте `http://localhost:8000/` для страницы входа, затем переход на защищённую страницу `/join_table` выполняется после авторизации.

## Запуск в Docker

Файлы: [Dockerfile](/Dockerfile), [docker-compose.yml](/docker-compose.yml)

1. Собрать и запустить контейнеры:

```bash
docker-compose up
```

2. Приложение будет доступно на `http://localhost:8000/`.

**Примечания по настройке Docker Compose**
- Внутри контейнера приложения `DB_HOST` должен быть `postgres`, т.к. это имя сервиса БД в Compose.
- Переменные `POSTGRES_*` задают инициализацию БД в контейнере `postgres`, а `DB_*` — окружение приложения.
- Команда приложения включает запуск миграций Alembic: `alembic upgrade head && uvicorn main:app ...`

## Эндпоинты

- Пользователи
  - `POST /users/login` — логин, выдаёт `access_token` ([users.py](/app/api/endpoints/users.py#L16-L27))
  - `POST /users/` — регистрация пользователя ([users.py](/app/api/endpoints/users.py#L29-L38))

- Задачи ([tasks.py](/app/api/endpoints/tasks.py))
  - `GET /tasks/` — получить список задач
  - `POST /tasks/` — создать задачу
  - `PUT /tasks/` — изменить заголовок/описание
  - `DELETE /tasks/?task_id=<id>` — удалить задачу
  - `PATCH /tasks/?task_id=<id>&checked=<bool>` — отметить выполненной/снять отметку

- Интерфейс
  - `GET /` — страница входа ([home.html](/app/templates/home.html))
  - `GET /join_table` — защищённая страница задач (требует `Authorization: Bearer <token>`) ([main.py](/main.py))

- WebSocket
  - `ws://localhost:8000/ws/table/?username=<name>` ([websocket.py](/app/api/endpoints/websocket.py#L28-L41))

## Тесты

Запуск тестов:

```bash
pytest -v
```

В каталоге [tests](/tests) есть проверка эндпоинтов задач, авторизации и websockets.
