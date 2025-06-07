-- Drop the database if it exists
USE master;
GO

IF EXISTS (SELECT name FROM sys.databases WHERE name = 'MyFlaskDB')
BEGIN
    ALTER DATABASE MyFlaskDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE MyFlaskDB;
END
GO

-- Create new database
CREATE DATABASE MyFlaskDB;
GO

USE MyFlaskDB;
GO

DROP TABLE IF EXISTS detail_transaksi_produk;
DROP TABLE IF EXISTS detail_transaksi_layanan;
DROP TABLE IF EXISTS layanan_pegawai;
DROP TABLE IF EXISTS transaksi;
DROP TABLE IF EXISTS produk;
DROP TABLE IF EXISTS layanan;
DROP TABLE IF EXISTS kategori_layanan;
DROP TABLE IF EXISTS pegawai;
DROP TABLE IF EXISTS pasien;
DROP TABLE IF EXISTS users;
GO

CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(100) NOT NULL UNIQUE,
    password NVARCHAR(255) NOT NULL
);
GO

CREATE TABLE pasien (
    id_pasien INT IDENTITY(1,1) PRIMARY KEY,
    nama NVARCHAR(100) NOT NULL,
    no_hp NVARCHAR(20),
    alamat NVARCHAR(MAX),
    tgl_lahir DATE,
    gender BIT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);
GO

CREATE TABLE pegawai (
    id_pegawai INT IDENTITY(1,1) PRIMARY KEY,
    nama NVARCHAR(100) NOT NULL,
    no_hp NVARCHAR(20),
    jabatan NVARCHAR(50),
    gender BIT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);
GO

CREATE TABLE kategori_layanan (
    id_kategori INT IDENTITY(1,1) PRIMARY KEY,
    nama_kategori NVARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);
GO

CREATE TABLE layanan (
    id_layanan INT IDENTITY(1,1) PRIMARY KEY,
    nama_layanan NVARCHAR(100) NOT NULL,
    id_kategori INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_kategori) REFERENCES kategori_layanan(id_kategori) ON DELETE CASCADE
);
GO

CREATE TABLE produk (
    id_produk INT IDENTITY(1,1) PRIMARY KEY,
    nama_produk NVARCHAR(100) NOT NULL,
    harga DECIMAL(12,2) NOT NULL,
    stok INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);
GO

CREATE TABLE transaksi (
    id_transaksi INT IDENTITY(1,1) PRIMARY KEY,
    id_pasien INT NOT NULL,
    tanggal DATE NOT NULL,
    total_harga DECIMAL(12,2) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_pasien) REFERENCES pasien(id_pasien) ON DELETE CASCADE
);
GO

CREATE TABLE layanan_pegawai (
    id_layanan INT NOT NULL,
    id_pegawai INT NOT NULL,
    biaya DECIMAL(12,2) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    PRIMARY KEY (id_layanan, id_pegawai),
    FOREIGN KEY (id_layanan) REFERENCES layanan(id_layanan) ON DELETE CASCADE,
    FOREIGN KEY (id_pegawai) REFERENCES pegawai(id_pegawai) ON DELETE CASCADE
);
GO

CREATE TABLE detail_transaksi_layanan (
    id_detailLayanan INT IDENTITY(1,1) PRIMARY KEY,
    id_transaksi INT NOT NULL,
    id_pegawai INT NOT NULL,
    id_layanan INT NOT NULL,
    kuantitas INT NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi) ON DELETE CASCADE,
    FOREIGN KEY (id_pegawai) REFERENCES pegawai(id_pegawai) ON DELETE NO ACTION,
    FOREIGN KEY (id_layanan) REFERENCES layanan(id_layanan) ON DELETE NO ACTION
);
GO

CREATE TABLE detail_transaksi_produk (
    id_detailProduk INT IDENTITY(1,1) PRIMARY KEY,
    id_transaksi INT NOT NULL,
    id_produk INT NOT NULL,
    id_layanan INT NULL,
    kuantitas INT NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi) ON DELETE CASCADE,
    FOREIGN KEY (id_produk) REFERENCES produk(id_produk) ON DELETE NO ACTION,
    FOREIGN KEY (id_layanan) REFERENCES layanan(id_layanan) ON DELETE NO ACTION
);
GO