This file contains everything you need to know in order to run this app.


## Setup

### Prerequisites
- Python 3.13 or later
- Git
- A terminal


## Environment variables

The application reads its environment variables from a `.env` file located inside the `anatomy_resource/` directory.

To get started:

1. Use the provided `anatomy_resource/.env.example` file as a template.
2. Copy it to `anatomy_resource/.env`.
3. Replace the placeholder values with your own values.

The application uses these environment variables:

| Variable                  | Purpose                                                                       |
|---------------------------|-------------------------------------------------------------------------------|
| SECRET_KEY                | Used by Flask for application-level security and signing.                    |
| JWT_SECRET                | Used to sign and verify JSON Web Tokens for authentication.                  |
| CONTENT_EDITOR_INVITE_CODE| Required invitation code for registering Content Editor accounts.            |
| DATABASE_URL              | Specifies the database connection. Defaults to SQLite for local development; production uses PostgreSQL. |

Never commit your real `.env` file or share its secret values. The `.env.example` file contains placeholders and is safe to include in the repository.

###  Clone the repository

```bash
git clone https://github.com/jdavisprsvr-tech/anatomy_resource.git
cd anatomy_resource
```

###  Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

###  Install dependencies

```bash
pip install -r requirements.txt
```

## Migrations

This project uses **Flask-Migrate** and **Alembic** to manage database schema changes. Migrations keep the database structure synchronized with the application's SQLAlchemy models.

### Apply existing migrations

After configuring your environment variables and setting up the database, run:

```bash
flask --app 'anatomy_resource:create_app("development")' db upgrade
```

This applies any pending migrations to your local database.

### Create a new migration

When you make changes to your SQLAlchemy models, generate a migration with:

```bash
flask --app 'anatomy_resource:create_app("development")' db migrate -m "Describe your changes"
```

Review the generated migration file before applying it.

Then run:

```bash
flask --app 'anatomy_resource:create_app("development")' db upgrade
```

### Existing migrations

The `migrations/` directory contains the Alembic configuration, migration environment, and version history. The existing migrations create the `users` and `anatomy_entries` database tables.

###  Initialize the database

```bash
flask --app 'anatomy_resource:create_app("development")' db upgrade
```

###  Run the application

```bash
flask --app 'anatomy_resource:create_app("development")' run --host 127.0.0.1 --port 5001
```

The API will be available at:

`http://127.0.0.1:5001`

To verify that the application is running, visit:

`http://127.0.0.1:5001/ping`

The health endpoint should return `pong`.