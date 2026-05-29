-- ==========================================================
-- Flexi Health Production Database Schema
-- Optimized for Flask + SQLite3 Architecture
-- ==========================================================

-- 1. Users Table: Centralized identity repository
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user', -- 'user' or 'admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Savings Accounts Table: Micro-savings ledger linked to users
CREATE TABLE IF NOT EXISTS savings_accounts (
    user_id INTEGER PRIMARY KEY,
    balance REAL DEFAULT 0.0,
    min_threshold REAL DEFAULT 500.0,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Transactions Table: Audit trail for all financial activity
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    transaction_type TEXT NOT NULL, -- 'recharge', 'service_fee', etc.
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Healthcare Providers Table: Emergency directory system
CREATE TABLE IF NOT EXISTS healthcare_providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL, -- 'Hospital', 'Ambulance', 'Blood Donor'
    type TEXT, -- 'Government', 'Private'
    zilla TEXT NOT NULL,
    city TEXT NOT NULL,
    reception_number TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creating Indices for Faster Searches
CREATE INDEX IF NOT EXISTS idx_location ON healthcare_providers (zilla, city);
CREATE INDEX IF NOT EXISTS idx_user_email ON users (email);
CREATE INDEX IF NOT EXISTS idx_user_phone ON users (phone);
