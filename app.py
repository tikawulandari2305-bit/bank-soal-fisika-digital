import streamlit as st
import pandas as pd
import os
from io import BytesIO

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
# Fungsi deskripsi level Bloom
def deskripsi_bloom(level):
    mapping = {
        "C1": "Mengingat",
        "C2": "Memahami",
        "C3": "Menerapkan",
        "C4": "Menganalisis",
        "C5": "Menilai",
        "C6": "Mencipta"
    }
    return mapping.get(level, "Tidak diketahui")

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

    # Kesimpulan tambahan
    kesimpulan = f"Perlu meningkatkan kemampuan {deskripsi_bloom(level_bloom)} ({level_bloom})."
    return nilai, kompetensi, kesimpulan

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
        nilai, kompetensi, kesimpulan = evaluasi_bloom(jawaban_siswa, kunci, max(set(level), key=level.count))

        st.success(f"Nilai Anda: {nilai}")
        st.info(f"Kesimpulan: {kesimpulan}")

        # Simpan nilai ke Excel
        os.makedirs("data", exist_ok=True)
        hasil_baru = pd.DataFrame([[username, nilai, kompetensi, kesimpulan]],
                                  columns=["Nama", "Nilai", "Kompetensi", "Kesimpulan"])

        file_path = "data/nilai.xlsx"
        if os.path.exists(file_path):
            hasil_lama = pd.read_excel(file_path)
            hasil = pd.concat([hasil_lama, hasil_baru], ignore_index=True)
        else:
            hasil = hasil_baru

        hasil.to_excel(file_path, index=False)
        st.success("Nilai berhasil disimpan!")

        # Tombol kembali
        if st.button("⬅️ Kembali ke Beranda Siswa"):
            st.session_state.pop("login_siswa", None)
            st.experimental_rerun()

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

        st.session_state["soal_terunggah"] = True
        st.success("✅ Soal berhasil diunggah dan disimpan!")

    # Tampilkan soal yang baru diunggah
    if os.path.exists("data/soal.xlsx"):
        st.subheader("📄 Soal yang sudah diunggah:")
        soal = pd.read_excel("data/soal.xlsx")
        st.dataframe(soal)

    # Rekap nilai siswa
    st.subheader("📊 Rekap Nilai Siswa")
    nilai_path = "data/nilai.xlsx"
    if os.path.exists(nilai_path):
        df = pd.read_excel(nilai_path)
        st.dataframe(df)
        rata = df['Nilai'].mean()
        st.write(f"Rata-rata kelas: **{rata:.2f}**")

        # --- Tombol download rekap nilai ---
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        st.download_button(
            label="📥 Download Rekap Nilai (.xlsx)",
            data=buffer,
            file_name="rekap_nilai_siswa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.info("Belum ada siswa yang mengerjakan soal.")

    # Tombol logout guru
    if st.button("⬅️ Keluar ke Beranda Guru"):
        st.session_state.pop("login_guru", None)
        st.experimental_rerun()

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
