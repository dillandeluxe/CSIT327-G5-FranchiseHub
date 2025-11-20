# 🚀 CSIT327-G5-FranchiseHub

## 📘 Project Overview
**FranchiseHub** is a web-based platform connecting potential franchisees with franchisors by showcasing franchise opportunities, investment requirements, and allowing application submission. Franchisors manage listings and review applications with accept/reject workflows.

---

## 🧰 Tech Stack
- Backend: Django 5.2.7 (Python 3.13)
- Database: Supabase (PostgreSQL)
- Frontend: HTML / CSS / Django Templates
- Deployment: Render (Gunicorn + WhiteNoise)
- Version Control: Git + GitHub

---

## 📂 Project Structure (Key Folders)
```
FranchiseHub/
├─ accounts/                # Django app (models, views, urls)
├─ backend/                 # settings, wsgi
├─ templates/               # Django templates
├─ static/                  # Source static assets (collected later)
├─ staticfiles/             # Created by collectstatic in production
├─ requirements.txt
├─ manage.py
└─ .env                     # Local-only (NOT committed)
```

---

## 🔐 Environment Variables

### Local Development (.env)
Create `.env` at project root (same level as manage.py):
```env
DJANGO_SECRET_KEY=replace-this-with-a-strong-key
DJANGO_DEBUG=True

# Option 1: Use single Supabase URL (preferred)
DATABASE_URL=postgresql://postgres:<PASSWORD>@<HOST>.supabase.co:5432/postgres

# Option 2 (legacy – if customizing settings.py)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=<PASSWORD>
DB_HOST=<HOST>.supabase.co
DB_PORT=5432
```

### Production (Render Dashboard)
Set these in Render > Environment:
```
DJANGO_SECRET_KEY=<strong-random>
DJANGO_DEBUG=False
DATABASE_URL=postgresql://postgres:<PASSWORD>@<HOST>.supabase.co:5432/postgres
RENDER_EXTERNAL_HOSTNAME=<auto-set by Render>
ALLOWED_HOSTS=<optional, custom-domain.com>
DJANGO_CSRF_TRUSTED_ORIGINS=https://<service>.onrender.com,https://<custom-domain.com>
```

If using one-click superuser creation (optional):
```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=you@example.com
DJANGO_SUPERUSER_PASSWORD=StrongPass123!
```

---

## 🛠 Local Setup

### 1️⃣ Clone
```bash
git clone https://github.com/dillandeluxe/CSIT327-G5-FranchiseHub.git
cd CSIT327-G5-FranchiseHub
```

### 2️⃣ Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure .env
Add variables (see above).

### 5️⃣ Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Create Superuser
```bash
python manage.py createsuperuser
```

### 7️⃣ Run Dev Server
```bash
python manage.py runserver
```
Visit:
```
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/
```

---

## 📦 Static Files Handling
- Source assets live in `static/`.
- Production assets served from `staticfiles/` after:
```bash
python manage.py collectstatic --noinput
```
WhiteNoise is enabled (no extra CDN/config required).

---

## ☁️ Render Deployment

### Build Command
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

### Start Command
```bash
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

### Checklist
| Item | Status |
|------|--------|
| WhiteNoise middleware | ✅ |
| STATIC_ROOT configured | ✅ |
| DATABASE_URL set | ✅ |
| DEBUG=False in prod | ✅ |
| collectstatic run | ✅ |
| migrations applied | ✅ |
| superuser created on Render | ✅ |

### Optional: Auto Superuser (only once)
Add env vars (see earlier) then in Build Command:
```bash
python manage.py createsuperuser --noinput || true
```

---

## 🔍 Common Issues
| Problem | Fix |
|---------|-----|
| Admin CSS missing | Ensure collectstatic + production storage (Manifest) |
| 500 on /admin/ | Check DATABASE_URL + migrations |
| Static 404 | WhiteNoise order + STATIC_ROOT path |
| CSRF errors | Add Render domain to DJANGO_CSRF_TRUSTED_ORIGINS |

---

## 🧪 Production-like Local Test
```bash
set DJANGO_DEBUG=False          # Windows (PowerShell)
# export DJANGO_DEBUG=False      # macOS/Linux
python manage.py collectstatic --noinput
python manage.py runserver
```

---

## 👥 Team Members
Lanz Roy Sumalpong - Product Owner - lanzroy.sumalpong@cit.edu  
Jethro Salindato - Business Analyst - jethro.salindato@cit.edu  
David Ryan Sia - Scrum Master - davidryan.sia@cit.edu  
Dillan Marquin Ycoy - Lead Developer - dillanmarquin.ycoy@cit.edu  
German Oliver Velasco - FullStack Developer - germanoliver.velasco@cit.edu  
John James Palis - FullStack Developer - johnjames.palis@cit.edu  

---

## ✅ Summary
You can develop locally with `.env`, deploy to Render using the provided build/start commands, and manage static assets via WhiteNoise and collectstatic. All configuration now matches the current codebase (Django 5.2.7, Python 3.13, Supabase, Render).

Happy building!
