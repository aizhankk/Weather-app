
- Python 3.11
- Django 5.2
- PostgreSQL (с full-text search)
- Docker и Docker Compose для контейнеризации
- JavaScript (автодополнение и визуализация статистики)
- Bootstrap + django-widget-tweaks (для удобства фронтенда)

---

## Как запустить проект

### Локально через виртуальное окружение

1. Склонируйте репозиторий:

   ```bash
   git clone <адрес_репозитория>
   cd weather-app
Создайте и активируйте виртуальное окружение:

bash
Копировать
Редактировать
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
Установите зависимости:

bash
Копировать
Редактировать
pip install -r requirements.txt
Создайте файл .env в корне с переменными окружения:

ini
Копировать
Редактировать
SECRET_KEY=your-secret-key
DB_NAME=weather_db
DB_USER=weather_user
DB_PASSWORD=weather_pass
DB_HOST=localhost
DB_PORT=5432
Запустите локальную базу данных PostgreSQL (или используйте уже существующую).

Выполните миграции и создайте суперпользователя:

bash
Копировать
Редактировать
python manage.py migrate
python manage.py createsuperuser
Запустите сервер:

bash
Копировать
Редактировать
python manage.py runserver
Откройте в браузере http://localhost:8000

Запуск через Docker (рекомендуется)
Убедитесь, что установлены Docker и Docker Compose.

Создайте файл .env с переменными окружения (как указано выше).

В корне проекта должен быть файл docker-compose.yml со следующим содержимым:

yaml
Копировать
Редактировать
version: '3.9'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db

volumes:
  pgdata:
В корне проекта должен быть файл Dockerfile:

dockerfile
Копировать
Редактировать
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
Запустите контейнеры:

bash
Копировать
Редактировать
docker-compose up --build
В отдельном терминале выполните миграции:

bash
Копировать
Редактировать
docker-compose exec web python manage.py migrate
(Опционально) Создайте суперпользователя:

bash
Копировать
Редактировать
docker-compose exec web python manage.py createsuperuser
Откройте браузер по адресу http://localhost:8000

Скриншоты
<!-- Добавьте сюда скриншоты: ![Главная страница](path/to/screenshot1.png) ![Автодополнение](path/to/screenshot2.png) ![Страница погоды](path/to/screenshot3.png) ![История поиска и статистика](path/to/screenshot4.png) -->
Контакты
По вопросам пишите на email: your.email@example.com
