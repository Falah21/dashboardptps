import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.preprocessing import (
    preprocess_files, save_to_supabase_fast, load_from_supabase
)
from utils.helper import format_angka, format_rupiah

st.set_page_config(page_title="Upload Data", layout="wide")

st.title("Upload & Preprocessing Data")
st.markdown("Upload file Excel mentah dari folder `DATA 2020-2025`.")

st.info("""
**Aturan nama file:**
- Format: `<kode_cabang> <kode_jenis> <nama_file>.xlsx`
- Contoh: `100 A januari 2020.xlsx`, `200 T maret.xlsx`
- Kode cabang: `100`, `200`, `300`
- Kode jenis: `A` (Air), `T` (Tempat), `L` (Listrik)
""")

# =========================================================
# MUAT DARI DATABASE
# =========================================================
st.markdown("### Muat Data dari Database")
st.caption("Klik untuk load data dari Supabase tanpa upload ulang.")

col_load1, col_load2 = st.columns([1, 3])
with col_load1:
    if st.button("Muat dari Supabase", type="secondary", use_container_width=True):
        with st.spinner("Memuat data dari database..."):
            try:
                df_db = load_from_supabase(use_local_cache=False)
                if df_db.empty:
                    st.warning("Database kosong. Silakan upload file terlebih dahulu.")
                else:
                    st.session_state["master_df"] = df_db
                    st.success(f"Berhasil load **{len(df_db):,} baris** dari Supabase!")
                    st.rerun()
            except Exception as e:
                st.error(f"Gagal load dari Supabase: {e}")

st.markdown("---")

# =========================================================
# UPLOAD FILE BARU
# =========================================================
st.markdown("### Upload File Baru")

uploaded_files = st.file_uploader(
    "Pilih file Excel (bisa multiple)",
    type=["xlsx", "xls"],
    accept_multiple_files=True,
    key="uploader"
)

if uploaded_files:
    st.success(f"**{len(uploaded_files)} file** siap diproses.")

    with st.expander("Lihat daftar file yang diupload"):
        for f in uploaded_files:
            st.write(f"• {f.name}")

    replace_all = st.checkbox(
        "Ganti semua data lama di database (recommended)",
        value=True,
        help="Kalau dicentang, semua data lama di tabel akan dihapus dulu sebelum insert. "
             "Kalau tidak dicentang, data akan ditambahkan (bisa dobel)."
    )

    if st.button("Proses & Simpan ke Database", type="primary", use_container_width=True):
        # ===== STEP 1: PREPROCESSING =====
        progress_bar = st.progress(0, text="Memulai preprocessing...")

        def update_progress(pct, nama):
            progress_bar.progress(min(pct, 1.0), text=f"Preprocessing: {nama}")

        master, errors = preprocess_files(uploaded_files, progress_callback=update_progress)
        progress_bar.empty()

        if master is None:
            st.error("Tidak ada data yang berhasil diproses.")
            for err in errors:
                st.warning(err)
            st.stop()

        st.session_state["master_df"] = master
        st.session_state["preprocess_time"] = pd.Timestamp.now()

        st.success(
            f"Preprocessing selesai! Total **{len(master):,} baris** "
            f"dari **{master['Sumber File'].nunique()} file**."
        )

        # ===== STEP 2: SIMPAN KE SUPABASE VIA COPY =====
        st.markdown("### Menyimpan ke Database")
        save_bar = st.progress(0, text="Memulai simpan ke database...")
        status_text = st.empty()

        def update_save_progress(pct, msg):
            save_bar.progress(min(pct, 1.0), text=f"Menyimpan: {int(pct*100)}%")
            status_text.caption(f"⏳ {msg}")

        import time
        t_start = time.time()

        inserted, err_db = save_to_supabase_fast(
            master,
            replace_all=replace_all,
            progress_callback=update_save_progress
        )

        t_elapsed = time.time() - t_start
        save_bar.empty()
        status_text.empty()

        if err_db:
            st.error(f"Gagal simpan ke database: {err_db}")
            st.info("Data tetap tersedia di sesi ini. Cek koneksi Supabase Anda.")
        else:
            st.success(
                f"✅ Berhasil simpan **{inserted:,} baris** ke database "
                f"dalam **{t_elapsed:.1f} detik**!"
            )

        # ===== RINGKASAN =====
        if errors:
            with st.expander(f"{len(errors)} file dilewati — lihat detail"):
                for err in errors:
                    st.warning(err)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Baris", format_angka(len(master)))
        col2.metric("Total Nilai", format_rupiah(master["Nilai"].sum()))
        col3.metric("Jumlah Pasar", format_angka(master["Nama Pasar"].nunique()))
        col4.metric("Jumlah Pedagang", format_angka(master["Pedagang"].nunique()))

        st.markdown("#### Preview Data (10 baris pertama)")
        st.dataframe(master.head(10), use_container_width=True)

        st.info("Silakan buka menu **Dashboard** di sidebar untuk melihat visualisasi.")

elif "master_df" in st.session_state and st.session_state["master_df"] is not None:
    st.success("Data sudah ada di sesi ini.")
    df = st.session_state["master_df"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Baris", format_angka(len(df)))
    col2.metric("Total Nilai", format_rupiah(df["Nilai"].sum()))
    col3.metric("Jumlah File", df["Sumber File"].nunique())

    st.dataframe(df.head(10), use_container_width=True)

    if st.button("Hapus Data dari Sesi"):
        st.session_state["master_df"] = None
        st.rerun()
