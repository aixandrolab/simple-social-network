# Simple Social Network

---

## Postgres installation

```shell
# Arch Linux
sudo pacman -S postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Initialize database cluster (Arch Linux)
sudo su - postgres -c "initdb --locale en_US.UTF-8 -D '/var/lib/postgres/data'"
sudo systemctl start postgresql
sudo systemctl enable postgresql
```


## Database creation

```shell
sudo -u postgres psql

-- Create database
CREATE DATABASE simple_social_network_db
    OWNER postgres
    ENCODING 'UTF-8'
    LC_COLLATE 'en_US.UTF-8'
    LC_CTYPE 'en_US.UTF-8'
    TEMPLATE template0;
```

---

## .env

```text
# Core Settings
DJANGO_ENV=development
SECRET_KEY=secret-key
DEBUG=True

# Database Settings
DB_NAME=simple_social_network_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Email settings
EMAIL_ON=True
EMAIL_HOST=smtp.server.com
EMAIL_HOST_USER=email@example.com
EMAIL_HOST_PASSWORD=password
```

```commandline
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```