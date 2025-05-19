import pandas as pd
import numpy as np
import json
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Install library yang diperlukan
# pip install pandas numpy scipy matplotlib seaborn openpyxl

# Konfigurasi
FILE_EXCEL = 'kuisioner.xlsx'
SHEET_NAME = 0  # atau nama sheet
RESPONDEN = 35

# Daftar pertanyaan sesuai dengan kuisioner
PERTANYAAN_LIKERT = [
    'Saya senang belajar bahasa Jepang',
    'Saya aktif selama proses pembelajaran bahasa Jepang di kelas',
    'Saya memahami materi bahasa Jepang yang diajarkan oleh guru.',
    'Saya memiliki kebiasaan belajar bahasa Jepang secara mandiri di luar kelas',
    'Saya selalu mengerjakan tugas bahasa Jepang tepat waktu.',
    'Saya bertanya kepada guru ketika ada materi yang belum saya pahami.',
    'Saya tertarik dengan budaya Jepang (anime, drama, musik, dll.)',
    'Saya belajar bahasa Jepang untuk meningkatkan peluang karier di masa depan',
    'Saya mengalami kesulitan dalam mengingat huruf Hiragana',
    'Saya mengalami kesulitan dalam mengingat huruf Katakana',
    'Saya merasa sulit membedakan huruf Hiragana yang bentuknya mirip',
    'Saya merasa sulit membedakan huruf Katakana yang bentuknya mirip',
    'Saya kesulitan menulis huruf Hiragana dengan urutan garis yang benar.',
    'Saya kesulitan menulis huruf Katakana dengan urutan garis yang benar',
    'Saya kesulitan mengingat pelafalan huruf Jepang',
    'Saya kesulitan memahami kosakata bahasa Jepang',
    'Saya merasa kesulitan mempelajari huruf Jepang dengan metode pembelajaran konvensional.',
    'Saya merasa bosan saat belajar huruf Jepang hanya dengan buku dan LKPD',
    'Saya membutuhkan media pembelajaran interaktif untuk belajar huruf Hiragana dan Katakana',
    'Saya lebih tertarik belajar huruf Jepang dengan menggunakan smartphone/laptop.',
    'Saya ingin belajar huruf Jepang melalui permainan (game)',
    'Saya membutuhkan media pembelajaran yang dapat diakses kapan saja dan di mana saja.',
    'Saya tertarik belajar huruf Jepang dengan menggunakan video pembelajaran.',
    'Saya membutuhkan media pembelajaran yang memberikan umpan balik langsung terhadap jawaban saya.',
    'Saya tertarik belajar huruf Jepang dengan sistem pengulangan berkala (spaced repetition).',
    'Saya merasa terbantu jika ada fitur latihan menulis huruf Jepang dalam media pembelajaran.',
    'Saya tertarik jika media pembelajaran dilengkapi dengan contoh pengucapan yang benar.',
    'Saya tertarik jika media pembelajaran menampilkan peringkat/skor untuk memotivasi belajar.',
    'Media pembelajaran berbasis gamifikasi (poin, lencana, papan peringkat).',
    'Media pembelajaran yang dapat digunakan secara offline.',
    'Media pembelajaran yang memiliki tampilan visual menarik.',
    'Media pembelajaran yang dilengkapi dengan animasi.',
    'Media pembelajaran yang dilengkapi dengan audio/suara.',
    'Media pembelajaran yang menyediakan evaluasi secara real-time.',
    'Media pembelajaran yang memiliki tingkat kesulitan bertahap.',
    'Media pembelajaran yang dapat memonitor kemajuan belajar saya.',
    'Media pembelajaran yang mengintegrasikan unsur budaya Jepang.',
    'Media pembelajaran yang dapat digunakan untuk belajar secara berkelompok.'
]

PERTANYAAN_ISIAN = [
    '1. Kesulitan terbesar apa yang Anda alami dalam mempelajari huruf Jepang (Hiragana dan Katakana)?',
    '2. Strategi apa yang biasa Anda gunakan untuk mengingat huruf Jepang?',
    '3. Menurut Anda, elemen atau komponen pendukung apa yang perlu ada dalam media pembelajaran untuk memudahkan penguasaan huruf Jepang?',
    '4. Apa pendapat Anda tentang penggunaan teknologi (smartphone/laptop) dalam pembelajaran huruf Jepang?',
    '5. Saran atau masukan untuk peningkatan kualitas pembelajaran huruf Jepang'
]

PERTANYAAN_POSITIF = [
    'Saya senang belajar bahasa Jepang',
    'Saya aktif selama proses pembelajaran bahasa Jepang di kelas',
    'Saya memahami materi bahasa Jepang yang diajarkan oleh guru.',
    'Saya memiliki kebiasaan belajar bahasa Jepang secara mandiri di luar kelas',
    'Saya selalu mengerjakan tugas bahasa Jepang tepat waktu.',
    'Saya bertanya kepada guru ketika ada materi yang belum saya pahami.',
    'Saya tertarik dengan budaya Jepang (anime, drama, musik, dll.)',
    'Saya belajar bahasa Jepang untuk meningkatkan peluang karier di masa depan'
]

PERTANYAAN_NEGATIF = [
    'Saya mengalami kesulitan dalam mengingat huruf Hiragana',
    'Saya mengalami kesulitan dalam mengingat huruf Katakana',
    'Saya merasa sulit membedakan huruf Hiragana yang bentuknya mirip',
    'Saya merasa sulit membedakan huruf Katakana yang bentuknya mirip',
    'Saya kesulitan menulis huruf Hiragana dengan urutan garis yang benar.',
    'Saya kesulitan menulis huruf Katakana dengan urutan garis yang benar',
    'Saya kesulitan mengingat pelafalan huruf Jepang',
    'Saya kesulitan memahami kosakata bahasa Jepang',
    'Saya merasa kesulitan mempelajari huruf Jepang dengan metode pembelajaran konvensional.',
    'Saya merasa bosan saat belajar huruf Jepang hanya dengan buku dan LKPD'
]

# Mapping skala Likert
LIKERT_MAP = {
    1: "Sangat Tidak Setuju",
    2: "Tidak Setuju",
    3: "Ragu-Ragu",
    4: "Setuju",
    5: "Sangat Setuju"
}

# Baca data
df = pd.read_excel(FILE_EXCEL, sheet_name=SHEET_NAME)

# Fungsi untuk analisis deskriptif pertanyaan Likert
def analisis_likert(data, pertanyaan):
    hasil = {
        'pertanyaan': pertanyaan,
        'jenis': 'likert',
        'deskriptif': {
            'mean': round(data.mean(), 2),
            'median': data.median(),
            'modus': int(data.mode()[0]),
            'std_dev': round(data.std(), 2),
            'varians': round(data.var(), 2),
            'min': int(data.min()),
            'max': int(data.max()),
            'range': int(data.max() - data.min()),
            'skewness': round(data.skew(), 2),
            'kurtosis': round(data.kurtosis(), 2)
        },
        'frekuensi': {
            'Sangat Tidak Setuju': int(data.value_counts().get(1, 0)),
            'Tidak Setuju': int(data.value_counts().get(2, 0)),
            'Ragu-Ragu': int(data.value_counts().get(3, 0)),
            'Setuju': int(data.value_counts().get(4, 0)),
            'Sangat Setuju': int(data.value_counts().get(5, 0))
        },
        'persentase': {
            'Sangat Tidak Setuju': round(data.value_counts().get(1, 0) / RESPONDEN * 100, 1),
            'Tidak Setuju': round(data.value_counts().get(2, 0) / RESPONDEN * 100, 1),
            'Ragu-Ragu': round(data.value_counts().get(3, 0) / RESPONDEN * 100, 1),
            'Setuju': round(data.value_counts().get(4, 0) / RESPONDEN * 100, 1),
            'Sangat Setuju': round(data.value_counts().get(5, 0) / RESPONDEN * 100, 1)
        }
    }
    return hasil

# Fungsi untuk analisis pertanyaan isian
def analisis_isian(data, pertanyaan):
    # Hitung frekuensi jawaban untuk pertanyaan isian
    frekuensi = data.value_counts().to_dict()
    
    hasil = {
        'pertanyaan': pertanyaan,
        'jenis': 'isian',
        'jawaban': [{'teks': str(k), 'frekuensi': int(v)} for k, v in frekuensi.items()]
    }
    return hasil

# Fungsi untuk uji reliabilitas (Cronbach's Alpha)
def cronbach_alpha(df, pertanyaan_positif, pertanyaan_negatif):
    df_processed = df.copy()
    
    # Reverse scoring untuk pertanyaan negatif
    for col in pertanyaan_negatif:
        if col in df_processed.columns:
            df_processed[col] = 6 - df_processed[col]  # Reverse score 1-5 menjadi 5-1
    
    # Gabungkan semua pertanyaan
    semua_pertanyaan = [p for p in (pertanyaan_positif + pertanyaan_negatif) if p in df_processed.columns]
    df_items = df_processed[semua_pertanyaan]
    
    # Hitung Cronbach's Alpha
    k = df_items.shape[1]
    if k < 2:
        return 0  # Tidak bisa dihitung jika kurang dari 2 pertanyaan
    
    var_total = df_items.sum(axis=1).var()
    sum_var_items = df_items.var(axis=0).sum()
    
    alpha = (k / (k - 1)) * (1 - (sum_var_items / var_total))
    return round(alpha, 3)

# Analisis tiap pertanyaan
hasil_analisis = []
for col in df.columns:
    if col in PERTANYAAN_LIKERT:
        # Pastikan data adalah numerik dan dalam range 1-5
        if pd.api.types.is_numeric_dtype(df[col]) and df[col].between(1, 5).all():
            hasil = analisis_likert(df[col], col)
            hasil_analisis.append(hasil)
    elif col in PERTANYAAN_ISIAN:
        hasil = analisis_isian(df[col], col)
        hasil_analisis.append(hasil)

# Analisis reliabilitas
alpha = cronbach_alpha(df, PERTANYAAN_POSITIF, PERTANYAAN_NEGATIF)

# Analisis korelasi untuk pertanyaan Likert
likert_cols = [col for col in PERTANYAAN_LIKERT if col in df.columns]
corr_matrix = df[likert_cols].corr() if len(likert_cols) > 1 else pd.DataFrame()

# Simpan hasil untuk visualisasi
output = {
    'metadata': {
        'total_responden': RESPONDEN,
        'reliabilitas': alpha,
        'total_pertanyaan': len(hasil_analisis),
        'likert_map': LIKERT_MAP
    },
    'analisis': hasil_analisis,
    'korelasi': corr_matrix.to_dict() if not corr_matrix.empty else {}
}

# Simpan ke JSON
with open('analisis_kuisioner.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

# Buat visualisasi tambahan
if not corr_matrix.empty:
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt=".2f")
    plt.title('Matriks Korelasi Antar Pertanyaan Likert')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()

print("Analisis selesai. Data disimpan dalam analisis_kuisioner.json dan correlation_matrix.png")