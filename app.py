import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bank Soal Fisika", page_icon="⚡", layout="centered")

st.title("⚡ Bank Soal Fisika Interaktif")

# ===============================
# MEMBACA DATA SOAL DARI EXCEL
# ===============================
try:
    df = pd.read_excel("Book1.xlsx")

    # Kolom wajib dalam file Excel:
    # 'Pertanyaan', 'Opsi_A', 'Opsi_B', 'Opsi_C', 'Opsi_D', 'Jawaban_Benar', 'Pembahasan'
except FileNotFoundError:
    st.error("❌ File soal_fisika.xlsx belum ditemukan. Pastikan file sudah diunggah ke GitHub.")
    st.stop()

# ===============================
# HALAMAN UTAMA
# ===============================
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.subheader("Silakan pilih peran:")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧠 Siswa"):
            st.session_state.page = "siswa"
            st.rerun()
    with col2:
        if st.button("👩‍🏫 Guru"):
            st.session_state.page = "guru"
            st.rerun()

# ===============================
# HALAMAN SISWA
# ===============================
if st.session_state.page == "siswa":
    st.header("🧠 Halaman Siswa")

    nama = st.text_input("Masukkan nama kamu:")

    if st.button("Mulai Latihan"):
        jawaban_siswa = []
        skor = 0

        for i, row in df.iterrows():
            st.write(f"**{i+1}. {row['soal']}**")
    
    # Buat daftar pilihan dari data Excel
for i, row in df.iterrows():
    st.write(f"**{i+1}. {row['soal']}**")
    pilihan = st.radio("Pilih jawabanmu:", ["A", "B", "C", "D"])
    jawaban_siswa.append(pilihan)
    
    if st.button("Kirim Jawaban"):
# Analisis setiap siswa
        hasil = []
        for idx, row in jawaban.iterrows():
            nama = row["nama"]
            skor_total = 0
            total_soal = len(soal_list)

# Catatan untuk per materi dan per level
    benar_materi = {}
    benar_level = {}

    for q in soal_list:
        benar = str(row[q]).strip().lower() == str(kunci[q]).strip().lower()
        if benar:
            skor_total += 1

# Ambil info dari bank soal
        materi = bank.loc[bank["id"] == q, "materi"].values[0]
        level = bank.loc[bank["id"] == q, "level_bloom"].values[0]

# Hitung benar per materi
        benar_materi[materi] = benar_materi.get(materi, 0) + (1 if benar else 0)
        benar_level[level] = benar_level.get(level, 0) + (1 if benar else 0)

# Buat nilai total
    nilai = (skor_total / total_soal) * 100 
    for i, row in df.iterrows():
         benar = row["jawaban_Benar"]
                
# Buat kesimpulan otomatis
    kesimpulan = []
# Evaluasi per materi
    for materi in bank["materi"].unique():
        jumlah_soal = len(bank[bank["materi"] == materi])
        benar = benar_materi.get(materi, 0)
        if benar < jumlah_soal / 2:
            kesimpulan.append(f"Lemah di materi {materi}")
        else:
            kesimpulan.append(f"Sudah menguasai materi {materi}")
# Evaluasi per level Bloom
    for level in bank["level_bloom"].unique():
        jumlah_level = len(bank[bank["level_bloom"] == level])
        benar = benar_level.get(level, 0)
        if benar < jumlah_level / 2:
            kesimpulan.append(f"Perlu meningkatkan kemampuan {level} ({'mengingat' if level=='C1' else 'memahami'})")
        else:
            kesimpulan.append(f"Sudah baik pada level {level}")
    hasil.append({
        "nama": nama,
        "skor_benar": skor_total,
        "total_soal": total_soal,
        "nilai": nilai,
        "kesimpulan": "; ".join(kesimpulan)
    })

# Simpan hasil ke Excel
hasil_df = pd.DataFrame(hasil)
hasil_df.to_excel("hasil_nilai_dengan_kesimpulan.xlsx", index=False)

print(hasil_df)
       

    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.page = "home"
        st.rerun()

# ===============================
# HALAMAN GURU
# ===============================
if st.session_state.page == "guru":
    st.header("👩‍🏫 Hasil Latihan Siswa")

    try:
        data = pd.read_csv("hasil_latihan.csv", names=["Nama", "Skor"])
        st.dataframe(data)
    except FileNotFoundError:
        st.warning("Belum ada data nilai siswa tersimpan.")

    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.page = "home"
        st.rerun()
