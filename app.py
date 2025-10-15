import streamlit as st
import pandas as pd

# -----------------------------
# KONFIGURASI HALAMAN
# -----------------------------
st.set_page_config(page_title="Bank Soal Fisika Digital", page_icon="⚡", layout="centered")

st.markdown(
    """
    <h1 style='text-align: center; color: #ffcc00;'>⚡ Bank Soal Fisika Interaktif</h1>
    <p style='text-align: center; color: #cccccc;'>Latih pemahaman konsep fisika dan dapatkan evaluasi otomatis 💡</p>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# MEMBACA FILE EXCEL
# -----------------------------
try:
    df = pd.read_excel("Book1.xlsx")  # pastikan nama kolom di Excel benar
    st.success("✅ File soal berhasil dimuat!")
except FileNotFoundError:
    st.error("❌ File 'Book1.xlsx' tidak ditemukan. Pastikan file sudah diunggah ke GitHub.")
    st.stop()

# -----------------------------
# HALAMAN UTAMA (HOME)
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.markdown("### 👋 Selamat datang di aplikasi latihan soal fisika!")
    st.markdown("Pilih peranmu di bawah ini untuk memulai:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Siswa"):
            st.session_state.page = "siswa"
            st.rerun()
    with col2:
        if st.button("👩‍🏫 Guru"):
            st.session_state.page = "guru"
            st.rerun()
# -----------------------------
# HALAMAN SISWA
# -----------------------------
if st.session_state.page == "siswa":
    st.header("🧠 Halaman Siswa")

    nama = st.text_input("Masukkan nama kamu:")

    if nama:
        st.info("Klik tombol di bawah untuk memulai latihan 👇")
        if st.button("🚀 Mulai Latihan Soal"):
            jawaban_siswa = []
            skor_benar = 0

            st.markdown("---")
            for i, row in df.iterrows():
                st.markdown(f"**{i+1}. {row['soal']}**")
                opsi = [row["opsi_a"], row["opsi_b"], row["opsi_c"], row["opsi_d"]]
                pilihan = st.radio("Pilih jawabanmu:", opsi, key=f"soal_{i}")
                jawaban_siswa.append({
                    "soal": row["soal"],
                    "jawaban": pilihan,
                    "benar": row["jawaban_benar"]
                })
                st.markdown("<hr>", unsafe_allow_html=True)

            if st.button("✅ Kirim Jawaban"):
                total_soal = len(jawaban_siswa)
                for j in jawaban_siswa:
                    if str(j["jawaban"]).strip().lower() == str(j["benar"]).strip().lower():
                        skor_benar += 1

                nilai = (skor_benar / total_soal) * 100

                st.success(f"🎯 Skor kamu: {skor_benar}/{total_soal} ({nilai:.2f})")
                st.progress(nilai / 100)

                # Evaluasi sederhana
                if nilai >= 80:
                    kesimpulan = "Pemahamanmu sangat baik! 🌟"
                elif nilai >= 60:
                    kesimpulan = "Cukup baik, tapi masih perlu memperdalam beberapa konsep ⚙️"
                else:
                    kesimpulan = "Perlu belajar lagi, tetap semangat ya! 💪"

                st.markdown(f"**Kesimpulan:** {kesimpulan}")

                # Tampilkan tabel hasil
                hasil_df = pd.DataFrame(jawaban_siswa)
                st.dataframe(hasil_df)

                # Simpan hasil (opsional)
                hasil = pd.DataFrame([{
                    "Nama": nama,
                    "Benar": skor_benar,
                    "Total Soal": total_soal,
                    "Nilai": nilai,
                    "Kesimpulan": kesimpulan
                }])
                hasil.to_csv("hasil_latihan.csv", mode="a", header=False, index=False)

                st.download_button(
                    label="💾 Unduh Hasil (CSV)",
                    data=hasil.to_csv(index=False).encode("utf-8"),
                    file_name=f"hasil_{nama}.csv",
                    mime="text/csv"
                )

    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.page = "home"
        st.rerun()
