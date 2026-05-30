# 🚀 Flexi Health - Enterprise Modular Backend
A robust, highly scalable, and production-ready Flask Backend Architecture implementing the Application Factory Pattern and Role-Based Access Control (RBAC). Built with security-first principles, automated request logging, and structured database lifecycle management.

## 🛠️ Tech Stack & Key Features
- **Core Framework:** Flask 3.x (Modular Blueprints Layout)
- **Database Layer:** SQLite3 (Encapsulated Thread-Safe Context Hooks)
- **Security Protocols:** PBKDF2 Password Hashing, Session Fixation Countermeasures, and Strict HTTP Security Headers (XSS/Clickjacking protections)
- **Environment Management:** Class-based configurations isolated via `python-dotenv`
- **Payment Gateway:** SSLCommerz (10% Auto-Savings Protocol)

## 📂 Project Architecture
flexi_health/
├── models/
│   ├── __init__.py
│   └── user.py
├── routes/
│   ├── __init__.py
│   ├── admin.py
│   ├── auth.py
│   ├── dashboard.py
│   └── payment.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   ├── admin/
│   │   ├── dashboard.html
│   │   └── requests.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── dashboard/
│   │   └── index.html
│   ├── errors/
│   │   ├── 403.html
│   │   ├── 404.html
│   │   └── 500.html
│   └── base.html
├── utils/
│   ├── __init__.py
│   ├── db.py
│   └── security.py
├── .env
├── .gitignore
├── app.py
├── config.py
├── Procfile
├── requirements.txt
└── schema.sql

## 🚀 Getting Started

### 1. Clone the repository
git clone https://github.com/yourusername/flexi-health.git
cd flexi-health

### 2. Create .env file
FLASK_SECRET_KEY=your_strong_secret_key_here
SSLCOMMERZ_STORE_ID=your_store_id
SSLCOMMERZ_STORE_PASSWORD=your_store_password

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the application
python app.py

## 👤 Default Roles
| Role | Access |
|------|--------|
| user | Dashboard, Services, Recharge |
| admin | Admin Console, User Management, Service Requests |

## 💰 How Savings Work
1. User recharges mobile via the app
2. 10% of recharge amount saved automatically
3. After 500 BDT saved, all services unlock

## 🔐 Security Features
- PBKDF2 Password Hashing
- Session Fixation Protection
- HTTP Security Headers (XSS, Clickjacking)
- Role-Based Access Control (RBAC)
- SQLite Foreign Key Enforcement

## 📄 License
© 2026 Flexi Health. All rights reserved.
