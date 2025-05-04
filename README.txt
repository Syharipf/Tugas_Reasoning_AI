==================================================
       PROGRAM PEMILIHAN RESTORAN TERBAIK
          (Menggunakan Logika Fuzzy)
==================================================

1. DESKRIPSI
Program ini dirancang untuk memilih 5 restoran terbaik 
di Bandung berdasarkan 2 kriteria:
- Kualitas pelayanan (skala 1-100)
- Harga (Rp 25.000 - 55.000)

2. PERSYARATAN
- Python 3.x (https://www.python.org/downloads/)
- Library openpyxl (install dengan: pip install openpyxl)

3. CARA MENGGUNAKAN:
1. Siapkan file data restoran.xlsx dengan format:
   - Kolom A: ID Restoran (angka)
   - Kolom B: Kualitas Pelayanan (1-100)
   - Kolom C: Harga (contoh: 30000)

2. Simpan file restoran.xlsx dalam folder yang sama 
   dengan file program ini

3. Jalankan program dengan command:
   python Reasoning.py

4. Hasil akan tersimpan otomatis dalam file:
   peringkat.xlsx

4. STRUKTUR FILE
Folder Anda harus berisi:
- Reasoning.py (file program utama)
- restoran.xlsx (file data input)
- peringkat.xlsx (akan dibuat otomatis)

5. CONTOH DATA
Contoh isi restoran.xlsx:
ID  Pelayanan  Harga
1   85         35000
2   90         28000
3   78         40000

6. TROUBLESHOOTING
- Jika error, pastikan:
  * File Excel tidak sedang dibuka
  * Format data sesuai petunjuk
  * Sudah install Python dan openpyxl
  * Nama file tepat 'restoran.xlsx'
