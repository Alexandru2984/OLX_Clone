# Configurare PostgreSQL pentru OLX Clone

## 1. Instalarea PostgreSQL pe Ubuntu/Debian:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

## 2. Configurarea utilizatorului și bazei de date:

```bash
# Comută la utilizatorul postgres
sudo -u postgres psql

# În consola PostgreSQL:
CREATE DATABASE olx_clone_db;
CREATE USER olx_user WITH PASSWORD 'parola_sigura_aici';
ALTER ROLE olx_user SET client_encoding TO 'utf8';
ALTER ROLE olx_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE olx_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE olx_clone_db TO olx_user;
\q
```

## 3. Configurarea Django:

Creează fișierul `.env` (copiază din `.env.example`):
```bash
cp .env.example .env
```

Editează `.env` cu valorile pentru PostgreSQL:
```env
# Django
SECRET_KEY=your-very-secret-key-here-generate-new-one
DEBUG=True

# Database PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=olx_clone_db
DB_USER=olx_user
DB_PASSWORD=parola_sigura_aici
DB_HOST=localhost
DB_PORT=5432

# Email settings
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here

# Site settings
SITE_ID=1
SITE_DOMAIN=localhost:8000
SITE_NAME=OLX Clone
```

## 4. Actualizează settings.py:

Adaugă la începutul fișierului `olx_clone/settings.py`:
```python
import os
from decouple import config

# Database
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}
```

## 5. Instalează python-decouple:

```bash
pip install python-decouple
```

## 6. Migrarea datelor de la SQLite la PostgreSQL:

### Opțiunea 1: Migrare cu datele existente
```bash
# Backup data din SQLite
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > backup.json

# Șterge migrațiile (păstrează __init__.py)
rm accounts/migrations/0*.py
rm listings/migrations/0*.py
rm categories/migrations/0*.py
rm messaging/migrations/0*.py

# Recrează migrațiile
python manage.py makemigrations accounts
python manage.py makemigrations listings  
python manage.py makemigrations categories
python manage.py makemigrations messaging

# Aplică migrațiile pe PostgreSQL
python manage.py migrate

# Restore data
python manage.py loaddata backup.json
```

### Opțiunea 2: Start fresh (fără date existente)
```bash
# Șterge migrațiile
rm accounts/migrations/0*.py
rm listings/migrations/0*.py
rm categories/migrations/0*.py
rm messaging/migrations/0*.py

# Recrează migrațiile
python manage.py makemigrations
python manage.py migrate

# Creează superuser nou
python manage.py createsuperuser
```

## 7. Testarea conexiunii:

```bash
python manage.py shell
```

În shell:
```python
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT version();")
row = cursor.fetchone()
print(row)
```

## 8. Servicii PostgreSQL:

```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Stop PostgreSQL  
sudo systemctl stop postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql

# Enable pe boot
sudo systemctl enable postgresql

# Status
sudo systemctl status postgresql
```

## 9. Comenzi utile PostgreSQL:

```bash
# Conectare la baza de date
psql -h localhost -d olx_clone_db -U olx_user

# Backup database
pg_dump -h localhost -U olx_user olx_clone_db > backup.sql

# Restore database
psql -h localhost -U olx_user olx_clone_db < backup.sql

# Verifică conexiunile active
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"
```

## 10. Configurare pentru producție:

Pentru producție (Heroku, DigitalOcean, etc.), folosește variabilele de mediu:
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

## Troubleshooting:

### Eroare: "FATAL: authentication failed"
```bash
sudo -u postgres psql
ALTER USER olx_user PASSWORD 'parola_noua';
```

### Eroare: "database does not exist"  
```bash
sudo -u postgres createdb olx_clone_db
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE olx_clone_db TO olx_user;"
```

### Eroare: "permission denied"
```bash
sudo -u postgres psql
GRANT ALL PRIVILEGES ON DATABASE olx_clone_db TO olx_user;
ALTER USER olx_user CREATEDB;
```
