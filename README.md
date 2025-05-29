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
   git clone <repository-url>
   cd weather-app

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

   
