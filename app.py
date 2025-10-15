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
