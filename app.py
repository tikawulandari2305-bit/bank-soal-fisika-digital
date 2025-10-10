import streamlit as st

st.title("📘 Bank Soal Fisika Digital")
st.write("Selamat datang di aplikasi bank soal fisika interaktif!")

# Input nama pengguna
nama = st.text_input("Masukkan nama kamu:")
nilai = 0

# Input sebagai siswa atau guru 
role = st.button("Siswa")

# Soal 1
st.subheader("Soal 1")
st.write("Sebuah benda bermassa 2 kg bergerak dengan percepatan 3 m/s². Berapa gaya yang bekerja padanya?")
jawaban1 = st.number_input("Jawaban (dalam Newton):", min_value=0)
if st.button("Cek Jawaban Soal 1"):
    if jawaban1 == 6:
        st.success("Benar! 💪")
        nilai += 10
    else:
        st.error("Salah 😅 Jawaban yang benar adalah 6 N")

# Hasil akhir
if st.button("Tampilkan Nilai Akhir"):
    st.write(f"Nilai akhir {nama} adalah: {nilai}")
