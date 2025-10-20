import streamlit as st
import pandas as pd
import os
st.set_page_config(page_title="Bank Soal Fisika Digital", page_icon="⚡", layout="centered")

st.markdown(
"""
<h1 style='text-align: center; color: #ffcc00;'>⚡ Bank Soal Fisika Interaktif</h1>
<p style='text-align: center; color: #cccccc;'>Latih pemahaman konsep fisika dan dapatkan evaluasi otomatis 💡</p>
""",
unsafe_allow_html=True
)
try:
df = pd.read_excel("Book1.xlsx") # Pastikan kolom: soal, opsi_a, opsi_b, opsi_c, opsi_d, jawaban_benar, materi, level
st.success("✅ File soal berhasil dimuat!")
except FileNotFoundError:
st.error("❌ File 'Book1.xlsx' tidak ditemukan.")
st.stop()
if "page" not in st.session_state:
st.session_state.page = "home"

if st.session_state.page == "home":
st.markdown("### 👋 Selamat datang di aplikasi latihan soal fisika!")
col1, col2 = st.columns(2)
with col1:
if st.button("🧠 Masuk sebagai Siswa"):
st.session_state.page = "siswa"
st.rerun()
with col2:
if st.button("👩‍🏫 Masuk sebagai Guru"):
st.session_state.page = "guru"
st.rerun()
if st.session_state.page == "siswa":
st.header("🧠 Halaman Siswa")
nama = st.text_input("Masukkan nama kamu:")

if nama and st.button("🚀 Mulai Latihan"):
    st.session_state.mulai = True

if st.session_state.get("mulai", False):
    st.subheader(f"Halo, {nama}! Selamat mengerjakan 🌟")
    st.markdown("---")

    # Pastikan session_state jawaban ada
    if "jawaban_siswa" not in st.session_state:
        st.session_state.jawaban_siswa = {}

    for i, row in df.iterrows():
        st.markdown(f"**{i+1}. {row['soal']}**")
        opsi = [row["opsi_a"], row["opsi_b"], row["opsi_c"], row["opsi_d"]]
        default_idx = opsi.index(st.session_state.jawaban_siswa.get(i)) if st.session_state.jawaban_siswa.get(i) in opsi else 0
        st.session_state.jawaban_siswa[i] = st.radio(f"Pilih jawabanmu untuk soal {i+1}:", opsi, key=f"radio_{i}", index=default_idx)
        st.markdown("<hr>", unsafe_allow_html=True)

    if st.button("✅ Kirim Jawaban"):
        jawaban_siswa = st.session_state.jawaban_siswa
        skor_benar, total_soal = 0, len(df)

        benar_materi, total_materi = {}, {}
        benar_level, total_level = {}, {}

        for i, row in df.iterrows():
            jawaban = jawaban_siswa.get(i, "")
            benar = str(jawaban).strip().lower() == str(row["jawaban_benar"]).strip().lower()
            materi = row.get("materi", "Umum")
            level = row.get("level", "C1")

            total_materi[materi] = total_materi.get(materi, 0) + 1
            total_level[level] = total_level.get(level, 0) + 1

            if benar:
                skor_benar += 1
                benar_materi[materi] = benar_materi.get(materi, 0) + 1
                benar_level[level] = benar_level.get(level, 0) + 1

        nilai = (skor_benar / total_soal) * 100

        # ======== HASIL DAN KESIMPULAN =========
        st.success(f"🎯 Skor kamu: {skor_benar}/{total_soal} ({nilai:.2f}%)")
        st.progress(nilai / 100)

        # Kesimpulan umum
        if nilai >= 80:
            kesimpulan_umum = "Pemahamanmu sangat baik! 🌟"
        elif nilai >= 60:
            kesimpulan_umum = "Cukup baik, tapi masih perlu memperdalam beberapa konsep ⚙️"
        else:
            kesimpulan_umum = "Perlu belajar lagi, tetap semangat ya! 💪"

        st.markdown(f"### 📊 Kesimpulan Umum\n{kesimpulan_umum}")

        # Kesimpulan per materi
        st.markdown("### 📘 Analisis Berdasarkan Materi")
        for materi, total in total_materi.items():
            benar = benar_materi.get(materi, 0)
            persen = (benar / total) * 100
            if persen >= 80:
                st.markdown(f"- ✅ Sudah menguasai **{materi}** ({persen:.0f}%)")
            elif persen >= 50:
                st.markdown(f"- ⚙️ Cukup baik di **{materi}** ({persen:.0f}%)")
            else:
                st.markdown(f"- ❌ Perlu belajar lagi pada **{materi}** ({persen:.0f}%)")

        # Kesimpulan per level
        st.markdown("### 🎯 Analisis Berdasarkan Level Taksonomi Bloom")
        for level, total in total_level.items():
            benar = benar_level.get(level, 0)
            persen = (benar / total) * 100
            if persen >= 80:
                st.markdown(f"- ✅ Sudah baik pada level **{level}** ({persen:.0f}%)")
            elif persen >= 50:
                st.markdown(f"- ⚙️ Cukup pada level **{level}** ({persen:.0f}%)")
            else:
                st.markdown(f"- ❌ Masih lemah pada level **{level}** ({persen:.0f}%)")

        # Simpan hasil ke CSV
        hasil = pd.DataFrame([{
            "Nama": nama,
            "Benar": skor_benar,
            "Total Soal": total_soal,
            "Nilai": nilai,
            "Kesimpulan": kesimpulan_umum
        }])
        hasil.to_csv("hasil_latihan.csv", mode="a", header=not os.path.exists("hasil_latihan.csv"), index=False)
        st.success("📁 Hasilmu sudah disimpan!")

    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.page = "home"
        st.session_state.pop("mulai", None)
        st.session_state.pop("jawaban_siswa", None)
        st.rerun()
