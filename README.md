# Weather App

A simple Django web application for viewing weather by selected city with search history and autocomplete.

---

## Features

- User registration and authentication  
- City autocomplete using local database and external API  
- Display current and hourly weather  
- Save search history (for both registered users and guest sessions)  
- Popular search statistics and history visualization  
- PostgreSQL with full-text search support  
- Localization and timezone handling
- The entire application is containerized using Docker and Docker Compose for easy setup and deployment.
- Autocomplete suggestions are implemented, providing real-time city name hints as the user types.
- Basic automated tests are written to ensure key functionality works correctly and to facilitate future development and maintenance.

---

## Technologies Used

- Python 3.11  
- Django 5.2  
- PostgreSQL (with full-text search)  
- Docker and Docker Compose for containerization  
- JavaScript (autocomplete and stats visualization)  
- Bootstrap + django-widget-tweaks (for frontend convenience)  

---

## How to Run the Project

### Locally with virtual environment

1. Clone the repository:

   ```bash
   git clone https://github.com/aizhankk/Weather-app.git
   cd weather-app

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a .env file in the project root with environment variables:
   ```bash
   SECRET_KEY=your-secret-key
   DB_NAME=weather_db
   DB_USER=weather_user
   DB_PASSWORD=weather_pass
   DB_HOST=localhost
   DB_PORT=5432
   ```
5. Run a local PostgreSQL database (or use an existing one).
6. Run migrations:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```
# Docker Setup for Local Development

## Prerequisites
- Docker installed ([installation guide](https://docs.docker.com/get-docker/))
- Docker Compose installed ([installation guide](https://docs.docker.com/compose/install/))

## Setup Instructions

1. Environment Configuration
Create a `.env` file in the project root with the following variables:
```bash
SECRET_KEY=your_django_secret_key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```


1. Environment Configuration
Create a `.env` file in the project root with the following variables:
```bash
SECRET_KEY=your_django_secret_key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

2. Build and start the containers:
```bash
docker-compose up --build
```

3. In a new terminal, apply migrations:
```bash
docker-compose exec web python manage.py migrate
```


4. (Optional) Create a superuser:
Create a `.env` file in the project root with the following variables:
```bash
docker-compose exec web python manage.py createsuperuser
```

5. Open your browser and navigate to http://localhost:8000 to see the app running.




## Screenshots

![Screenshot 1](1.png)  

---

![Screenshot 2](2.png)  

---


![Screenshot 3](3.png)  

---

![Screenshot 4](4.png)  

---

![Screenshot 5](5.png)  

---

![Screenshot 6](6.png)  

---

![Screenshot 7](7.png)  

---

![Screenshot 8](8.png)  

