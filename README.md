# 📝 FastAPI Blog API

A secure, scalable, and modular REST API built using **FastAPI**, designed for managing blog posts with full **CRUD functionality**, **JWT authentication**, and **PostgreSQL** integration.

## 🚀 Features

- 🔐 JWT-based user authentication (OAuth2 Password Flow)
- 🧾 CRUD operations for blog posts
- 👥 User registration and login
- 🛠 Modular code structure (`routers/`, `schemas/`, `models/`, `auth/`)
- 📦 SQLAlchemy ORM + PostgreSQL
- 🔍 Data validation with Pydantic
- 🔄 Environment config using `.env` + `pydantic.BaseSettings`
- 🧪 Unit + Integration testing using Pytest
- 🌐 OpenAPI docs auto-generated (`/docs`)
- ☁️ Deployed on [Render](https://render.com)

---

## 📁 Project Structure

```bash
.
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── post.py
│   │   ├── user.py
│   │   └── auth.py
│   └── auth/
│       ├── hashing.py
│       └── token.py
├── .env
├── requirements.txt
├── Procfile

````

---

## ⚙️ Tech Stack

* **FastAPI** – Backend framework
* **PostgreSQL** – Relational DB
* **SQLAlchemy** – ORM
* **Pydantic** – Request & response validation
* **JWT (OAuth2)** – Authentication
* **Pytest** – Testing
* **Render** – Deployment platform

---

## 🔐 Authentication

Implemented using OAuth2 password flow + JWT tokens.

* `POST /register` – Create a new user
* `POST /login` – Generate JWT token
* Protected routes require `Authorization: Bearer <token>` header

---

## 🧪 Running Tests

```bash
pytest
```

Make sure to activate your virtual environment and set up your `.env` before running tests.

---

## 🧬 Environment Variables

Create a `.env` file in the root:

```env
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🛠 Setup & Run Locally

```bash
git clone https://github.com/rajveerpathak1/FastAPI-Blog-Project.git
cd FastAPI-Blog-Project

# Create virtual env & activate
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload
```

Go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the Swagger UI.

---

## 🌍 Deployed URL

🟢 **Live Demo**: https://socialmediaproject-backend-fastapi.onrender.com

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---
## 🙌 Acknowledgments

Built with ❤️ by [Rajveer Pathak](https://www.linkedin.com/in/rajveerpathak/)

```
