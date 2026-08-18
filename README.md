# Django Student Login System

A beginner-friendly **Student Registration and Login System** built using **Python, Django, HTML, CSS, MySQL, and PyMySQL**.

This project demonstrates how to create a Django web application connected to a MySQL database, register students, validate duplicate usernames, authenticate users, and display successful or invalid login messages.

---

## Project Overview

The application provides a simple student registration and login system.

### Users can:

* Register with username, password, contact, email, and address
* Store student details in MySQL
* Check whether a username already exists
* Login using registered credentials
* Validate username and password
* Display an invalid login message
* Display a successful login page
* Verify registered users directly through MySQL

---

## Features

* Student Registration
* Student Login
* Username Duplicate Checking
* Username and Password Validation
* MySQL Database Integration
* PyMySQL Connection
* Django URL Routing
* HTML Forms
* CSS Styling
* CSRF Protection
* Successful Login Page
* Invalid Login Message
* MySQL Database Verification
* Responsive Login Page

---

## Technologies Used

| Technology | Purpose              |
| ---------- | -------------------- |
| Python     | Programming language |
| Django     | Web framework        |
| MySQL      | Database             |
| PyMySQL    | MySQL connection     |
| HTML5      | Web pages            |
| CSS3       | Page styling         |

---

# Project Structure

```text
django-student-login-system/
│
├── manage.py
│
├── project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── app/
│   ├── __init__.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   └── models.py
│
├── templates/
│   ├── index.html
│   ├── signup.html
│   ├── login.html
│   └── home.html
│
├── static/
│       └── login.css
│
└── README.md

```

---

# Step 1: Create Django Project

Create the Django project:

```bash
django-admin startproject project
```

Create the application:

```bash
python manage.py startapp app
```

---

# Step 2: Install Required Packages

Install Django:

```bash
pip install django
```

Install PyMySQL:

```bash
pip install pymysql
```

---

# Step 3: Add App in settings.py

Open:

```text
project/settings.py
```

Add `app` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app',
]
```

Configure templates:

```python
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
        ...
    },
]
```

Configure static files:

```python
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

---

# Step 4: Create MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE student;
```

Select the database:

```sql
USE student;
```

---

# Step 5: Create Users Table

Create the `users` table:

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    contact VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL
);
```

---

# Step 6: MySQL Connection

The project uses PyMySQL to connect Django with MySQL.

Example:

```python
import pymysql


def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='*****',
        database='student'
    )
```

> The actual database password should never be uploaded to a public GitHub repository.

For a production project, use environment variables instead of hard-coded credentials.

---

# Step 7: views.py

The application contains:

* `index()`
* `signup()`
* `login()`

Example:

```python
from django.shortcuts import render
import pymysql


def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='*****',
        database='student'
    )


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == "POST":

        username = request.POST.get("t1")
        password = request.POST.get("t2")
        contact = request.POST.get("t3")
        email = request.POST.get("t4")
        address = request.POST.get("t5")

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s",
            (username,)
        )

        user = cur.fetchone()

        if user:
            cur.close()
            con.close()

            return render(
                request,
                "signup.html",
                {"msg": "Username already exists"}
            )

        cur.execute(
            """
            INSERT INTO users
            (username, password, contact, email, address)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (username, password, contact, email, address)
        )

        con.commit()

        cur.close()
        con.close()

        return render(
            request,
            "signup.html",
            {"msg": "Registration Successful"}
        )

    return render(request, "signup.html")


def login(request):
    if request.method == "POST":

        username = request.POST.get("t1")
        password = request.POST.get("t2")

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cur.fetchone()

        cur.close()
        con.close()

        if user:
            return render(
                request,
                "home.html",
                {"username": username}
            )

        return render(
            request,
            "login.html",
            {"msg": "Invalid username or password"}
        )

    return render(request, "login.html")
```

---

# Step 8: Signup HTML

Create:

```text
templates/signup.html
```

The form uses:

| Field    | Name |
| -------- | ---- |
| Username | `t1` |
| Password | `t2` |
| Contact  | `t3` |
| Email    | `t4` |
| Address  | `t5` |

Example:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
</head>

<body>

    <h2>Student Registration</h2>

    <form method="POST">
        {% csrf_token %}

        <input type="text" name="t1"
               placeholder="Username" required>

        <br><br>

        <input type="password" name="t2"
               placeholder="Password" required>

        <br><br>

        <input type="text" name="t3"
               placeholder="Contact" required>

        <br><br>

        <input type="email" name="t4"
               placeholder="Email" required>

        <br><br>

        <input type="text" name="t5"
               placeholder="Address" required>

        <br><br>

        <input type="submit" value="Signup">
    </form>

    {% if msg %}
        <p>{{ msg }}</p>
    {% endif %}

</body>
</html>
```

---

# Step 9: Login HTML

Create:

```text
templates/login.html
```

Use:

```html
{% load static %}

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Student Login</title>

    <link rel="stylesheet"
          href="{% static 'css/login.css' %}">
</head>

<body>

    <div class="login-container">

        <div class="login-box">

            <h1>Student Login</h1>

            <p class="subtitle">
                Welcome back! Please login to continue.
            </p>

            <form method="POST">

                {% csrf_token %}

                <div class="input-group">
                    <label>Username</label>

                    <input type="text"
                           name="t1"
                           placeholder="Enter your username"
                           required>
                </div>

                <div class="input-group">
                    <label>Password</label>

                    <input type="password"
                           name="t2"
                           placeholder="Enter your password"
                           required>
                </div>

                <button type="submit">
                    Login
                </button>

            </form>

            {% if msg %}
                <p class="message">{{ msg }}</p>
            {% endif %}

            <div class="signup-link">
                Don't have an account?
                <a href="/signup/">
                    Continue to Signup
                </a>
            </div>

        </div>

    </div>

</body>
</html>
```

---

# Step 10: Login CSS

Create:

```text
static/css/login.css
```

Add:

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, Helvetica, sans-serif;
    min-height: 100vh;

    background: linear-gradient(135deg, #667eea, #764ba2);

    display: flex;
    justify-content: center;
    align-items: center;
}

.login-container {
    width: 100%;
    padding: 20px;
}

.login-box {
    width: 400px;
    max-width: 100%;
    margin: auto;

    background: white;
    padding: 40px;

    border-radius: 15px;

    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
}

.login-box h1 {
    text-align: center;
    color: #333;
    margin-bottom: 10px;
    font-size: 30px;
}

.subtitle {
    text-align: center;
    color: #777;
    font-size: 14px;
    margin-bottom: 30px;
}

.input-group {
    margin-bottom: 20px;
}

.input-group label {
    display: block;
    margin-bottom: 8px;

    font-size: 14px;
    font-weight: bold;
    color: #444;
}

.input-group input {
    width: 100%;
    padding: 13px 15px;

    border: 1px solid #ddd;
    border-radius: 8px;

    font-size: 15px;
    outline: none;

    transition: 0.3s;
}

.input-group input:focus {
    border-color: #667eea;

    box-shadow:
        0 0 0 3px rgba(102, 126, 234, 0.15);
}

button {
    width: 100%;
    padding: 13px;

    border: none;
    border-radius: 8px;

    background: linear-gradient(135deg, #667eea, #764ba2);

    color: white;
    font-size: 16px;
    font-weight: bold;

    cursor: pointer;

    transition: 0.3s;
}

button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 8px 20px rgba(102, 126, 234, 0.3);
}

.message {
    margin-top: 20px;

    text-align: center;

    color: #d93025;
    font-size: 14px;
    font-weight: bold;
}

.signup-link {
    text-align: center;

    margin-top: 25px;

    color: #777;
    font-size: 14px;
}

.signup-link a {
    color: #667eea;

    text-decoration: none;

    font-weight: bold;
}

.signup-link a:hover {
    text-decoration: underline;
}

@media (max-width: 480px) {

    .login-box {
        padding: 30px 20px;
    }

    .login-box h1 {
        font-size: 26px;
    }
}
```

---

# Step 11: Home HTML

Create:

```text
templates/home.html
```

```html
<!DOCTYPE html>
<html>

<head>
    <title>Home</title>
</head>

<body>

    <h1>Welcome {{ username }}</h1>

    <p>Login successful.</p>

</body>

</html>
```

---

# Step 12: Index HTML

Create:

```text
templates/index.html
```

```html
<!DOCTYPE html>
<html>

<head>
    <title>Student System</title>
</head>

<body>

    <h1>
        Student Registration and Login System
    </h1>

    <a href="/signup/">Signup</a>

    <br><br>

    <a href="/login/">Login</a>

</body>

</html>
```

---

# Step 13: App urls.py

Create or update:

```text
app/urls.py
```

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]
```

---

# Step 14: Project urls.py

Open:

```text
project/urls.py
```

Use:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
```

---

# Step 15: Run the Django Server

Run:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# Application URLs

| Page   | URL        |
| ------ | ---------- |
| Home   | `/`        |
| Signup | `/signup/` |
| Login  | `/login/`  |

Full URLs:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/signup/
http://127.0.0.1:8000/login/
```

---

# Registration Process

Open:

```text
http://127.0.0.1:8000/signup/
```

Enter the student details:

```text
Username: *****
Password: *****
Contact: *****
Email: *****
Address: *****
```

Click **Signup**.

If registration succeeds:

```text
Registration Successful
```

The details are inserted into the MySQL `users` table.

If the username already exists:

```text
Username already exists
```

---

# Login Process

Open:

```text
http://127.0.0.1:8000/login/
```

Enter the registered credentials.

If the credentials are correct:

```text
Welcome *****

Login successful.
```

If the credentials are incorrect:

```text
Invalid username or password
```

The login page also contains:

```text
Continue to Signup
```

---

# MySQL Database Verification

Select the database:

```sql
USE student;
```

Check the current database:

```sql
SELECT DATABASE();
```

Expected:

```text
student
```

Show tables:

```sql
SHOW TABLES;
```

Check the table structure:

```sql
DESCRIBE users;
```

Check all registered users:

```sql
SELECT * FROM users;
```

---

# Check Login Credentials

To verify whether a particular username and password exist:

```sql
SELECT *
FROM users
WHERE username = '*****'
AND password = '*****';
```

If a matching row is returned, the credentials exist.

If no row is returned, the credentials do not match the database.

> Real usernames and passwords are intentionally hidden from this README.

---

# Complete MySQL Verification Flow

```text
USE student;
       ↓
SELECT DATABASE();
       ↓
SHOW TABLES;
       ↓
DESCRIBE users;
       ↓
SELECT * FROM users;
       ↓
Check user data
       ↓
Test login
```

---

# Output

## 1. Home Page

The application displays:

```text
Student Registration and Login System

Signup

Login
```

## 2. Signup Page

The registration form contains:

```text
Username
Password
Contact
Email
Address

Signup
```

Successful registration:

```text
Registration Successful
```

Duplicate username:

```text
Username already exists
```

## 3. Login Page

The login page contains:

```text
Student Login

Username
Password

Login

Don't have an account?
Continue to Signup
```

## 4. Successful Login

```text
Welcome *****

Login successful.
```

## 5. Invalid Login

```text
Invalid username or password
```

## 6. MySQL Output

The `users` table contains registered student records.

Actual credentials are intentionally hidden from this README.

---

# Application Flow

```text
                    Student
                       |
                       ↓
                  Home Page
                  /        \
                 /          \
                ↓            ↓
             Signup        Login
                |             |
                ↓             ↓
        Enter Student      Enter
           Details       Credentials
                |             |
                ↓             ↓
             views.py      views.py
                |             |
                └──────┬──────┘
                       ↓
                     MySQL
                       |
                       ↓
                  users table
                       |
                       ↓
                Validate Data
                  /       \
                 /         \
                ↓           ↓
             Valid       Invalid
                |           |
                ↓           ↓
           Home Page    Login Page
                       with Message
```

---

# Database Structure

### Database

```text
student
```

### Table

```text
users
```

### Columns

| Column   | Data Type    | Description      |
| -------- | ------------ | ---------------- |
| id       | INT          | Primary key      |
| username | VARCHAR(100) | Student username |
| password | VARCHAR(255) | Student password |
| contact  | VARCHAR(15)  | Contact number   |
| email    | VARCHAR(100) | Email address    |
| address  | VARCHAR(255) | Student address  |

---

# Security Note

This project is designed primarily for learning purposes.

The current implementation stores passwords directly in MySQL. **Plain-text password storage should not be used in a production application.**

A production version should use:

* Django password hashing
* Django authentication system
* Sessions
* Logout functionality
* Environment variables
* Secure database configuration
* Server-side input validation
* Proper error handling

Never commit real database passwords, API keys, or other secrets to GitHub.

---

# Future Improvements

* Django authentication system
* Password hashing
* Session-based authentication
* Logout functionality
* User profile page
* Forgot password
* Bootstrap responsive design
* Improved form validation
* Admin dashboard
* Environment variable configuration
* Better error handling
* Secure password reset
* Database models using Django ORM

---

# Learning Outcomes

This project demonstrates:

* Django project creation
* Django application creation
* Adding an app to `settings.py`
* Django URL routing
* Django views
* HTML forms
* POST requests
* CSRF protection
* CSS styling
* MySQL database creation
* MySQL table creation
* PyMySQL connection
* SQL `SELECT` queries
* SQL `INSERT` queries
* Username validation
* Login validation
* Frontend-to-backend communication
* MySQL debugging
* Basic web application development

---

# Author

**Kammineni Venkata Manasa**

B.Tech – Computer Science & Engineering

---

# Project Status

**Completed**

Current workflow:

```text
Signup
   ↓
Enter Student Details
   ↓
Store User in MySQL
   ↓
Login
   ↓
Validate Username & Password
   ↓
Successful / Invalid Login Output
```



