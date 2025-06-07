USE MyFlaskDB;
GO

-- Insert Kategori Layanan
INSERT INTO kategori_layanan (nama_kategori) VALUES
('Perawatan Rambut'),
('Perawatan Wajah'),
('Perawatan Kuku'),
('Perawatan Tubuh');
GO

-- Insert Layanan
INSERT INTO layanan (nama_layanan, id_kategori) VALUES
('Haircut', 1),
('Hair Coloring', 1),
('Facial Treatment', 2),
('Manicure', 3),
('Pedicure', 3),
('Massage', 4),
('Hair Spa', 1),
('Facial Clean Up', 2);
GO

-- Insert Pegawai
INSERT INTO pegawai (nama, no_hp, jabatan, gender) VALUES
('Budi Santoso', '081234567890', 'Hair Stylist', 0),      -- Laki-laki
('Siti Aminah', '082345678901', 'Beautician', 1),         -- Perempuan
('Ahmad Rizki', '083456789012', 'Massage Therapist', 0),  -- Laki-laki
('Dewi Lestari', '084567890123', 'Nail Artist', 1),       -- Perempuan
('Rudi Hartono', '085678901234', 'Hair Colorist', 0);     -- Laki-laki
GO

-- Insert Layanan Pegawai
INSERT INTO layanan_pegawai (id_layanan, id_pegawai, biaya) VALUES
(1, 1, 100000), -- Haircut by Budi
(2, 5, 250000), -- Hair Coloring by Rudi
(3, 2, 150000), -- Facial by Siti
(4, 4, 80000),  -- Manicure by Dewi
(5, 4, 100000), -- Pedicure by Dewi
(6, 3, 200000), -- Massage by Ahmad
(7, 1, 180000), -- Hair Spa by Budi
(8, 2, 120000); -- Facial Clean Up by Siti
GO

-- Insert Produk
INSERT INTO produk (nama_produk, harga, stok) VALUES
('Shampoo Premium', 85000, 50),
('Hair Color Kit', 150000, 30),
('Facial Cleanser', 120000, 40),
('Nail Polish', 75000, 60),
('Massage Oil', 95000, 45),
('Hair Mask', 110000, 35),
('Face Mask', 90000, 50),
('Nail Care Set', 130000, 25);
GO

-- Insert Pasien with registration dates and gender
INSERT INTO pasien (nama, no_hp, alamat, tgl_lahir, gender, created_at) VALUES
-- July 2024
('Ani Wijaya', '081234567891', 'Jl. Merdeka No. 1', '1990-05-15', 1, '2024-07-03 09:15:00'),
('Budi Pratama', '082345678902', 'Jl. Sudirman No. 2', '1985-08-20', 0, '2024-07-15 14:30:00'),
('Citra Dewi', '083456789013', 'Jl. Gatot Subroto No. 3', '1995-03-10', 1, '2024-07-28 11:45:00'),

-- August 2024
('Dian Kusuma', '084567890124', 'Jl. Thamrin No. 4', '1988-11-25', 1, '2024-08-05 10:20:00'),
('Eko Prasetyo', '085678901235', 'Jl. Asia Afrika No. 5', '1992-07-30', 0, '2024-08-18 15:40:00'),
('Fina Putri', '086789012346', 'Jl. Diponegoro No. 6', '1993-04-18', 1, '2024-08-25 13:10:00'),

-- September 2024
('Gita Sari', '087890123457', 'Jl. Veteran No. 7', '1991-09-22', 1, '2024-09-02 09:30:00'),
('Hadi Wijaya', '088901234568', 'Jl. Pahlawan No. 8', '1987-12-05', 0, '2024-09-15 16:20:00'),
('Indra Nugraha', '089012345679', 'Jl. Imam Bonjol No. 9', '1994-06-12', 0, '2024-09-28 11:15:00'),

-- October 2024
('Joko Susilo', '089123456780', 'Jl. Diponegoro No. 10', '1989-02-28', 0, '2024-10-05 14:45:00'),
('Kartika Dewi', '089234567891', 'Jl. Sudirman No. 11', '1996-08-15', 1, '2024-10-18 10:30:00'),
('Lina Wijaya', '089345678902', 'Jl. Gatot Subroto No. 12', '1993-11-20', 1, '2024-10-25 15:50:00'),

-- November 2024
('Mario Kusuma', '089456789013', 'Jl. Thamrin No. 13', '1990-04-05', 0, '2024-11-03 09:20:00'),
('Nina Putri', '089567890124', 'Jl. Asia Afrika No. 14', '1995-09-18', 1, '2024-11-15 13:40:00'),
('Oscar Pratama', '089678901235', 'Jl. Veteran No. 15', '1988-07-25', 0, '2024-11-28 16:10:00'),

-- December 2024
('Putri Sari', '089789012346', 'Jl. Pahlawan No. 16', '1992-01-30', 1, '2024-12-05 10:15:00'),
('Rudi Hartono', '089890123457', 'Jl. Imam Bonjol No. 17', '1987-03-12', 0, '2024-12-18 14:30:00'),
('Siti Aminah', '089901234568', 'Jl. Diponegoro No. 18', '1994-10-08', 1, '2024-12-25 11:45:00'),

-- January 2025
('Tono Wijaya', '089012345679', 'Jl. Sudirman No. 19', '1991-12-15', 0, '2025-01-05 15:20:00'),
('Umi Kusuma', '089123456780', 'Jl. Gatot Subroto No. 20', '1996-05-22', 1, '2025-01-18 09:30:00'),
('Vina Putri', '089234567891', 'Jl. Thamrin No. 21', '1993-08-28', 1, '2025-01-25 13:50:00'),

-- February 2025
('Wahyu Pratama', '089345678902', 'Jl. Asia Afrika No. 22', '1989-11-10', 0, '2025-02-03 16:15:00'),
('Xena Sari', '089456789013', 'Jl. Veteran No. 23', '1995-02-18', 1, '2025-02-15 10:40:00'),
('Yudi Hartono', '089567890124', 'Jl. Pahlawan No. 24', '1990-07-25', 0, '2025-02-28 14:20:00'),

-- March 2025
('Zara Aminah', '089678901235', 'Jl. Imam Bonjol No. 25', '1994-04-05', 1, '2025-03-05 11:30:00'),
('Ahmad Rizki', '089789012346', 'Jl. Diponegoro No. 26', '1988-09-12', 0, '2025-03-18 15:45:00'),
('Bella Kusuma', '089890123457', 'Jl. Sudirman No. 27', '1992-12-20', 1, '2025-03-25 09:15:00'),

-- April 2025
('Candra Putra', '089901234568', 'Jl. Imam Bonjol No. 28', '1996-03-15', 0, '2025-04-05 13:20:00'),
('Dewi Lestari', '089012345679', 'Jl. Thamrin No. 29', '1993-06-28', 1, '2025-04-18 16:30:00'),
('Erik Wijaya', '089123456780', 'Jl. Asia Afrika No. 30', '1991-10-05', 0, '2025-04-25 10:45:00'),

-- May 2025
('Fina Pratama', '089234567891', 'Jl. Veteran No. 31', '1995-01-18', 1, '2025-05-03 14:15:00'),
('Gunawan Sari', '089345678902', 'Jl. Pahlawan No. 32', '1989-08-22', 0, '2025-05-15 11:30:00'),
('Hani Aminah', '089456789013', 'Jl. Imam Bonjol No. 33', '1994-05-30', 1, '2025-05-28 15:40:00'),

-- June 2025
('Irfan Rizki', '089567890124', 'Jl. Diponegoro No. 34', '1992-11-12', 0, '2025-06-05 09:25:00'),
('Jasmine Kusuma', '089678901235', 'Jl. Sudirman No. 35', '1996-02-25', 1, '2025-06-18 13:35:00'),
('Kevin Putra', '089789012346', 'Jl. Gatot Subroto No. 36', '1993-07-08', 0, '2025-06-25 16:45:00'),

-- July 2025
('Lina Wijaya', '089890123457', 'Jl. Thamrin No. 37', '1991-04-15', 1, '2025-07-03 10:20:00'),
('Mario Pratama', '089901234568', 'Jl. Asia Afrika No. 38', '1995-09-28', 0, '2025-07-15 14:30:00'),
('Nina Sari', '089012345679', 'Jl. Veteran No. 39', '1990-12-05', 1, '2025-07-25 11:40:00');
GO

-- Insert Transaksi and Details (July 2024 - July 2025)
-- July 2024
INSERT INTO transaksi (id_pasien, tanggal, total_harga) VALUES
(1, '2024-07-03', 180000),
(2, '2024-07-10', 330000),
(3, '2024-07-17', 420000);
GO

INSERT INTO detail_transaksi_layanan (id_transaksi, id_pegawai, id_layanan, kuantitas, subtotal) VALUES
(1, 4, 4, 1, 80000),  -- Manicure
(1, 4, 5, 1, 100000), -- Pedicure
(2, 5, 2, 1, 250000), -- Hair Coloring
(2, 1, 1, 1, 100000), -- Haircut
(3, 1, 7, 1, 180000), -- Hair Spa
(3, 2, 3, 1, 150000), -- Facial
(3, 4, 5, 1, 100000); -- Pedicure
GO

-- August 2024
INSERT INTO transaksi (id_pasien, tanggal, total_harga) VALUES
(4, '2024-08-05', 430000),
(5, '2024-08-12', 280000),
(6, '2024-08-20', 350000);
GO

INSERT INTO detail_transaksi_layanan (id_transaksi, id_pegawai, id_layanan, kuantitas, subtotal) VALUES
(4, 5, 2, 1, 250000), -- Hair Coloring
(4, 1, 7, 1, 180000), -- Hair Spa
(5, 3, 6, 1, 200000), -- Massage
(5, 4, 4, 1, 80000),  -- Manicure
(6, 1, 1, 1, 100000), -- Haircut
(6, 5, 2, 1, 250000); -- Hair Coloring
GO

-- September 2024
INSERT INTO transaksi (id_pasien, tanggal, total_harga) VALUES
(7, '2024-09-03', 270000),
(8, '2024-09-10', 380000),
(1, '2024-09-17', 230000);
GO

INSERT INTO detail_transaksi_layanan (id_transaksi, id_pegawai, id_layanan, kuantitas, subtotal) VALUES
(7, 2, 3, 1, 150000), -- Facial
(7, 2, 8, 1, 120000), -- Facial Clean Up
(8, 5, 2, 1, 250000), -- Hair Coloring
(8, 4, 4, 1, 80000),  -- Manicure
(9, 3, 6, 1, 200000), -- Massage
(9, 4, 5, 1, 80000);  -- Pedicure
GO

-- October 2024
INSERT INTO transaksi (id_pasien, tanggal, total_harga) VALUES
(2, '2024-10-05', 305000),
(3, '2024-10-12', 420000),
(4, '2024-10-19', 280000);
GO

INSERT INTO detail_transaksi_produk (id_transaksi, id_produk, kuantitas, subtotal) VALUES
(10, 2, 1, 150000), -- Hair Color Kit
(10, 6, 1, 110000), -- Hair Mask
(10, 7, 1, 90000),  -- Face Mask
(11, 1, 3, 255000), -- 3x Shampoo Premium
(11, 3, 1, 120000), -- Facial Cleanser
(11, 5, 1, 95000),  -- Massage Oil
(12, 4, 2, 150000), -- 2x Nail Polish
(12, 8, 1, 130000); -- Nail Care Set
GO

-- November 2024
INSERT INTO transaksi (id_pasien, tanggal, total_harga) VALUES
(5, '2024-11-03', 180000),
(6, '2024-11-10', 330000),
(7, '2024-11-17', 450000);
GO

INSERT INTO detail_transaksi_layanan (id_transaksi, id_pegawai, id_layanan, kuantitas, subtotal) VALUES
(13, 3, 6, 1, 200000), -- Massage
(14, 5, 2, 1, 250000), -- Hair Coloring
(14, 1, 1, 1, 100000), -- Haircut
(15, 1, 7, 1, 180000), -- Hair Spa
(15, 2, 3, 1, 150000), -- Facial
(15, 4, 5, 1, 100000); -- Pedicure
GO

-- December 2024
INSERT INTO transaksi (id_pasien, tanggal, total_harga) VALUES
(8, '2024-12-05', 330000),
(1, '2024-12-12', 280000),
(2, '2024-12-19', 405000);
GO

INSERT INTO detail_transaksi_layanan (id_transaksi, id_pegawai, id_layanan, kuantitas, subtotal) VALUES
(16, 1, 1, 1, 100000), -- Haircut
(16, 5, 2, 1, 250000), -- Hair Coloring
(17, 3, 6, 1, 200000), -- Massage
(17, 4, 4, 1, 80000),  -- Manicure
(18, 1, 7, 1, 180000), -- Hair Spa
(18, 2, 3, 1, 150000), -- Facial
(18, 4, 5, 1, 100000); -- Pedicure
GO

-- January 2025
INSERT INTO transaksi (id_pasien, tanggal, total_harga) VALUES
(3, '2025-01-05', 350000),
(4, '2025-01-12', 280000),
(5, '2025-01-19', 420000);
GO

INSERT INTO detail_transaksi_layanan (id_transaksi, id_pegawai, id_layanan, kuantitas, subtotal) VALUES
(19, 1, 1, 1, 100000), -- Haircut
(19, 5, 2, 1, 250000), -- Hair Coloring
(20, 3, 6, 1, 200000), -- Massage
(20, 4, 4, 1, 80000),  -- Manicure
(21, 1, 7, 1, 180000), -- Hair Spa
(21, 2, 3, 1, 150000), -- Facial
(21, 4, 5, 1, 100000); -- Pedicure
GO

-- February 2025
INSERT INTO transaksi (id_pasien, tanggal, total_harga) VALUES
(6, '2025-02-03', 230000),
(7, '2025-02-10', 335000),
(8, '2025-02-17', 180000);
GO

INSERT INTO detail_transaksi_layanan (id_transaksi, id_pegawai, id_layanan, kuantitas, subtotal) VALUES
(22, 2, 3, 1, 150000), -- Facial
(22, 4, 4, 1, 80000),  -- Manicure
(23, 5, 2, 1, 250000), -- Hair Coloring
(23, 4, 5, 1, 100000), -- Pedicure
(24, 3, 6, 1, 200000); -- Massage
GO

-- March 2025
INSERT INTO transaksi (id_pasien, tanggal, total_harga) VALUES
(1, '2025-03-05', 280000),
(2, '2025-03-12', 430000),
(3, '2025-03-19', 195000);
GO

INSERT INTO detail_transaksi_layanan (id_transaksi, id_pegawai, id_layanan, kuantitas, subtotal) VALUES
(25, 3, 6, 1, 200000), -- Massage
(25, 4, 5, 1, 80000),  -- Pedicure
(26, 5, 2, 1, 250000), -- Hair Coloring
(26, 1, 7, 1, 180000), -- Hair Spa
(27, 1, 1, 1, 100000), -- Haircut
(27, 2, 8, 1, 120000); -- Facial Clean Up
GO

-- April 2025
INSERT INTO transaksi (id_pasien, tanggal, total_harga) VALUES
(4, '2025-04-03', 330000),
(5, '2025-04-10', 280000),
(6, '2025-04-17', 405000);
GO

INSERT INTO detail_transaksi_layanan (id_transaksi, id_pegawai, id_layanan, kuantitas, subtotal) VALUES
(28, 1, 7, 1, 180000), -- Hair Spa
(28, 2, 8, 1, 150000), -- Facial Clean Up
(29, 3, 6, 1, 200000), -- Massage
(29, 4, 4, 1, 80000),  -- Manicure
(30, 5, 2, 1, 250000), -- Hair Coloring
(30, 1, 1, 1, 100000), -- Haircut
(30, 2, 3, 1, 150000); -- Facial
GO

-- May 2025
INSERT INTO transaksi (id_pasien, tanggal, total_harga) VALUES
(7, '2025-05-05', 185000),
(8, '2025-05-12', 260000),
(1, '2025-05-19', 320000);
GO

INSERT INTO detail_transaksi_produk (id_transaksi, id_produk, kuantitas, subtotal) VALUES
(31, 1, 2, 170000), -- 2x Shampoo Premium
(31, 3, 1, 120000), -- 1x Facial Cleanser
(32, 2, 1, 150000), -- Hair Color Kit
(32, 6, 1, 110000), -- Hair Mask
(33, 4, 2, 150000), -- 2x Nail Polish
(33, 8, 1, 130000); -- Nail Care Set
GO

-- June 2025
INSERT INTO transaksi (id_pasien, tanggal, total_harga) VALUES
(2, '2025-06-03', 225000),
(3, '2025-06-10', 380000),
(4, '2025-06-17', 290000);
GO

INSERT INTO detail_transaksi_layanan (id_transaksi, id_pegawai, id_layanan, kuantitas, subtotal) VALUES
(34, 1, 1, 1, 100000), -- Haircut
(34, 2, 3, 1, 150000), -- Facial
(35, 5, 2, 1, 250000), -- Hair Coloring
(35, 4, 4, 1, 80000),  -- Manicure
(36, 3, 6, 1, 200000), -- Massage
(36, 2, 8, 1, 120000); -- Facial Clean Up
GO

-- July 2025
INSERT INTO transaksi (id_pasien, tanggal, total_harga) VALUES
(5, '2025-07-05', 180000),
(6, '2025-07-12', 330000),
(7, '2025-07-19', 420000);
GO

INSERT INTO detail_transaksi_layanan (id_transaksi, id_pegawai, id_layanan, kuantitas, subtotal) VALUES
(37, 4, 4, 1, 80000),  -- Manicure
(37, 4, 5, 1, 100000), -- Pedicure
(38, 5, 2, 1, 250000), -- Hair Coloring
(38, 1, 1, 1, 100000), -- Haircut
(39, 1, 7, 1, 180000), -- Hair Spa
(39, 2, 3, 1, 150000), -- Facial
(39, 4, 5, 1, 100000); -- Pedicure
GO 