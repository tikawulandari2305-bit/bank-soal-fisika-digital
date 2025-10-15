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
            st.session_state["mulai"] = True

    # Jika latihan sudah dimulai
    if st.session_state.get("mulai", False):
        st.subheader(f"Halo, {nama}! Selamat mengerjakan 🌟")
        st.markdown("---")

        # Siapkan session_state untuk jawaban
        if "jawaban_siswa" not in st.session_state:
            st.session_state.jawaban_siswa = {}

        # Tampilkan soal satu per satu
        for i, row in df.iterrows():
            st.markdown(f"**{i+1}. {row['soal']}**")
            opsi = [row["opsi_a"], row["opsi_b"], row["opsi_c"], row["opsi_d"]]

            # Gunakan session_state agar pilihan tidak hilang
            st.session_state.jawaban_siswa[i] = st.radio(
                f"Pilih jawabanmu untuk soal {i+1}:",
                opsi,
                key=f"radio_{i}",
                index=opsi.index(st.session_state.jawaban_siswa[i])
                if i in st.session_state.jawaban_siswa and st.session_state.jawaban_siswa[i] in opsi
                else 0
            )

            st.markdown("<hr>", unsafe_allow_html=True)

        # Tombol kirim jawaban
        if st.button("✅ Kirim Jawaban"):
            jawaban_siswa = st.session_state.jawaban_siswa
            skor_benar = 0
            total_soal = len(df)

            for i, row in df.iterrows():
                jawaban = jawaban_siswa.get(i, "")
                benar = str(jawaban).strip().lower() == str(row["jawaban_benar"]).strip().lower()
                if benar:
                    skor_benar += 1

            nilai = (skor_benar / total_soal) * 100

            st.success(f"🎯 Skor kamu: {skor_benar}/{total_soal} ({nilai:.2f})")
            st.progress(nilai / 100)

            # Evaluasi hasil
            if nilai >= 80:
                kesimpulan = "Pemahamanmu sangat baik! 🌟"
            elif nilai >= 60:
                kesimpulan = "Cukup baik, tapi masih perlu memperdalam beberapa konsep ⚙️"
            else:
                kesimpulan = "Perlu belajar lagi, tetap semangat ya! 💪"

            st.markdown(f"**Kesimpulan:** {kesimpulan}")

            hasil_df = pd.DataFrame([
                {"Nama": nama, "Benar": skor_benar, "Total Soal": total_soal, "Nilai": nilai}
            ])
            st.dataframe(hasil_df)

            # Simpan hasil ke CSV
            hasil_df.to_csv("hasil_latihan.csv", mode="a", header=False, index=False)

            st.download_button(
                label="💾 Unduh Hasil (CSV)",
                data=hasil_df.to_csv(index=False).encode("utf-8"),
                file_name=f"hasil_{nama}.csv",
                mime="text/csv"
            )

        # Tombol kembali
        if st.button("⬅️ Kembali ke Beranda"):
            st.session_state.page = "home"
            st.session_state.pop("mulai", None)
            st.session_state.pop("jawaban_siswa", None)
            st.rerun()
# -----------------------------
# HALAMAN GURU
# -----------------------------
if st.session_state.page == "guru":
    st.header("👩‍🏫 Rekap Nilai Siswa")

    try:
        data = pd.read_csv("hasil_latihan.csv", names=["Nama", "Benar", "Total Soal", "Nilai", "Kesimpulan"])
        st.dataframe(data)
    except FileNotFoundError:
        st.warning("Belum ada data nilai siswa tersimpan.")

    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.page = "home"
        st.rerun()
