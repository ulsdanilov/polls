# polls

Сервис опросов пользователей

# Подготовительные действия

Установка и активация виртуального окружения

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Установка зависимостей

```bash
pip install -r requirements.txt
```

Установка переменных окружения (см. шаблон .env.example)

```bash
cd /polls/project
nano .env
```

Применение миграции к БД и создание администратора сервиса

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Запуск

```bash
python manage.py runserver
```

## Swagger

[http://127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger)
