-- =========================
-- USERS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE NOT NULL,

    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',

    -- wallet system
    balance INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,

    -- ===== Extended Profile =====
    date_of_birth TEXT,
    blood_group TEXT,
    address TEXT,

    latitude REAL,
    longitude REAL,

    -- reset system (email OTP / link)
    reset_token TEXT,
    reset_token_expiry INTEGER,

    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);


CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);


-- =========================
-- HEALTH RECORDS
-- =========================
CREATE TABLE IF NOT EXISTS health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,

    weight REAL,
    height REAL,

    blood_pressure_systolic INTEGER,
    blood_pressure_diastolic INTEGER,

    blood_type TEXT,
    notes TEXT,

    recorded_at TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_health_user ON health_records(user_id);


-- =========================
-- RECHARGE HISTORY
-- =========================
CREATE TABLE IF NOT EXISTS recharge_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,

    amount INTEGER NOT NULL,
    saved_amount INTEGER NOT NULL,
    operator TEXT NOT NULL,

    status TEXT NOT NULL DEFAULT 'completed',

    created_at TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_recharge_user ON recharge_history(user_id);


-- =========================
-- SERVICE REQUESTS
-- =========================
CREATE TABLE IF NOT EXISTS service_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,

    service_type TEXT NOT NULL,
    description TEXT,

    status TEXT NOT NULL DEFAULT 'pending',

    amount_used INTEGER DEFAULT 0,

    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_service_user ON service_requests(user_id);


-- =========================
-- ADMIN SEED USER
-- =========================
INSERT OR IGNORE INTO users (
    full_name,
    email,
    phone,
    password_hash,
    role,
    balance,
    is_active,
    blood_group
)
VALUES (
    'Admin',
    'admin@flexihealth.com',
    '01700000000',

    -- IMPORTANT: replace with real hashed password
    'pbkdf2:sha256:260000$adminseed$dummyhash',

    'admin',
    0,
    1,
    'O+'
);
