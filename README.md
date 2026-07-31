# Simple Social Network

**Version**: 1.0.0

---

## Overview

Simple Social Network is a Django-based web application that provides real-time messaging, friendship management, user profiles, and two-factor authentication. The platform is designed for secure communication and social interaction with a modern, dark-themed interface.

---

## ⚠️ Disclaimer

**By using this software, you agree to the full disclaimer terms.**

**Summary:** Software provided "AS IS" without warranty. You assume all risks.

**Full legal disclaimer:** See [DISCLAIMER.md](DISCLAIMER.md)

---

## Features

- **User Authentication**: Registration, login, email verification, password reset
- **Two-Factor Authentication**: TOTP-based 2FA with backup codes
- **Real-time Chat**: WebSocket-powered messaging with edit/delete capabilities
- **Friend System**: Send, accept, reject, and cancel friend requests
- **User Profiles**: Customizable profiles with avatars, biography, and personal information
- **Chat Management**: Archive, mute, delete, and restore chats
- **Message Status**: Read receipts and message timestamps
- **User Search**: Find users by username or first name
- **Responsive Design**: Works on desktop and mobile devices

---

## Technology Stack

### Backend
- **Django 6.0.5**: Web framework
- **PostgreSQL**: Database
- **Redis**: Caching and session storage
- **Django Channels**: WebSocket support for real-time features

### Frontend
- **Django Templates**: Server-side rendering
- **Semantic UI**: Frontend framework
- **JavaScript**: Native WebSocket client

### Security
- **pyotp**: TOTP generation/verification
- **bcrypt**: Backup code hashing

---

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/aixandrolab/simple-social-network.git
cd simple-social-network
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure PostgreSQL

#### Install PostgreSQL

**Arch Linux:**
```bash
sudo pacman -S postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql postgresql-contrib
```

#### Initialize Database Cluster (Arch Linux)
```bash
sudo su - postgres -c "initdb --locale en_US.UTF-8 -D '/var/lib/postgres/data'"
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Create Database
```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE simple_social_network_db
    OWNER postgres
    ENCODING 'UTF-8'
    LC_COLLATE 'en_US.UTF-8'
    LC_CTYPE 'en_US.UTF-8'
    TEMPLATE template0;
```

### Step 5: Configure Redis

**Arch Linux:**
```bash
sudo pacman -S redis
sudo systemctl start redis
sudo systemctl enable redis
```

**Ubuntu/Debian:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

### Step 6: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Core Settings
DJANGO_ENV=development
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=simple_social_network_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Redis Settings
REDIS_URL=redis://localhost:6379/1

# Email Settings (SMTP)
EMAIL_ON=True
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 7: Apply Migrations

```bash
python manage.py migrate
```

### Step 8: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 9: Collect Static Files

```bash
python manage.py collectstatic
```

### Step 10: Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

---

## Database Management

### Backup Database

```bash
pg_dump -U postgres -d simple_social_network_db > backup.sql
```

### Restore Database

```bash
psql -U postgres -d simple_social_network_db < backup.sql
```

### Remove Database

```sql
REVOKE CONNECT ON DATABASE simple_social_network_db FROM PUBLIC;
DROP DATABASE simple_social_network_db;
```

---

## Project Structure

```
simple-social-network/
├── chats/
│   ├── signals.py            # Post-save signals
│   ├── forms/                # Chat settings form
│   ├── templatetags/         # Custom template tags
│   ├── models/               # Chat, ChatStatus, ChatMessage
│   └── views/                # Chat views
├── core/
│   ├── consumers.py          # WebSocket consumers
│   ├── context_processors.py # Site config context
│   ├── models.py             # SiteConfig singleton
│   ├── services.py           # Email services
│   ├── routing.py            # WebSocket routing
│   ├── signals.py            # SiteConfig signals
│   ├── utils/                # Pagination utilities
│   └── views/                # Home, auth, password views
├── friends/
│   ├── services.py           # Friendship business logic
│   ├── signals.py            # Status change logging
│   ├── models/               # Friendship, FriendshipHistory
│   └── views/                # Friend request views
├── profiles/
│   ├── middleware.py         # Last activity tracking
│   ├── signals.py            # User profile creation
│   ├── forms/                # Profile, 2FA, password forms
│   ├── utils/                # Image validation
│   ├── models/             # Profile, token models
│   └── views/                # Profile, 2FA, settings views
├── static/                   # Static files
├── templates/                # Base templates and components
├── media/                    # User-uploaded files
├── .env                      # Environment variables
├── manage.py
├── requirements.txt
└── README.md
```

---

## Key Models

### Profile
- User profile with avatar, biography, 2FA settings
- Tracks online status via Redis
- Supports TOTP and backup codes

### Friendship
- Manages friend relationships with status (pending/accepted/rejected)
- Maintains history of status changes

### Chat
- Two-user private chat
- Supports naming, archiving, muting, and deletion

### ChatMessage
- Messages with content, read status, edit/delete support
- Timestamp tracking

### ChatStatus
- Per-user chat preferences (archived, muted, deleted, visible)
- Unique constraint per chat and profile

---

## API Endpoints

### WebSocket
```
ws://localhost:8000/ws/chat/{chat_id}/
```

**Message Types:**
- `chat_message_event`: Send/receive new messages
- `edit_message_event`: Edit existing messages
- `delete_message_event`: Delete messages

### URL Patterns

| URL                           | Description              |
|-------------------------------|--------------------------|
| `/`                           | Home page                |
| `/login/`                     | User login               |
| `/register/`                  | User registration        |
| `/profile/detail/{slug}/`     | User profile             |
| `/profile/search/`            | Search users             |
| `/friends/@username/`         | Friends list             |
| `/friends/incoming/`          | Incoming friend requests |
| `/friends/outgoing/`          | Outgoing friend requests |
| `/chats/active/`              | Active chats list        |
| `/chats/archived/`            | Archived chats           |
| `/chats/deleted/`             | Deleted chats            |
| `/chats/create/{profile_id}/` | Create new chat          |
| `/chat/details/{chat_id}/`    | Chat detail/messages     |
| `/chat/settings/{chat_id}/`   | Chat settings            |
| `/two-factor/`                | 2FA management           |

---

## Environment Variables Reference

| Variable              | Description                          | Default                    |
|-----------------------|--------------------------------------|----------------------------|
| `DJANGO_ENV`          | Environment (development/production) | `development`              |
| `SECRET_KEY`          | Django secret key                    | Required                   |
| `DEBUG`               | Debug mode                           | `True`                     |
| `ALLOWED_HOSTS`       | Comma-separated hosts                | `localhost`                |
| `DB_NAME`             | Database name                        | `simple_social_network_db` |
| `DB_USER`             | Database user                        | `postgres`                 |
| `DB_PASSWORD`         | Database password                    | Required                   |
| `DB_HOST`             | Database host                        | `localhost`                |
| `DB_PORT`             | Database port                        | `5432`                     |
| `REDIS_URL`           | Redis connection URL                 | `redis://localhost:6379/1` |
| `EMAIL_ON`            | Enable email sending                 | `False`                    |
| `EMAIL_HOST`          | SMTP server                          | -                          |
| `EMAIL_HOST_USER`     | SMTP username                        | -                          |
| `EMAIL_HOST_PASSWORD` | SMTP password                        | -                          |

---

## Development

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Shell Access

```bash
python manage.py shell
```

### Static Files

```bash
python manage.py collectstatic
python manage.py compress
```

---

## Troubleshooting

### Database Connection Issues

Check PostgreSQL is running:
```bash
sudo systemctl status postgresql
```

Verify database exists:
```bash
sudo -u postgres psql -l
```

### Redis Connection Issues

Check Redis is running:
```bash
sudo systemctl status redis
```

Test Redis connection:
```bash
redis-cli ping
```

### WebSocket Connection Issues

Ensure Daphne is running:
```bash
ps aux | grep daphne
```

Check Nginx WebSocket configuration:
```bash
sudo nginx -t
```

### 2FA Issues

Clear session data:
```bash
python manage.py shell
from django.contrib.sessions.models import Session
Session.objects.all().delete()
```

---

## Security Considerations

- All passwords are hashed using Django's PBKDF2
- 2FA uses TOTP with 30-second windows
- Backup codes are hashed with bcrypt
- CSRF protection is enabled
- Session data is stored in Redis
- SQL injection prevention via ORM
- XSS protection via Django templates

---

## License

Copyright (c) 2026, Alexander Suvorov. All rights reserved.