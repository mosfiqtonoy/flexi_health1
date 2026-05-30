-- ==========================================================
-- Flexi Health Production Database Schema
-- ==========================================================

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Savings Accounts Table
CREATE TABLE IF NOT EXISTS savings_accounts (
    user_id INTEGER PRIMARY KEY,
    balance REAL DEFAULT 0.0,
    min_threshold REAL DEFAULT 500.0,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Transactions Table
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    transaction_type TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Healthcare Providers Table
CREATE TABLE IF NOT EXISTS healthcare_providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    type TEXT,
    zilla TEXT NOT NULL,
    city TEXT NOT NULL,
    reception_number TEXT NOT NULL,
    latitude REAL,
    longitude REAL
);

-- 5. Doctors Table
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    hospital_name TEXT,
    zilla TEXT NOT NULL,
    city TEXT NOT NULL,
    phone TEXT NOT NULL
);

-- 6. Blood Donors Table
CREATE TABLE IF NOT EXISTS blood_donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    blood_group TEXT NOT NULL,
    zilla TEXT NOT NULL,
    city TEXT NOT NULL,
    phone TEXT NOT NULL,
    last_donated DATE
);

-- 7. Service Requests Table
CREATE TABLE IF NOT EXISTS service_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    service_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_healthcare_loc ON healthcare_providers (zilla, city);
CREATE INDEX IF NOT EXISTS idx_doctor_search ON doctors (specialization, zilla, city);
CREATE INDEX IF NOT EXISTS idx_blood_donor_search ON blood_donors (blood_group, zilla, city);
CREATE INDEX IF NOT EXISTS idx_users_phone ON users (phone);
CREATE INDEX IF NOT EXISTS idx_service_requests ON service_requests (status, created_at);
