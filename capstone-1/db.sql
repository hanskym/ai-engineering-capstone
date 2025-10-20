-- Create Database
CREATE DATABASE IF NOT EXISTS hospital_management;
USE hospital_management;

-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pasien VARCHAR(100) NOT NULL,
    umur INT NOT NULL,
    jenis_kelamin ENUM('Laki-laki', 'Perempuan') NOT NULL,
    jenis_rawat ENUM('Rawat Jalan', 'Rawat Inap') NOT NULL,
    biaya_pengobatan DECIMAL(10,2) NOT NULL,
    tanggal_masuk DATE NOT NULL,
    alamat VARCHAR(200),
    nomor_telepon VARCHAR(15)
);

-- Insert sample data
INSERT INTO patients (nama_pasien, umur, jenis_kelamin, jenis_rawat, biaya_pengobatan, tanggal_masuk, alamat, nomor_telepon) VALUES
('Fajar Hidayat', 40, 'Laki-laki', 'Rawat Inap', 2750000.00, '2024-03-02', 'Jl. Asia Afrika No. 10', '082112345678'),
('Putri Anggraini', 27, 'Perempuan', 'Rawat Jalan', 130000.00, '2024-03-05', 'Jl. Melati No. 22', '082223456789'),
('Rangga Saputra', 33, 'Laki-laki', 'Rawat Jalan', 185000.00, '2024-03-08', 'Jl. Mawar No. 35', '082334567890'),
('Clara Setiani', 48, 'Perempuan', 'Rawat Inap', 2950000.00, '2024-03-10', 'Jl. Kenanga No. 44', '082445678901'),
('Yoga Pratama', 31, 'Laki-laki', 'Rawat Jalan', 160000.00, '2024-03-12', 'Jl. Cendana No. 57', '082556789012'),
('Nadia Rahma', 54, 'Perempuan', 'Rawat Inap', 3700000.00, '2024-03-15', 'Jl. Anggrek No. 68', '082667890123'),
('Rizky Kurniawan', 39, 'Laki-laki', 'Rawat Inap', 2450000.00, '2024-03-18', 'Jl. Flamboyan No. 72', '082778901234'),
('Dian Lestari', 26, 'Perempuan', 'Rawat Jalan', 145000.00, '2024-03-20', 'Jl. Teratai No. 81', '082889012345'),
('Anton Susilo', 58, 'Laki-laki', 'Rawat Inap', 4100000.00, '2024-03-22', 'Jl. Dahlia No. 93', '082990123456'),
('Mega Puspita', 34, 'Perempuan', 'Rawat Jalan', 175000.00, '2024-03-25', 'Jl. Sakura No. 104', '083101234567'),
('Dedi Firmansyah', 46, 'Laki-laki', 'Rawat Inap', 2600000.00, '2024-03-27', 'Jl. Angsana No. 115', '083212345678'),
('Selvi Maharani', 30, 'Perempuan', 'Rawat Jalan', 155000.00, '2024-03-29', 'Jl. Ketapang No. 126', '083323456789'),
('Halim Perdana', 53, 'Laki-laki', 'Rawat Inap', 3400000.00, '2024-04-01', 'Jl. Cemara No. 138', '083434567890'),
('Ayu Kartika', 41, 'Perempuan', 'Rawat Jalan', 190000.00, '2024-04-03', 'Jl. Bougenville No. 149', '083545678901'),
('Taufik Ismail', 37, 'Laki-laki', 'Rawat Inap', 2300000.00, '2024-04-05', 'Jl. Pinus No. 152', '083656789012'),
('Mira Anggun', 29, 'Perempuan', 'Rawat Jalan', 140000.00, '2024-04-07', 'Jl. Kamboja No. 163', '083767890123'),
('Heri Susanto', 44, 'Laki-laki', 'Rawat Inap', 3150000.00, '2024-04-09', 'Jl. Palem No. 174', '083878901234'),
('Ratna Dewi', 36, 'Perempuan', 'Rawat Jalan', 170000.00, '2024-04-11', 'Jl. Kenari No. 185', '083989012345'),
('Bagus Pranata', 51, 'Laki-laki', 'Rawat Inap', 3550000.00, '2024-04-13', 'Jl. Merpati No. 196', '084101234567'),
('Yuni Safitri', 28, 'Perempuan', 'Rawat Jalan', 150000.00, '2024-04-15', 'Jl. Elang No. 207', '084212345678'),
('Andre Putra', 47, 'Laki-laki', 'Rawat Inap', 2850000.00, '2024-04-17', 'Jl. Rajawali No. 218', '084323456789'),
('Citra Melani', 32, 'Perempuan', 'Rawat Jalan', 165000.00, '2024-04-19', 'Jl. Walet No. 229', '084434567890'),
('Samuel Aditya', 55, 'Laki-laki', 'Rawat Inap', 3900000.00, '2024-04-21', 'Jl. Nuri No. 240', '084545678901'),
('Intan Permata', 43, 'Perempuan', 'Rawat Jalan', 180000.00, '2024-04-23', 'Jl. Cendrawasih No. 251', '084656789012'),
('Yusuf Haryanto', 38, 'Laki-laki', 'Rawat Inap', 2500000.00, '2024-04-25', 'Jl. Jalak No. 262', '084767890123');
