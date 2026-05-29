# 🚀 Lexi Health - Enterprise Modular Backend

A robust, highly scalable, and production-ready **Flask Backend Architecture** implementing the **Application Factory Pattern** and **Role-Based Access Control (RBAC)**. Built with security-first principles, automated request logging, and structured database lifecycle management.

---

## 🛠️ Tech Stack & Key Features
- **Core Framework:** Flask 3.x (Modular Blueprints Layout)
- **Database Layer:** SQLite3 (Encapsulated Thread-Safe Context Hooks)
- **Security Protocols:** PBKDF2 Password Hashing, Session Fixation Countermeasures, and Strict HTTP Security Headers (XSS/Clickjacking protections)
- **Environment Management:** Class-based configurations isolated via `python-dotenv`

---

## 📂 Project Architecture
```text
lexi_health/
├── models/          # Business Logic & Data Schemas
├── routes/          # Isolated Component Blueprints (Auth, Admin, User)
├── utils/           # Shared System Utilities (DB Hooks, RBAC Guards)
├── templates/       # Dynamic UI Server Templates
├── .env.example     # Blueprint for Environment Configuration
├── .gitignore       # System Git exclusion parameters
├── app.py           # Production Application Factory Entry-Point
├── config.py        # Environment Configuration Matrix
├── Procfile         # WSGI Server Production Directives
└── requirements.txt # System Module Dependency Layout
