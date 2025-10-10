import streamlit as st
import pandas as pd

st.title("📘 Bank Soal Fisika Digital")
st.write("Selamat datang di aplikasi bank soal fisika interaktif!")

# Input nama pengguna
nama = st.text_input("Masukkan nama kamu:")
nilai = 0

# Input sebagai siswa  
role = st.button("Siswa"):
if role == "Siswa":
    st.header("🧠 Halaman Siswa")
    
    st.write("Silakan jawab soal berikut:")
    soal1 = st.radio("1. Besaran turunan di bawah ini adalah:", 
                     ["Massa", "Waktu", "Gaya", "Suhu"])
    soal2 = st.radio("2. Satuan dari gaya adalah:", 
                     ["Joule", "Newton", "Pascal", "Watt"])
    
    if st.button("Kirim Jawaban"):
        skor = 0
        if soal1 == "Gaya":
            skor += 1
        if soal2 == "Newton":
            skor += 1
        
        st.success(f"Skor kamu: {skor}/2")
st.warning("Jawaban kamu sudah direkam!")

        # Simpan hasil ke file CSV
            hasil = pd.DataFrame({"Nama": [nama], "Skor": [skor]})
            hasil.to_csv("hasil_latihan.csv", mode="a", header=False, index=False)

    
    # Bisa tambahkan latihan lain:
    if st.button("Latihan Soal 2"):
        st.subheader("Latihan 2: Hukum Newton")
        st.write("Contoh latihan berikutnya nanti bisa kamu tambahkan di sini!")

# Input sebagai guru
role = st.button("Guru"):
if role == "Guru":
    st.header("👩‍🏫 Halaman Guru")
    st.write("Berikut data hasil siswa:")
    
