from datetime import date
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, Date, DECIMAL, ForeignKey, DateTime, func
from flask_login import UserMixin
from database import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

class Pasien(db.Model):
    __tablename__ = 'pasien'
    id_pasien = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(100), nullable=False)
    no_hp = Column(String(20))
    alamat = Column(Text)
    tgl_lahir = Column(Date)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    transaksi = relationship('Transaksi', backref='pasien', cascade='all, delete-orphan')

class Pegawai(db.Model):
    __tablename__ = 'pegawai'
    id_pegawai = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(100), nullable=False)
    no_hp = Column(String(20))
    jabatan = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    detail_transaksi_layanan = relationship('DetailTransaksiLayanan', backref='pegawai', cascade='all, delete-orphan')
    layanan_pegawai = relationship('LayananPegawai', backref='pegawai', cascade='all, delete-orphan')

class KategoriLayanan(db.Model):
    __tablename__ = 'kategori_layanan'
    id_kategori = Column(Integer, primary_key=True, autoincrement=True)
    nama_kategori = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    layanan = relationship('Layanan', backref='kategori', cascade='all, delete-orphan')

class Layanan(db.Model):
    __tablename__ = 'layanan'
    id_layanan = Column(Integer, primary_key=True, autoincrement=True)
    nama_layanan = Column(String(100), nullable=False)
    id_kategori = Column(Integer, ForeignKey('kategori_layanan.id_kategori', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    layanan_pegawai = relationship('LayananPegawai', backref='layanan', cascade='all, delete-orphan')
    detail_transaksi_layanan = relationship('DetailTransaksiLayanan', backref='layanan', cascade='all, delete-orphan')
    detail_transaksi_produk = relationship('DetailTransaksiProduk', backref='layanan', cascade='all, delete-orphan')

class LayananPegawai(db.Model):
    __tablename__ = 'layanan_pegawai'
    id_layanan = Column(Integer, ForeignKey('layanan.id_layanan', ondelete='CASCADE'), primary_key=True)
    id_pegawai = Column(Integer, ForeignKey('pegawai.id_pegawai', ondelete='CASCADE'), primary_key=True)
    biaya = Column(DECIMAL(12,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Produk(db.Model):
    __tablename__ = 'produk'
    id_produk = Column(Integer, primary_key=True, autoincrement=True)
    nama_produk = Column(String(100), nullable=False)
    harga = Column(DECIMAL(12,2), nullable=False)
    stok = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    detail_transaksi_produk = relationship('DetailTransaksiProduk', backref='produk', cascade='all, delete-orphan')

class Transaksi(db.Model):
    __tablename__ = 'transaksi'
    id_transaksi = Column(Integer, primary_key=True, autoincrement=True)
    id_pasien = Column(Integer, ForeignKey('pasien.id_pasien', ondelete='CASCADE'), nullable=False)
    tanggal = Column(Date, nullable=False)
    total_harga = Column(DECIMAL(12,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    detail_transaksi_layanan = relationship('DetailTransaksiLayanan', backref='transaksi', cascade='all, delete-orphan')
    detail_transaksi_produk = relationship('DetailTransaksiProduk', backref='transaksi', cascade='all, delete-orphan')


class DetailTransaksiLayanan(db.Model):
    __tablename__ = 'detail_transaksi_layanan'
    id_detailLayanan = Column(Integer, primary_key=True, autoincrement=True)
    id_transaksi = Column(Integer, ForeignKey('transaksi.id_transaksi', ondelete='CASCADE'), nullable=False)
    id_pegawai = Column(Integer, ForeignKey('pegawai.id_pegawai', ondelete='CASCADE'), nullable=False)
    id_layanan = Column(Integer, ForeignKey('layanan.id_layanan', ondelete='CASCADE'), nullable=False)
    kuantitas = Column(Integer, nullable=False)
    subtotal = Column(DECIMAL(12,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class DetailTransaksiProduk(db.Model):
    __tablename__ = 'detail_transaksi_produk'
    id_detailProduk = Column(Integer, primary_key=True, autoincrement=True)
    id_transaksi = Column(Integer, ForeignKey('transaksi.id_transaksi', ondelete='CASCADE'), nullable=False)
    id_produk = Column(Integer, ForeignKey('produk.id_produk', ondelete='CASCADE'), nullable=False)
    id_layanan = Column(Integer, ForeignKey('layanan.id_layanan', ondelete='CASCADE'), nullable=True)
    kuantitas = Column(Integer, nullable=False)
    subtotal = Column(DECIMAL(12,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now()) 