# IN16 Study Manager

A full-featured Django web application for IN16 students to manage study resources.

## Features
- 🔐 Login / Register with student profile
- 📚 Units listing with note & group counts
- 📝 Notes per unit with full-detail view
- 👥 Study groups with member listings
- 🎓 Full class list with search & gender filter
- 📣 Announcements board
- ⏰ Personal class reminders
- 🌙 Dark mode toggle (localStorage)
- 📱 Fully responsive (Bootstrap 5)
- ⚙️ Admin panel for all data management

---

## Setup Instructions

### 1. Install Python & Django

```bash
pip install django
```

### 2. Navigate into the project

```bash
cd IN16_Study_Manager
```

### 3. Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
````

This creates:
- 6 units
- 8 sample students (password: `pass1234`)
- 6 notes across units
- 3 study groups
- 3 announcements
- Superuser: `admin` / `admin123`

### 5. Run the development server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## Admin Panel

Go to **http://127.0.0.1:8000/admin/**

Login: `admin` / `admin123`

From the admin you can:
- Add/edit Units, Notes, Students, Groups
- Post Announcements
- Manage Reminders

---

## Project Structure

```
IN16_Study_Manager/
├── manage.py
├── seed_data.py          ← Run once to populate sample data
├── IN16_Study_Manager/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── notes_app/
    ├── models.py         ← Unit, Student, Note, Group, Announcement, Reminder
    ├── views.py          ← All page views
    ├── urls.py           ← URL routing
    ├── forms.py          ← Register & Reminder forms
    ├── admin.py          ← Admin panel config
    └── templates/
        └── notes_app/
            ├── base.html          ← Sidebar, topbar, dark mode
            ├── login.html
            ├── register.html
            ├── home.html          ← Dashboard
            ├── units.html
            ├── notes.html
            ├── note_detail.html
            ├── groups.html
            ├── students.html
            ├── announcements.html
            └── reminders.html
```

## Tech Stack
- **Backend**: Django 4+
- **Frontend**: Bootstrap 5.3 + Bootstrap Icons
- **Fonts**: Sora + JetBrains Mono (Google Fonts)
- **Database**: SQLite (default)/postgresSQL
- **Auth**: Django built-in authentication
