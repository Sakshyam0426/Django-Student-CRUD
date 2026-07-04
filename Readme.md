<div align="center">

# 🎓 Django Student CRUD System

A full-featured Student Management System built with **Django** and **Bootstrap 5**.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

</div>

---

## 📋 Features

- ✅ Dashboard with student statistics
- ✅ Add, View, Edit, Delete students (CRUD)
- ✅ Search students by name, ID, or email
- ✅ Pagination (5 students per page)
- ✅ Export student list to CSV
- ✅ Print student ID card
- ✅ User Login / Register / Logout
- ✅ Forgot Password / Reset Password

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.14, Django 6.0 |
| **Frontend** | Bootstrap 5, Bootstrap Icons |
| **Database** | SQLite3 |
| **Language** | Python |

---

## 📁 Project Structure

```
Django-Student-CRUD/
│
├── env/
│
├── firstapp/
│   ├── __pycache__/
│   ├── migrations/
│   ├── media/
│   ├── templates/firstapp/
│   │   ├── Base.html
│   │   ├── change_password.html
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── password_reset.html
│   │   ├── password_reset_done.html
│   │   ├── password_reset_confirm.html
│   │   ├── password_reset_complete.html
│   │   ├── register.html
│   │   ├── student_add.html
│   │   ├── student_card.html
│   │   ├── student_confirm_delete.html
│   │   ├── student_detail.html
│   │   ├── student_edit.html
│   │   └── student_list.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── myproject/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Django-Student-CRUD.git
cd Django-Student-CRUD
```

### 2. Create and activate virtual environment
```bash
python -m venv env

# Windows
env\Scripts\activate

# Mac/Linux
source env/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (admin)
```bash
python manage.py createsuperuser
```

### 6. Run the server
```bash
python manage.py runserver
```

### 7. Open in browser
```
http://127.0.0.1:8000/
```

---

## 👤 Student Model Fields

| Field | Type | Description |
|---|---|---|
| `name` | CharField | Full name |
| `student_id` | CharField | Unique student ID |
| `email` | EmailField | Email address |
| `phone` | CharField | Phone number |
| `address` | TextField | Home address |
| `gender` | CharField | Male / Female / Other |
| `date_of_birth` | DateField | Date of birth |
| `enrolled_data` | DateTimeField | Auto enrollment date |

---

## 📸 Pages

| Page | URL |
|---|---|
| Dashboard | `/` |
| Student List | `/students/` |
| Add Student | `/add/` |
| Student Detail | `/detail/<id>/` |
| Edit Student | `/edit/<id>/` |
| Delete Student | `/delete/<id>/` |
| Export CSV | `/export/` |
| Print Card | `/card/<id>/` |
| Login | `/login/` |
| Register | `/register/` |
| Forgot Password | `/password-reset/` |

---

## 📦 Requirements

```
Django>=6.0
```

To auto-generate `requirements.txt` with all installed packages:
```bash
pip freeze > requirements.txt
```

---

## 🙏 Credits

Built with **Django** & **Bootstrap 5** by [Sakshyam Paudel](https://github.com/Sakshyam0426)
