import streamlit as st
import pandas as pd
import os

# --------------------------------------------------
# Konfigurasi halaman
st.set_page_config(page_title="Sistem Penilaian Taksonomi Bloom", layout="wide")
st.title("📘 Sistem Penilaian Taksonomi Bloom")

# --------------------------------------------------
# Fungsi login sederhana
def login(role):
    username = st.text_input(f"Masukkan username {role}")
    password = st.text_input("Masukkan password", type="password")
    login_button = st.button("Masuk")

    if login_button:
        if role == "Guru" and username == "guru" and password == "123":
            st.session_state["login_guru"] = True
            st.success("Login Guru berhasil!")
        elif role == "Siswa" and username != "" and password == "123":
            st.session_state["login_siswa"] = username
            st.success(f"Selamat datang, {username}!")
        else:
            st.error("Username atau password salah!")

# --------------------------------------------------
# Fungsi baca soal
def baca_soal():
    if os.path.exists("data/soal.xlsx"):
        return pd.read_excel("data/soal.xlsx")
    else:
        return None

# --------------------------------------------------
# Fungsi evaluasi nilai & taksonomi Bloom
def evaluasi_bloom(jawaban_siswa, kunci_jawaban, level_bloom):
    benar = sum([1 for i in range(len(jawaban_siswa)) if jawaban_siswa[i] == kunci_jawaban[i]])
    total = len(kunci_jawaban)
    nilai = round((benar / total) * 100, 2)

    # Tentukan kompetensi berdasarkan Bloom
    if nilai >= 85:
        kompetensi = f"Tingkat Analisis ({level_bloom})"
    elif nilai >= 70:
        kompetensi = f"Tingkat Penerapan ({level_bloom})"
    elif nilai >= 55:
        kompetensi = f"Tingkat Pemahaman ({level_bloom})"
    else:
        kompetensi = f"Tingkat Pengetahuan Dasar ({level_bloom})"
    return nilai, kompetensi

# --------------------------------------------------
# Halaman Siswa
def halaman_siswa(username):
    st.header(f"📘 Halaman Siswa ({username})")

    soal_df = baca_soal()
    if soal_df is None:
        st.warning("Belum ada soal yang diunggah guru.")
        return

    jawaban_siswa = []
    for i, row in soal_df.iterrows():
        st.subheader(f"Soal {i+1}")
        st.write(row['soal'])
        opsi = [row['opsi_a'], row['opsi_b'], row['opsi_c'], row['opsi_d']]
        jawaban = st.radio("Pilih jawaban Anda:", opsi, key=f"soal_{i}")
        jawaban_siswa.append(jawaban)

    if st.button("Kirim Jawaban"):
        kunci = list(soal_df['kunci'])
        level = list(soal_df['level_bloom'])
        nilai, kompetensi = evaluasi_bloom(jawaban_siswa, kunci, max(set(level), key=level.count))

        st.success(f"Nilai Anda: {nilai}")
        st.info(f"Kesimpulan: Kompetensi Anda berada pada {kompetensi}")

        # Simpan nilai ke Excel
        os.makedirs("data", exist_ok=True)
        hasil = pd.DataFrame([[username, nilai, kompetensi]], columns=["Nama", "Nilai", "Kompetensi"])
        if os.path.exists("data/nilai.xlsx"):
            hasil_lama = pd.read_csv("data/nilai.xlsx")
            hasil = pd.concat([hasil_lama, hasil], ignore_index=True)
        hasil.to_csv("data/nilai.csv", index=False)
        st.success("Nilai berhasil disimpan!")

# --------------------------------------------------
# Halaman Guru
def halaman_guru():
    st.header("🧑‍🏫 Halaman Guru")

    # Upload soal
    st.subheader("Upload Soal dalam format Excel")
    st.markdown("Kolom wajib: `soal`, `opsi_a`, `opsi_b`, `opsi_c`, `opsi_d`, `kunci`, `level_bloom`")

    file = st.file_uploader("Upload file Excel (.xlsx)", type=["xlsx"])

    if file is not None:
        os.makedirs("data", exist_ok=True)
        file_path = os.path.join("data", "soal.xlsx")

        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        # Simpan status agar tidak reload ke awal
        st.session_state["soal_terunggah"] = True
        st.success("✅ Soal berhasil diunggah!")

    # Tampilkan soal yang baru diunggah
    if "soal_terunggah" in st.session_state and os.path.exists("data/soal.xlsx"):
        st.subheader("📄 Soal yang sudah diunggah:")
        soal = pd.read_excel("data/soal.xlsx")
        st.dataframe(soal)

    # Rekap nilai siswa
    st.subheader("📊 Rekap Nilai Siswa")
    if os.path.exists("data/nilai.xlsx"):
        df = pd.read_xlsx("data/nilai.xlsx")
        st.dataframe(df)
        rata = df['Nilai'].mean()
        st.write(f"Rata-rata kelas: **{rata:.2f}**")
    else:
        st.info("Belum ada siswa yang mengerjakan soal.")

# --------------------------------------------------
# Tampilan utama (sidebar)
st.sidebar.title("🔐 Pilih Peran")
role = st.sidebar.selectbox("Masuk sebagai:", ["Pilih...", "Guru", "Siswa"])

if role == "Guru":
    if "login_guru" not in st.session_state:
        login("Guru")
    elif st.session_state["login_guru"]:
        halaman_guru()

elif role == "Siswa":
    if "login_siswa" not in st.session_state:
        login("Siswa")
    elif st.session_state["login_siswa"]:
        halaman_siswa(st.session_state["login_siswa"])

else:
    st.info("Silakan pilih peran Anda di sidebar.")
