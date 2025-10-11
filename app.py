import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bank Soal Fisika", page_icon="⚡", layout="centered")

st.title("⚡ Bank Soal Fisika Interaktif")

# ===============================
# MEMBACA DATA SOAL DARI EXCEL
# ===============================
try:
    df = pd.read_excel("data/Book1.xlsx")

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
            st.write(f"**{i+1}. {row['Pertanyaan']}**")
            pilihan = st.radio(
                "Pilih jawabanmu:",
                [row["Opsi_A"], row["Opsi_B"], row["Opsi_C"], row["Opsi_D"]],
                key=f"soal_{i}"
            )
            jawaban_siswa.append(pilihan)

        if st.button("Kirim Jawaban"):
            hasil = []
            for i, row in df.iterrows():
                benar = row["Jawaban_Benar"]
                pembahasan = row["Pembahasan"]
                if jawaban_siswa[i] == benar:
                    skor += 1
                    hasil.append({"No": i+1, "Status": "✅ Benar", "Pembahasan": pembahasan})
                else:
                    hasil.append({"No": i+1, "Status": f"❌ Salah (Jawaban benar: {benar})", "Pembahasan": pembahasan})

            st.success(f"Skor kamu: {skor} / {len(df)}")
            st.subheader("📘 Pembahasan:")
            st.table(pd.DataFrame(hasil))

            # Simpan hasil ke file CSV
            hasil_simpan = pd.DataFrame({"Nama": [nama], "Skor": [skor]})
            hasil_simpan.to_csv("hasil_latihan.csv", mode="a", header=False, index=False)

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
