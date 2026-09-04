# Warraq — Library Management System

A full-stack web application built with Django, HTML5, CSS3, and vanilla JavaScript that allows library members to browse the catalog, search titles, and manage book loans, while enabling librarians to oversee inventory and circulation via Django Admin.

## Tech Stack

- **Backend:** Python 3.12+, Django 6.1 (Model-View-Template architecture)
- **Database:** SQLite 3
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+), Bootstrap 5.3

## Application Architecture

The system is organized into three decoupled Django applications:

- **`accounts`**: Manages user authentication and session lifecycles. It provides member registration with both client-side JavaScript validation and Django server-side validation, secure password hashing, and login/logout views.
- **`catalog`**: Governs book inventory and metadata (title, author, ISBN, category, total copies, and available copies). It serves the catalog interface featuring instant, client-side title and author filtering without server round-trips.
- **`loans`**: Controls borrowing and returning workflows. It tracks loan records, enforces business rules (preventing checkouts when available copies reach zero), and immediately recalculates inventory counts upon book return.

## Project Structure

```text
ITI-Final/
├── accounts/                  # User authentication and registration
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── catalog/                   # Book inventory and catalog browsing
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── loans/                     # Borrowing and returning workflows
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── config/                    # Project settings and root URL configuration
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/                    # Global static assets
│   ├── css/
│   │   └── styles.css         # Theme styles and typography
│   ├── js/
│   │   ├── catalog-search.js  # Client-side catalog live search & filter
│   │   ├── main.js            # Dark mode toggling & global UI scripts
│   │   └── signup-validation.js # Client-side registration form validation
│   └── images/
│       └── warraq1.png
├── templates/                 # HTML templates
│   ├── accounts/
│   │   ├── login.html
│   │   └── signup.html
│   ├── catalog/
│   │   └── book_list.html
│   ├── loans/
│   │   └── my_loans.html
│   ├── base.html              # Base layout (navigation, messages, footer)
│   └── home.html              # Home landing page
├── manage.py                  # Django CLI entrypoint
├── requirements.txt           # Project dependencies
├── seed_sample_books.py       # Sample book catalog seeder
└── README.md                  # Project documentation
```

## Setup Instructions

Follow these steps to set up and run the application locally from a clean clone in under 10 minutes.

### 1. Clone the Repository and Navigate to Root

```bash
git clone https://github.com/Amr-Mohammed-Eid/ITI-Final.git
cd ITI-Final
```

### 2. Create and Activate a Virtual Environment

- **Windows (PowerShell / Command Prompt):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  ```

- **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Seed Initial Catalog Data

Populate the database with sample academic titles and copy counts:

```bash
python seed_sample_books.py
```

### 6. Create Librarian / Admin Account

Create a superuser to access the administrative interface:

```bash
python manage.py createsuperuser
```

Follow the prompts to configure the librarian username, email, and password.

### 7. Start the Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to:
- Member Portal: `http://127.0.0.1:8000/`
- Librarian Admin: `http://127.0.0.1:8000/admin/`

## Running Tests

Execute the automated test suite covering authentication, catalog views, and end-to-end loan workflows:

```bash
python manage.py test
```
