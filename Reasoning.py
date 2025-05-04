import pandas as pd  # type: ignore # Library untuk membaca dan menyimpan file Excel

# ---------- 1. Fungsi Fuzzifikasi untuk Kualitas Servis ----------
def fuzzify_servis(value):
    # Mengubah nilai kualitas pelayanan yang menggunakan poin menjadi derajat keanggotaan fuzzy:
    # Buruk, Cukup, Baik. Menggunakan fungsi segitiga.

    if value <= 40:
        return {'buruk': 1, 'cukup': 0, 'baik': 0}
    elif 40 < value < 60:
        return {
            'buruk': (60 - value) / 20,
            'cukup': (value - 40) / 20,
            'baik': 0
        }
    elif 60 <= value < 80:
        return {
            'buruk': 0,
            'cukup': (80 - value) / 20,
            'baik': (value - 60) / 20
        }
    else:  # value >= 80
        return {'buruk': 0, 'cukup': 0, 'baik': 1}

# ---------- 2. Fungsi Fuzzifikasi untuk Harga ----------
def fuzzify_harga(value):
    # Mengubah nilai harga yang menggunakan nominal menjadi fuzzy:
    # Murah, Sedang, Mahal. Menggunakan fungsi segitiga.
    
    if value <= 30000:
        return {'murah': 1, 'sedang': 0, 'mahal': 0}
    elif 30000 < value < 40000:
        return {
            'murah': (40000 - value) / 10000,
            'sedang': (value - 30000) / 10000,
            'mahal': 0
        }
    elif 40000 <= value < 50000:
        return {
            'murah': 0,
            'sedang': (50000 - value) / 10000,
            'mahal': (value - 40000) / 10000
        }
    else:  # value >= 50000
        return {'murah': 0, 'sedang': 0, 'mahal': 1}

# ---------- 3. Aturan Inferensi Fuzzy ----------
def inferensi(servis_fuzzy, harga_fuzzy):
    # Menggabungkan input fuzzy (servis & harga) dengan aturan IF-THEN
    # untuk menghasilkan output fuzzy berupa kelayakan: rendah, sedang, tinggi.
    
    rules = []

    # Mengkomombinasikan semua kemungkinan nilai fuzzy dari input
    for s_key, s_val in servis_fuzzy.items():
        for h_key, h_val in harga_fuzzy.items():
            min_val = min(s_val, h_val)  # Operator fuzzy: AND (minimum)
            if min_val == 0:
                continue  # Lewati jika salah satu derajat keanggotaan 0

            # Aturan-aturan fuzzy manual (9 kombinasi)
            if s_key == 'baik' and h_key == 'murah':
                rules.append(('tinggi', min_val))
            elif s_key == 'baik' and h_key == 'sedang':
                rules.append(('tinggi', min_val))
            elif s_key == 'baik' and h_key == 'mahal':
                rules.append(('sedang', min_val))
            elif s_key == 'cukup' and h_key == 'murah':
                rules.append(('tinggi', min_val))
            elif s_key == 'cukup' and h_key == 'sedang':
                rules.append(('sedang', min_val))
            elif s_key == 'cukup' and h_key == 'mahal':
                rules.append(('rendah', min_val))
            elif s_key == 'buruk' and h_key == 'murah':
                rules.append(('sedang', min_val))
            elif s_key == 'buruk' and h_key == 'sedang':
                rules.append(('rendah', min_val))
            elif s_key == 'buruk' and h_key == 'mahal':
                rules.append(('rendah', min_val))

    return rules

# ---------- 4. Defuzzifikasi ----------
def defuzzifikasi(rules):
    # Mengubah output fuzzy dari aturan menjadi numerik
    # menggunakan metode centroid (rata-rata tertimbang).

    # Representasi nilai numerik untuk output fuzzy
    kelayakan_values = {
        'rendah': 30,
        'sedang': 60,
        'tinggi': 90
    }

    # Hitung rata-rata tertimbang
    numerator = 0
    denominator = 0
    for kategori, nilai in rules:
        bobot = kelayakan_values[kategori]
        numerator += bobot * nilai
        denominator += nilai

    if denominator == 0:
        return 0  # Menghindari pembagian nol
    return numerator / denominator

# ---------- 5. Main Program ----------
# Membaca data dari file Excel
df = pd.read_excel('restoran.xlsx')

# Memeriksa kolom yang ada
print(f"Kolom yang ditemukan: {df.columns}")

# Memastikan kolom yang benar
if 'Pelayanan' not in df.columns or 'harga' not in df.columns:
    raise KeyError("Kolom 'Pelayanan' atau 'harga' tidak ditemukan dalam file Excel.")

# Memproses setiap baris untuk mendapatkan skor kelayakan
scores = []  # List untuk menyimpan skor dari setiap restoran

for i, row in df.iterrows():
    pelayanan = row['Pelayanan']
    harga = row['harga']

    # fuzzifikasi
    pelayanan_fuzzy = fuzzify_servis(pelayanan)
    harga_fuzzy = fuzzify_harga(harga)

    # inferensi
    rules = inferensi(pelayanan_fuzzy, harga_fuzzy)

    # Defuzzifikasi
    skor = defuzzifikasi(rules)

    # Simpan skor ke list
    scores.append(skor)

# Menambahkan kolom skor ke dataframe
df['Skor Kelayakan'] = scores

# Mengurutkan dan ambil 5 restoran terbaik
top5 = df.sort_values(by='Skor Kelayakan', ascending=False).head(5)

# Menyimpan hasil ke file Excel
top5.to_excel('peringkat.xlsx', index=False)

print("✅ Selesai! File 'peringkat.xlsx' berisi 5 restoran terbaik berdasarkan fuzzy logic.")
