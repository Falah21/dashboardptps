import streamlit as st
import pandas as pd
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.preprocessing import (
    preprocess_files, save_to_supabase_fast, load_from_supabase,
    get_existing_files_from_db
)
from utils.helper import format_angka, format_rupiah

st.set_page_config(page_title="Upload Data", layout="wide")

st.title("Upload & Preprocessing Data")
st.markdown("Upload file Excel mentah dari folder `DATA 2010-sekarang`.")

st.info("""
**Aturan nama file:**
- Format: `<kode_cabang> <kode_jenis> <nama_file>.xlsx`
- Contoh: `100 A januari 2020.xlsx`, `200 T maret.xlsx`
- Kode cabang: `100`, `200`, `300`
- Kode jenis: `A` (Air), `T` (Tempat), `L` (Listrik)
""")

# =========================================================
# INFO DATA SAAT INI
# =========================================================
try:
    df_cek = load_from_supabase()
    if not df_cek.empty:
        tahun_ada = sorted(df_cek["Tahun"].dropna().unique().tolist())
        st.success(
            f"**Data di database:** {format_angka(len(df_cek))} baris | "
            f"{df_cek['Sumber File'].nunique()} file | "
            f"Tahun: {tahun_ada[0]}–{tahun_ada[-1]}"
        )
    else:
        st.info("Database masih kosong. Silakan upload file pertama Anda.")
except Exception:
    st.warning("Tidak dapat memuat info data dari database.")

st.markdown("---")

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
                st.cache_data.clear()
                df_db = load_from_supabase()
                if df_db.empty:
                    st.warning("Database kosong.")
                else:
                    st.session_state["master_df"] = df_db
                    st.success(f"Berhasil load **{len(df_db):,} baris**!")
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
    # ===== CEK DUPLIKAT DENGAN DATABASE =====
    daftar_nama = [f.name for f in uploaded_files]

    with st.spinner("Mengecek duplikat dengan database..."):
        file_di_db = get_existing_files_from_db()

    duplikat = [f for f in daftar_nama if f in file_di_db]
    file_baru = [f for f in daftar_nama if f not in file_di_db]

    # Info file baru
    if file_baru:
        st.success(f"**{len(file_baru)} file baru** siap diupload:")
        with st.expander(f"Lihat {len(file_baru)} file baru", expanded=False):
            for f in file_baru:
                st.write(f"• {f}")

    # Info file duplikat
    if duplikat:
        st.warning(
            f"**{len(duplikat)} file sudah ada di database** — akan otomatis di-skip:"
        )
        with st.expander(f"Lihat {len(duplikat)} file duplikat", expanded=True):
            for f in duplikat:
                st.write(f"• ~~{f}~~ (sudah ada)")

    # Kalau semua duplikat
    if not file_baru and duplikat:
        st.error(
            "Semua file yang Anda upload sudah ada di database. "
            "Tidak ada yang perlu disimpan. "
            "Kalau ingin replace, gunakan mode **Reset Total** di bawah."
        )

    st.markdown("---")

    # ===== MODE SIMPAN =====
    st.markdown("#### Mode Simpan")
    mode = st.radio(
        "Pilih mode:",
        options=[
            "Tambah data baru (recommended)",
            "Reset total (HAPUS semua data lama)"
        ],
        index=0,
        help=(
            "**Tambah data baru**: file yang sudah ada di database otomatis di-skip. "
            "Hanya file baru yang disimpan.\n\n"
            "**Reset total**: SEMUA data lama dihapus, diganti dengan data dari file yang diupload."
        )
    )

    replace_all = (mode == "Reset total (HAPUS semua data lama)")

    if replace_all:
        st.warning(
            "**PERINGATAN:** Anda memilih RESET TOTAL. "
            "Semua data lama akan DIHAPUS. Tidak bisa dibatalkan!"
        )

    # ===== TOMBOL PROSES =====
    tombol_disabled = (not file_baru and not replace_all)

    if st.button(
        "Proses & Simpan ke Database",
        type="primary",
        use_container_width=True,
        disabled=tombol_disabled
    ):
        # ===== STEP 1: PREPROCESSING =====
        progress_bar = st.progress(0, text="Memulai preprocessing...")

        def update_progress(pct, nama):
            progress_bar.progress(min(pct, 1.0), text=f"Preprocessing: {nama}")

        master, errors = preprocess_files(uploaded_files, progress_callback=update_progress)
        progress_bar.empty()

        if master is None or master.empty:
            st.error("Tidak ada data yang berhasil diproses.")
            for err in errors:
                st.warning(err)
            st.stop()

        tahun_proses = sorted(master["Tahun"].dropna().unique().tolist())
        st.info(f"Tahun yang diproses: **{', '.join(map(str, tahun_proses))}**")

        st.session_state["master_df"] = master

        st.success(
            f"Preprocessing selesai! Total **{len(master):,} baris** "
            f"dari **{master['Sumber File'].nunique()} file**."
        )

        # ===== STEP 2: SIMPAN KE DATABASE =====
        st.markdown("### Menyimpan ke Database")
        save_bar = st.progress(0, text="Memulai simpan...")
        status_text = st.empty()

        def update_save_progress(pct, msg):
            save_bar.progress(min(pct, 1.0), text=f"Menyimpan: {int(pct*100)}%")
            status_text.caption(f"⏳ {msg}")

        t_start = time.time()
        inserted, err_db, info = save_to_supabase_fast(
            master,
            replace_all=replace_all,
            progress_callback=update_save_progress
        )
        t_elapsed = time.time() - t_start

        save_bar.empty()
        status_text.empty()

        # ===== HASIL =====
        if err_db:
            st.error(f"Gagal simpan: {err_db}")

        elif inserted == 0:
            st.warning("Tidak ada data baru yang ditambahkan.")
            if info.get("file_dilewati"):
                with st.expander(f"Lihat {len(info['file_dilewati'])} file yang dilewati"):
                    for f in info["file_dilewati"]:
                        st.write(f"• {f}")

        else:
            st.success(
                f"Berhasil simpan **{inserted:,} baris** "
                f"dalam **{t_elapsed:.1f} detik**!"
            )

            if info.get("file_baru"):
                with st.expander(f"{len(info['file_baru'])} file berhasil disimpan"):
                    for f in info["file_baru"]:
                        st.write(f"• {f}")

            if info.get("file_dilewati"):
                st.info(
                    f"{len(info['file_dilewati'])} file dilewati (duplikat) — "
                    f"{info['dilewati']:,} baris tidak disimpan."
                )
                with st.expander(f"Lihat {len(info['file_dilewati'])} file duplikat"):
                    for f in info["file_dilewati"]:
                        st.write(f"• {f}")

        if errors:
            with st.expander(f"{len(errors)} file gagal diproses"):
                for err in errors:
                    st.warning(err)

        # Ringkasan
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Baris", format_angka(len(master)))
        col2.metric("Total Nilai", format_rupiah(master["Nilai"].sum()))
        col3.metric("Jumlah Pasar", format_angka(master["Nama Pasar"].nunique()))
        col4.metric("Jumlah Pedagang", format_angka(master["Pedagang"].nunique()))

        st.info("Buka menu **Dashboard** di sidebar untuk melihat visualisasi.")

elif "master_df" in st.session_state and st.session_state["master_df"] is not None:
    st.success("Data sudah ada di sesi ini.")
    df = st.session_state["master_df"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Baris", format_angka(len(df)))
    col2.metric("Total Nilai", format_rupiah(df["Nilai"].sum()))
    col3.metric("Jumlah File", df["Sumber File"].nunique())

    st.dataframe(df.head(10), use_container_width=True)
