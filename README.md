# 🛒 OLX Clone - Platforma de Anunțuri Online

Un clone modern al platformei OLX, dezvoltat în Django, cu funcționalități complete pentru vânzarea și cumpărarea de produse online.

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✅ Probleme Rezolvate Recent 

### 🆕 Noi Funcționalități (Latest Update)
- **✅ Editare email în profil** - Utilizatorii pot modifica adresa de email cu reconfirmarea automată
- **✅ Parolă uitată la login** - Link direct în pagina de conectare pentru resetarea parolei
- **✅ Schimbare parolă din profil** - Buton dedicat în pagina de profil pentru modificarea parolei
- **✅ Formulare personalizate** - Design consistent pentru toate operațiunile de autentificare
- **✅ Emailuri HTML** - Template-uri profesionale pentru resetarea parolei
- **✅ Validări îmbunătățite** - Verificări de securitate pentru toate formularele

### 🐛 Fix-uri Implementate
- **✅ Mesaje personalizate** - Rezolvat problema cu textarea-ul pentru mesaje custom
- **✅ Template editare anunț** - Creat template complet pentru editarea anunțurilor (`edit.html`)
- **✅ Funcționalitate salvare anunțuri** - Corectată logica pentru salvarea/eliminarea din favorite
- **✅ Afișare anunțuri utilizator** - Fixed `my_listings.html` să afișeze corect anunțurile
- **✅ Ștergere imagini** - Adăugată funcționalitatea pentru ștergerea imaginilor din edit
- **✅ URL-uri corecte** - Toate URL-urile și rutele funcționează corect
- **✅ Status anunțuri** - Implementat sistem complet de dezactivare/activare anunțuri

### 🔧 Îmbunătățiri Tehnice
- Context complet în view-uri (page_obj + compatibility variables)
- Funcții JavaScript optimizate pentru operații async
- Validare îmbunătățită în formulare
- Design responsive pentru toate template-urile
- Sistem de status-uri: Activ, Vândut, Dezactivat, Ciornă

### 🗄️ Configurare PostgreSQL
- **Ghid complet** - `POSTGRESQL_SETUP.md` cu instrucțiuni pas cu pas
- **Configurare flexibilă** - Suport pentru SQLite (dezvoltare) și PostgreSQL (producție)
- **Migrare ușoară** - Instrucțiuni pentru transferul datelor existente
- **Environment variables** - Configurare prin fișiere `.env`

### 📋 Funcționalități Status Anunțuri:
1. **Activ** - Anunțul este vizibil și poate fi contactat
2. **Vândut** - Anunțul este marcat ca vândut (nu mai apare în căutări)
3. **Dezactivat** - Anunțul este temporar oprit
4. **Ciornă** - Anunțul este salvat dar nu publicat

**Cum schimbi status-ul:**
- Mergi la "Anunțurile mele"
- Apasă dropdown-ul "Status" de lângă fiecare anunț
- Alege noul status dorit

### 🔐 Workflow Autentificare Completă

#### Resetare Parolă:
1. **Click "Ai uitat parola?"** din pagina de login
2. **Introduci emailul** asociat contului
3. **Primești email** cu link de resetare (valabil 24h)
4. **Setezi parola nouă** prin formularul securizat
5. **Confirmare** și redirecționare către login

#### Editare Email în Profil:
1. **Accesezi "Editează profilul"** din pagina personală
2. **Modifici adresa de email** în formular
3. **Salvezi modificările** - emailul se actualizează
4. **Primești email de reconfirmarea** la noua adresă
5. **Confirmi noua adresă** prin link-ul din email

#### Schimbare Parolă din Profil:
1. **Click "Schimbă parola"** din pagina de profil
2. **Introduci parola curentă** pentru verificare
3. **Setezi parola nouă** de două ori pentru confirmare
4. **Salvezi** - parola se actualizează imediat

## ✨ Funcționalități Principale

### 🔐 Sistem de Autentificare Complet
- **Înregistrare cu confirmare email** - Utilizatorii primesc email de confirmare
- **Login/Logout securizat** - Sesiuni protejate cu CSRF
- **Profil utilizator complet** - Avatar, informații personale, setări
- **✨ Editare email din profil** - Modificarea adresei cu reconfirmarea automată
- **✨ Resetare parolă prin email** - Workflow complet pentru recuperarea parolei
- **✨ Schimbare parolă din profil** - Opțiune directă în panoul utilizatorului
- **Validări avansate** - Verificări de securitate pentru toate operațiunile

#### 🛡️ Securitate Autentificare:
- **Password Hashing**: PBKDF2 cu SHA256 + salt unic per parolă
- **Token Security**: Token-uri unice cu expirare pentru resetare/confirmare
- **Session Protection**: Cookie-uri securizate cu HttpOnly și Secure flags
- **CSRF Protection**: Protecție completă împotriva atacurilor cross-site
- **Input Validation**: Sanitizare și validare pentru toate input-urile
- **Rate Limiting**: Protecție împotriva atacurilor brute-force (în producție)

### 📝 Gestionarea Anunțurilor
- **Creare anunțuri** - Interfață intuitivă cu upload imagini
- **Editare și gestionare** - Controlul complet asupra anunțurilor
- **Categorii organizate** - Structură ierarhică pentru organizare
- **Căutare avansată** - Filtrare după preț, locație, categorie
- **Anunțuri salvate** - Sistem de favorite

### 💬 Sistem de Mesagerie
- **Mesaje în timp real** - Comunicare directă între utilizatori
- **Mesaje rapide** - Template-uri predefinite pentru conveniență
- **Mesaje personalizate** - Editor rich pentru mesaje custom
- **Notificări email** - Alertă pentru mesaje noi
- **Conversații organizate** - Istoric complet de comunicare

### 🎨 Interfață Modernă
- **Design responsive** - Optimizat pentru toate dispozitivele
- **Bootstrap 5** - Interface elegantă și modernă
- **Animații CSS** - Experiență de utilizare fluidă
- **UX intuitiv** - Navigare simplă și eficientă

## 🛠 Tehnologii Utilizate

### Backend
- **Django 5.2.4** - Framework web Python
- **SQLite** - Baza de date (dezvoltare)
- **PostgreSQL** - Recomandat pentru producție
- **Django Sites Framework** - Gestionarea site-urilor
- **Django Email Backend** - Sistem de email complet

### Frontend
- **Bootstrap 5.3** - Framework CSS responsive
- **FontAwesome** - Iconuri moderne
- **JavaScript vanilla** - Interactivitate
- **CSS3 animations** - Animații fluide

### Dependențe Python
```
Django==5.2.4
django-crispy-forms
django-crispy-bootstrap4
django-widget-tweaks
Pillow  # Pentru procesarea imaginilor
```

## 🛡️ Securitate și Autentificare

### Password Hashing
Django folosește **PBKDF2 cu SHA256** pentru hash-uirea parolelor:
```python
# Exemplu hash în database
pbkdf2_sha256$390000$randomsalt$hashedpassword

# Configurare în settings.py
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',  # Default
    'django.contrib.auth.hashers.Argon2PasswordHasher',  # Alternative
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
```

### Validări Parole
```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

### Securitatea Sesiunilor
```python
SESSION_COOKIE_AGE = 1209600  # 2 săptămâni
SESSION_COOKIE_SECURE = True  # Pentru HTTPS
SESSION_COOKIE_HTTPONLY = True  # Previne XSS
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
```

### Token-uri Securizate
- **Email Confirmation**: Token-uri de 64 caractere cu expirare în 3 zile
- **Password Reset**: Token-uri Django built-in cu expirare în 24h
- **CSRF Protection**: Token-uri unice pentru fiecare sesiune

### Măsuri de Protecție
- ✅ **SQL Injection**: Django ORM previne automat
- ✅ **XSS**: Template escaping automat
- ✅ **CSRF**: Protecție pe toate formularele
- ✅ **Session Fixation**: Regenerare sesiune la login
- ✅ **Brute Force**: Rate limiting prin Nginx în producție

## 🚀 Instalare și Configurare

### Prerequisite
- Python 3.12+
- pip (Python package manager)
- Git

### 1. Clonează Proiectul
```bash
git clone https://github.com/yourusername/olx-clone.git
cd olx-clone
```

### 2. Creează Mediul Virtual
```bash
python -m venv myproject_venv
source myproject_venv/bin/activate  # Linux/Mac
# sau
myproject_venv\Scripts\activate  # Windows
```

### 3. Instalează Dependențele
```bash
pip install -r requirements.txt
```

### 4. Configurează Setările

#### Email Settings (în `olx_clone/settings.py`)
```python
# Pentru Gmail (dezvoltare)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'

# Pentru testing local
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

#### Database (opțional pentru PostgreSQL)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'olx_clone_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Aplică Migrațiile
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Creează Superuser
```bash
python manage.py createsuperuser
```

### 7. Colectează Fișierele Statice
```bash
python manage.py collectstatic
```

### 8. Pornește Serverul
```bash
python manage.py runserver
```

Acesează aplicația la: `http://127.0.0.1:8000`

## 📁 Structura Proiectului

```
olx_clone/
├── accounts/                 # App pentru utilizatori
│   ├── models.py            # UserProfile, EmailConfirmation
│   ├── views.py             # Autentificare, profil
│   ├── forms.py             # Formulare utilizator
│   ├── utils.py             # Servicii email
│   └── urls.py              # URL-uri accounts
├── listings/                # App pentru anunțuri
│   ├── models.py            # Listing, ListingImage, SavedListing
│   ├── views.py             # CRUD anunțuri
│   ├── forms.py             # Formulare anunțuri
│   └── urls.py              # URL-uri listings
├── categories/              # App pentru categorii
│   ├── models.py            # Category model
│   └── admin.py             # Admin categorii
├── messaging/               # App pentru mesagerie
│   ├── models.py            # Conversation, Message
│   ├── views.py             # Chat, notificări
│   ├── forms.py             # Formulare mesaje
│   └── urls.py              # URL-uri messaging
├── templates/               # Template-uri HTML
│   ├── base/                # Template-uri de bază
│   ├── accounts/            # Template-uri utilizatori
│   ├── listings/            # Template-uri anunțuri
│   └── messaging/           # Template-uri mesagerie
├── static/                  # Fișiere statice
├── media/                   # Upload-uri utilizatori
├── olx_clone/              # Setări proiect
│   ├── settings.py         # Configurații Django
│   ├── urls.py             # URL-uri principale
│   └── wsgi.py             # WSGI config
└── manage.py               # Django management
```

## 🌐 Deploy în Producție

### Option 1: Heroku Deploy

#### 1. Pregătire pentru Heroku
```bash
pip install gunicorn whitenoise dj-database-url psycopg2-binary
pip freeze > requirements.txt
```

#### 2. Creează `Procfile`
```
web: gunicorn olx_clone.wsgi:application
```

#### 3. Configurează `settings.py` pentru producție
```python
import dj_database_url
import os

# Database
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Adaugă WhiteNoise
    # ... rest of middleware
]

# Security
ALLOWED_HOSTS = ['your-app-name.herokuapp.com', 'localhost']
DEBUG = False  # Pentru producție
```

#### 4. Deploy pe Heroku
```bash
heroku login
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set EMAIL_HOST_USER='your-email@gmail.com'
heroku config:set EMAIL_HOST_PASSWORD='your-app-password'

git add .
git commit -m "Initial deploy"
git push heroku main

heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py collectstatic --noinput
```

### Option 2: VPS cu Domeniul Tău (Recomandat)

#### 1. Pregătirea pentru VPS
```bash
# Pe serverul local, pregătește fișierele
cp olx_clone/settings_production.py olx_clone/settings_production.py.backup
cp .env.production.example .env.production

# Editează .env.production cu datele tale:
nano .env.production
```

#### 2. Configurare Environment Variables
```bash
# .env.production (pe server)
DJANGO_ENV=production
DJANGO_DEBUG=False
SECRET_KEY=your-very-secret-key

# Database
DB_NAME=olx_clone_db
DB_USER=olx_user
DB_PASSWORD=your-strong-password

# Email pentru domeniul tău
EMAIL_HOST=mail.yourdomain.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
```

#### 3. Configurare Email în cPanel/Hosting
1. **Creează adresele de email în cPanel:**
   - `noreply@yourdomain.com`
   - `admin@yourdomain.com`
   - `server@yourdomain.com`

2. **Găsește setările SMTP în cPanel:**
   - Outgoing Server: `mail.yourdomain.com` sau `smtp.yourdomain.com`
   - Port: `587` (TLS) sau `465` (SSL)
   - Authentication: Activat

#### 1. Configurare Server
```bash
# Instalare dependențe
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib

# Creează utilizator pentru aplicație
sudo adduser olxuser
sudo usermod -aG sudo olxuser
```

#### 2. Configurare PostgreSQL
```bash
sudo -u postgres psql
CREATE DATABASE olx_clone_db;
CREATE USER olxuser WITH PASSWORD 'strongpassword';
GRANT ALL PRIVILEGES ON DATABASE olx_clone_db TO olxuser;
\q
```

#### 3. Deploy Aplicație
```bash
# Clonează proiectul
git clone https://github.com/yourusername/olx-clone.git
cd olx-clone

# Configurează mediul virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurează database
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

#### 4. Configurare Gunicorn
```bash
# Testează Gunicorn
gunicorn --bind 0.0.0.0:8000 olx_clone.wsgi:application

# Creează service file
sudo nano /etc/systemd/system/olxclone.service
```

Conținut `olxclone.service`:
```ini
[Unit]
Description=OLX Clone Django App
After=network.target

[Service]
User=olxuser
Group=www-data
WorkingDirectory=/home/olxuser/olx-clone
Environment="PATH=/home/olxuser/olx-clone/venv/bin"
ExecStart=/home/olxuser/olx-clone/venv/bin/gunicorn --workers 3 --bind unix:/home/olxuser/olx-clone/olx_clone.sock olx_clone.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 5. Configurare Nginx
```bash
sudo nano /etc/nginx/sites-available/olxclone
```

Conținut Nginx config:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/olxuser/olx-clone;
    }
    
    location /media/ {
        root /home/olxuser/olx-clone;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/olxuser/olx-clone/olx_clone.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/olxclone /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable olxclone
sudo systemctl start olxclone
```

## 🔧 Configurare Email în Producție

### Gmail (Recomandat pentru testing)
1. Activează **2-Factor Authentication**
2. Generează **App Password** în Google Account Settings
3. Folosește App Password în `EMAIL_HOST_PASSWORD`

### SendGrid (Recomandat pentru producție)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

## 📊 Administrare

### Panoul de Admin
Accesează: `http://your-domain.com/admin/`

**Funcționalități admin:**
- Gestionarea utilizatorilor și profilurilor
- Moderarea anunțurilor
- Gestionarea categoriilor
- Monitorizarea conversațiilor
- Statistici și rapoarte

### Comenzi Management Utile
```bash
# Backup database
python manage.py dumpdata > backup.json

# Restore database
python manage.py loaddata backup.json

# Clear sessions
python manage.py clearsessions

# Update search indexes (dacă folosești search)
python manage.py update_index
```

## 🌐 Configurare Domeniu Personal

### 📧 Setări Email pentru Domeniul Tău

#### 1. Creează Adresele de Email în cPanel
```
noreply@yourdomain.com   - Pentru emailuri automate
admin@yourdomain.com     - Pentru notificări admin
server@yourdomain.com    - Pentru erori de server
```

#### 2. Configurare Django pentru Domeniul Tău
```python
# În settings_production.py
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Email configuration
EMAIL_HOST = 'mail.yourdomain.com'
EMAIL_HOST_USER = 'noreply@yourdomain.com'
DEFAULT_FROM_EMAIL = 'OLX Clone <noreply@yourdomain.com>'
```

#### 3. Testează Configurația Email
```bash
# Pe server, testează trimiterea de email
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Mesaj test', 'noreply@yourdomain.com', ['your-email@gmail.com'])
```

### 🚀 Deploy pe VPS cu Domeniul Tău

#### 1. Upload Proiect pe Server
```bash
# Conectează-te la VPS
ssh root@your-server-ip

# Navighează în directorul web
cd /var/www/
mkdir yourdomain.com
cd yourdomain.com

# Clonează proiectul
git clone your-git-repo.git .
```

#### 2. Configurare Environment
```bash
# Copiază fișierul de environment
cp .env.production.example .env
nano .env

# Editează cu datele tale:
DJANGO_ENV=production
SECRET_KEY=your-secret-key
EMAIL_HOST=mail.yourdomain.com
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-password
```

#### 3. Configurare Nginx pentru Domeniul Tău
```nginx
# /etc/nginx/sites-available/yourdomain.com
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location /static/ {
        alias /var/www/yourdomain.com/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/yourdomain.com/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/yourdomain.com/olx_clone.sock;
    }
}
```

#### 4. SSL Certificate cu Let's Encrypt
```bash
# Instalează Certbot
sudo apt install certbot python3-certbot-nginx

# Obține certificat SSL pentru domeniul tău
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Verifică renewarea automată
sudo certbot renew --dry-run
```

## 🐛 Troubleshooting

### Probleme Comune

#### 1. Email nu se trimite
```bash
# Verifică setările email în settings.py
# Pentru debugging, folosește console backend:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

#### 2. Imagini nu se afișează
```bash
# Verifică MEDIA_URL și MEDIA_ROOT în settings.py
# Asigură-te că nginx servește fișierele media
```

#### 3. Erori CSS/JS
```bash
# Rulează collectstatic
python manage.py collectstatic --clear

# Verifică setările STATIC_URL și STATIC_ROOT
```

#### 4. Erori database
```bash
# Reset migrations (ATENȚIE: șterge datele!)
python manage.py migrate --fake-initial
python manage.py migrate --run-syncdb
```

## 🤝 Contribuție

1. Fork proiectul
2. Creează un branch pentru feature (`git checkout -b feature/AmazingFeature`)
3. Commit modificările (`git commit -m 'Add some AmazingFeature'`)
4. Push în branch (`git push origin feature/AmazingFeature`)
5. Deschide un Pull Request

## 📝 License

Acest proiect este licențiat sub MIT License - vezi fișierul [LICENSE](LICENSE) pentru detalii.

## 👨‍💻 Autor

**[Numele Tău]**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Mulțumiri

- Django Community pentru framework-ul excelent
- Bootstrap team pentru design system
- FontAwesome pentru iconuri
- Contribuitori și testeri

---

⭐ **Dacă proiectul ți-a fost util, lasă o stea pe GitHub!** ⭐
