Tabel Users (users)

CREATE TABLE users (
    id SERIAL PRIMARY KEY,                   -- ID pengguna, auto increment
    username VARCHAR(50) NOT NULL UNIQUE,    -- Username unik untuk login
    email VARCHAR(100) NOT NULL UNIQUE,      -- Email pengguna unik
    password_hash VARCHAR(255) NOT NULL,     -- Hash dari kata sandi (bukan kata sandi asli)
    role VARCHAR(20) DEFAULT 'user',         -- Peran pengguna, default 'user' (bisa 'admin', 'manager', dll.)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Waktu pembuatan akun
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Waktu pembaruan data terakhir
);
Tabel Login Attempts (login_attempts) Tabel ini menyimpan catatan percobaan login pengguna. Ini berguna untuk melacak aktivitas login, misalnya untuk mencegah brute-force attack atau memberikan peringatan ketika ada percobaan login yang gagal.

CREATE TABLE login_attempts (
    id SERIAL PRIMARY KEY,                   -- ID percobaan login
    user_id INTEGER,                         -- ID dari pengguna (relasi ke tabel users)
    ip_address VARCHAR(45),                  -- Alamat IP saat login
    user_agent TEXT,                         -- Informasi browser/klien yang digunakan
    success BOOLEAN,                         -- Apakah percobaan login berhasil atau gagal
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Waktu percobaan login
    FOREIGN KEY (user_id) REFERENCES users(id) -- Relasi ke tabel users
);
Tabel Password Resets (password_resets) Tabel ini menyimpan informasi tentang permintaan reset kata sandi. Ini berguna jika pengguna meminta untuk mereset kata sandi mereka melalui email.

CREATE TABLE password_resets (
    id SERIAL PRIMARY KEY,                   -- ID reset permintaan
    user_id INTEGER NOT NULL,                -- ID dari pengguna (relasi ke tabel users)
    token VARCHAR(255) NOT NULL,             -- Token unik untuk reset kata sandi
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Waktu permintaan reset kata sandi
    expired_at TIMESTAMP NOT NULL,           -- Waktu kedaluwarsa token reset
    FOREIGN KEY (user_id) REFERENCES users(id) -- Relasi ke tabel users
);