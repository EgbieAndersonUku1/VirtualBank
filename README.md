### VirtualBank dashboard (in progress) 

A **Django-based virtual banking dashboard** equipped with essential features such as user registration, email verification, wallet and card management, and admin-level tools for logging and verification, along with authentiation and limited bank utilities. 



## 🚀 Features

- 🔐 User Registration and Login
- ✅ Email Verification System with Admin Controls
- 💳 Add and Delete Cards
- 💰 Add Funds to Wallet or Bank
- 🔔 Notifications System
- 🛠 Admin Panel with Verification Code Generator
- 📬 Email Logger for Tracking Activity

---

## 🛠 Tech Stack

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript (Admin Enhancements)
- **Database**: SQLite (default for development)
- **Email**: SMTP (Gmail setup via environment variables)

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/EgbieAndersonUku1/VirtualBank.git
cd VirtualBank
````

### 2. Create a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file based on `.env.example` and add your email credentials:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

> 💡 For Gmail, generate an App Password if you have 2FA enabled.

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

Provide a username, email, first name, surname and password when prompted.

### 7. Start the Development Server

```bash
python manage.py runserver
```

---

## 🌐 How to Use

* 🔗 Visit `http://127.0.0.1:8000/register` to register a new user.
* 📩 A verification link will be sent to your email.
* ✅ Click the link to verify and activate your account.
* 🔐 Visit `http://127.0.0.1:8000/login` to log in.

### Admin Panel

* Navigate to `http://127.0.0.1:8000/admin`
* Use your superuser credentials to access advanced tools.

### Verification Code Generator (Admin Only)

* Admins and superusers can generate a random verification code using a "Generate Code" button on the verification page.
* The code is auto-inserted into the form input for quicker processing.

---

## 🎨  (To-Do / In Progress)
- Link the frontend
- Link the backend to the frontent






