-- Membuat tabel untuk users (simple login)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE devices
ADD COLUMN reg_no VARCHAR(15);

-- Membuat tabel untuk perangkat GPS (devices)
CREATE TABLE public.devices (
    device_id VARCHAR(50) PRIMARY KEY,
    device_name VARCHAR(100),
    phone_number VARCHAR(15),
    reg_no VARCHAR(50)
);

-- Membuat tabel untuk history posisi GPS (histories)
CREATE TABLE histories (
    history_id SERIAL PRIMARY KEY,
    device_id INTEGER REFERENCES devices(device_id),
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    speed DECIMAL(10, 2),               -- dalam km/h                   
    recorded_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);