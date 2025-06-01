# 🎬 Cinema Management

Cinema Management is a web application for managing movie theaters, developed using **Django** and styled with **Bootstrap 5**. It provides functionality for managing films, screenings, tickets, and more through a responsive user interface and a robust backend.

## ✨ Features

- 🔁 Fully rewritten backend in **Django** (replaces the old PHP implementation)
- 🎨 Frontend built with **Bootstrap 5**
- 🗃️ Uses **MySQL/MariaDB** by default but easily switchable to **SQLite**
- 📦 Includes a **SQL dump** file of the original MariaDB database
- 🔄 JavaScript logic reused from the legacy project
- 💅 Most of the original CSS replaced with Bootstrap, but some styles reused
- 🧪 RESTful APIs for data retrieval and management
- 🚀 Ready for both **development** and **production** (via **Gunicorn**)

---

## 🔌 Database Configuration

By default, the project uses **MariaDB**. The configuration can be found in the `settings.py` file under the `DATABASES` section.

### Example: MariaDB (default)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cinema',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## Switch to SQLite (optional)

To use SQLite instead of MySQL, simply update the `DATABASES` configuration in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 🚀 Running the Project

### Development Mode

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations (only if needed)
python manage.py migrate

# Start the development server
python manage.py runserver
```

### Production Mode

```bash
# Install dependencies
pip install -r requirements.txt

# Collect static files
python cinema/manage.py collectstatic

# Run database migrations
python cinema/manage.py migrate

# Start the Gunicorn server
gunicorn cinema.wsgi:application
```