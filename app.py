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


# Evaluasi hasil berdasarkan skor, materi, dan level Bloom

# Hitung benar per materi dan per level
benar_materi = {}
benar_level = {}
total_materi = {}
total_level = {}

for i, row in df.iterrows():
    materi = row.get("materi", "Umum")
    level = row.get("level", "C1")
    jawaban = st.session_state.jawaban_siswa.get(i, "")
    benar = str(jawaban).strip().lower() == str(row["jawaban_benar"]).strip().lower()

    # Hitung total soal per materi & level
    total_materi[materi] = total_materi.get(materi, 0) + 1
    total_level[level] = total_level.get(level, 0) + 1

    # Hitung benar per materi & level
    if benar:
        benar_materi[materi] = benar_materi.get(materi, 0) + 1
        benar_level[level] = benar_level.get(level, 0) + 1

# Evaluasi umum berdasarkan skor total
if nilai >= 80:
    kesimpulan_umum = "Pemahamanmu sangat baik! 🌟"
elif nilai >= 60:
    kesimpulan_umum = "Cukup baik, tapi masih perlu memperdalam beberapa konsep ⚙️"
else:
    kesimpulan_umum = "Perlu belajar lagi, tetap semangat ya! 💪"

# Buat kesimpulan tambahan per materi
kesimpulan_materi = []
for materi, benar in benar_materi.items():
    persen = (benar / total_materi[materi]) * 100
    if persen >= 80:
        kesimpulan_materi.append(f"✅ Sudah menguasai materi **{materi}** ({persen:.0f}%)")
    elif persen >= 50:
        kesimpulan_materi.append(f"⚙️ Cukup pada materi **{materi}** ({persen:.0f}%)")
    else:
        kesimpulan_materi.append(f"❌ Perlu belajar lagi pada materi **{materi}** ({persen:.0f}%)")

# Buat kesimpulan tambahan per level Bloom
kesimpulan_level = []
for level, benar in benar_level.items():
    persen = (benar / total_level[level]) * 100
    if persen >= 80:
        kesimpulan_level.append(f"✅ Sudah baik pada level **{level}** ({persen:.0f}%)")
    elif persen >= 50:
        kesimpulan_level.append(f"⚙️ Cukup pada level **{level}** ({persen:.0f}%)")
    else:
        kesimpulan_level.append(f"❌ Perlu ditingkatkan pada level **{level}** ({persen:.0f}%)")

# Gabungkan semua kesimpulan
st.markdown(f"### 📊 Kesimpulan Umum\n{kesimpulan_umum}")
st.markdown("### 📘 Analisis Berdasarkan Materi")
for teks in kesimpulan_materi:
    st.markdown(f"- {teks}")
st.markdown("### 🎯 Analisis Berdasarkan Level Taksonomi Bloom")
for teks in kesimpulan_level:
    st.markdown(f"- {teks}")

# Simpan kesimpulan utama
kesimpulan = kesimpulan_umum + " | " + "; ".join(kesimpulan_materi + kesimpulan_level)
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
    st.header("👩‍🏫 Halaman Guru")

    # Password guru
    PASSWORD_GURU = "fisika123"  # 🔒 kamu bisa ubah sesuai keinginan

    # Cek apakah guru sudah login
    if "guru_logged_in" not in st.session_state:
        st.session_state.guru_logged_in = False

    # Jika belum login, tampilkan input password
    if not st.session_state.guru_logged_in:
        with st.form("login_guru_form"):
            password_input = st.text_input("Masukkan kata sandi guru:", type="password")
            login_button = st.form_submit_button("🔐 Login")

        if login_button:
            if password_input == PASSWORD_GURU:
                st.session_state.guru_logged_in = True
                st.success("✅ Login berhasil! Mengakses data nilai siswa...")
                st.rerun()
            else:
                st.error("❌ Kata sandi salah. Coba lagi.")

        if st.button("⬅️ Kembali ke Beranda"):
            st.session_state.page = "home"
            st.rerun()

    # Jika sudah login, tampilkan data nilai siswa
    else:
        st.subheader("📊 Rekap Nilai Siswa")

        try:
            data = pd.read_csv(
                "hasil_latihan.csv",
                names=["No","Nama", "Benar", "Total Soal", "Nilai", "Kesimpulan"]
            )
            st.dataframe(data)
        except FileNotFoundError:
            st.warning("⚠️ Belum ada data nilai siswa tersimpan.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Kembali ke Beranda"):
                st.session_state.page = "home"
                st.session_state.guru_logged_in = False
                st.rerun()
        with col2:
            if st.button("🚪 Logout Guru"):
                st.session_state.guru_logged_in = False
                st.success("Anda telah logout.")
                st.rerun()

