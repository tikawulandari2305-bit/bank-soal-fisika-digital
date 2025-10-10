import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bank Soal Fisika", page_icon="🎓", layout="centered")

# Judul utama
st.title("🎓 Bank Soal Fisika Digital")

st.write("Silakan pilih peran kamu untuk melanjutkan:")

# Gunakan session_state untuk menyimpan pilihan halaman
if "page" not in st.session_state:
    st.session_state.page = "home"

# ===============================
# HALAMAN UTAMA (HOME)
# ===============================
if st.session_state.page == "home":
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Masuk sebagai Siswa"):
            st.session_state.page = "siswa"
            st.experimental_rerun()
    with col2:
        if st.button("👩‍🏫 Masuk sebagai Guru"):
            st.session_state.page = "guru"
            st.experimental_rerun()

# ===============================
# HALAMAN SISWA
# ===============================
if st.session_state.page == "siswa":
    st.header("🧠 Halaman Siswa")
    nama = st.text_input("Masukkan nama kamu:")

    if st.button("Mulai Latihan Soal"):
        st.subheader("Latihan 1: Besaran dan Satuan")
        soal1 = st.radio("1. Satuan dari gaya adalah ...", 
                         ["Joule", "Newton", "Watt", "Coulomb"])
        soal2 = st.radio("2. Besaran pokok berikut ini adalah ...", 
                         ["Gaya", "Massa", "Usaha", "Tekanan"])
        soal3 = st.radio("3. Satuan dari energi adalah ...", 
                         ["Newton", "Pascal", "Joule", "Watt"])

        if st.button("Kirim Jawaban"):
            skor = 0
            if soal1 == "Newton": skor += 1
            if soal2 == "Massa": skor += 1
            if soal3 == "Joule": skor += 1

            st.success(f"Skor kamu: {skor}/3")
            st.info("Terima kasih sudah mengerjakan latihan ini! 🌟")

            hasil = pd.DataFrame({"Nama": [nama], "Skor": [skor]})
            hasil.to_csv("hasil_latihan.csv", mode="a", header=False, index=False)

    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.page = "home"
        st.experimental_rerun()

# ===============================
# HALAMAN GURU
# ===============================
if st.session_state.page == "guru":
    st.header("👩‍🏫 Halaman Guru")
    st.write("Berikut hasil latihan siswa:")

    try:
        data = pd.read_csv("hasil_latihan.csv", names=["Nama", "Skor"])
        st.dataframe(data)
    except FileNotFoundError:
        st.warning("Belum ada siswa yang mengerjakan latihan.")

    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.page = "home"
        st.experimental_rerun()
