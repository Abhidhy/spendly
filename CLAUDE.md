# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup & Running

```bash
# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app (available at http://localhost:5001)
python app.py
```

## Testing

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_foo.py

# Run a single test
pytest tests/test_foo.py::test_function_name
```

## Architecture

**Stack:** Python/Flask backend, Jinja2 HTML templates, SQLite database, plain CSS/JS frontend.

**App entry point:** `app.py` — defines all Flask routes and starts the server on port 5001.

**Template hierarchy:** All pages extend `templates/base.html`, which provides the navbar, footer, CSS/JS includes, and a `{% block content %}` slot. Named routes via `url_for()` are used throughout templates.

**Database layer:** `database/db.py` — intended to contain `get_db()` (SQLite connection with row_factory + foreign keys), `init_db()` (CREATE TABLE IF NOT EXISTS), and `seed_db()` (sample data). Currently a stub awaiting implementation.

**Static assets:** `static/css/style.css` (all styling, uses DM Serif Display + DM Sans from Google Fonts) and `static/js/main.js` (placeholder).

## Current Implementation Status

The project is a step-by-step learning project. Currently implemented: Flask routing, static pages (landing, login, register, terms, privacy), and UI styling. Not yet implemented: database, authentication/sessions, user profiles, and expense CRUD operations. Stub routes exist in `app.py` for logout, profile, and expense add/edit/delete.
