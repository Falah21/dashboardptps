import pandas as pd
import os
import datetime
import streamlit as st
from st_supabase_connection import SupabaseConnection
import psycopg2
from io import StringIO


# =========================================================
# KONFIGURASI TAHUN
# =========================================================
TAHUN_MINIMAL = 2010
TAHUN_MAKSIMAL = datetime.date.today().year + 1


# =========================================================
# MAPPING
# =========================================================
MAPPING_CABANG = {
    "100": "Selatan",
    "200": "Timur",
    "300": "Utara"
}

MAPPING_JENIS = {
    "A": "Air",
    "T": "Tempat",
    "L": "Listrik"
}

KOLOM_DIBUTUHAN = [
    "tglbayar", "tglclosing", "pasar", "alamat",
    "stand", "pedagang", "periode", "nilai"
]

MAPPING_PASAR = {
    "101": "BENDUL MERISI",
    "102": "GAYUNG SARI",
    "103": "WONOKROMO LAMA",
    "104": "DUKUH KUPANG",
    "105": "DUKUH KUPANG BARAT",
    "106": "GENTENG BARU",
    "107": "KARANG PILANG",
    "108": "LAKARSANTRI",
    "109": "BANGKINGAN",
    "110": "HWN KARANG PILANG",
    "111": "KEMBANG",
    "112": "KEDUNGSARI",
    "113": "KEDUNGDORO",
    "114": "KUPANG",
    "115": "PANDEGILING",
    "116": "KUPANG GUNUNG",
    "117": "PAKIS",
    "118": "WONOKITRI",
    "119": "TUNJUNGAN",
    "120": "WONOKROMO",
    "201": "BUNGA BRATANG",
    "202": "BURUNG BRATANG",
    "203": "INPRES BRATANG",
    "204": "KEPUTIH",
    "205": "GUBENG MASJID",
    "206": "GUBENG KERTAJAYA",
    "207": "KAPASAN",
    "208": "ASWOTOMO",
    "209": "KERTOPATEN",
    "210": "KENDANGSARI",
    "211": "TENGGILIS",
    "212": "PANJANGJIWO",
    "213": "KEPUTRAN UTARA",
    "214": "KEPUTRAN SELATAN",
    "215": "DINOYO TANGSI",
    "216": "KAYOON",
    "217": "KRUKAH",
    "218": "PACAR KELING",
    "219": "INDRAKILA INDUK",
    "220": "INDRAKILA DRT",
    "221": "AMBENGAN BATU",
    "222": "JL. KELAPA",
    "223": "SUTOREJO",
    "224": "KALI KEDINDING",
    "225": "PUCANG ANOM",
    "226": "RUNGKUT BARU",
    "227": "TAMBAH REJO",
    "228": "KAPASAN BARU",
    "301": "ASEM ROWO",
    "302": "TIDAR",
    "303": "TEMBOK DUKUH",
    "304": "BABA'AN",
    "305": "KEBALEN BARAT DRT",
    "306": "BALONGSARI",
    "307": "MANUKAN KULON",
    "308": "BANJAR SUGIHAN",
    "309": "BLAURAN BARU",
    "310": "KOBLEN",
    "311": "KEPATIHAN",
    "312": "DUPAK BANDEROJO",
    "313": "DUPAK BANGUNREJO",
    "314": "DUPAK RUKUN",
    "315": "KREMBANGAN",
    "316": "PESAPEN",
    "317": "PESAPEN CIKAR",
    "318": "JL GRESIK",
    "319": "JEMBATAN MERAH",
    "320": "PABEAN",
    "321": "BIBIS",
    "322": "JL. DUKUH",
    "323": "PECINDILAN",
    "324": "KALIANYAR",
    "325": "GEMBONG TEBASAN",
    "326": "GEMBONG TEBASAN DRT",
    "327": "JAGALAN",
    "328": "PEGIRIAN",
    "329": "AMPEL",
    "330": "SUKODONO",
    "331": "SIMO",
    "332": "SIMO GUNUNG",
    "333": "SIMO MULYO",
    "334": "WONOKUSUMO"
}


# =========================================================
# PREPROCESSING
# =========================================================
def preprocess_files(uploaded_files, progress_callback=None):
    data_semua = []
    errors = []
    total = len(uploaded_files)

    for i, file in enumerate(uploaded_files):
        nama_file = file.name
        nama_tanpa_ext = os.path.splitext(nama_file)[0]
        bagian = nama_tanpa_ext.split()

        if len(bagian) < 2:
            errors.append(f"Skip '{nama_file}': format nama tidak valid")
            continue

        kode_cabang = bagian[0]
        kode_jenis = bagian[1]

        if kode_cabang not in MAPPING_CABANG:
            errors.append(f"Skip '{nama_file}': kode cabang '{kode_cabang}' tidak dikenal")
            continue

        if kode_jenis not in MAPPING_JENIS:
            errors.append(f"Skip '{nama_file}': kode jenis '{kode_jenis}' tidak dikenal")
            continue

        cabang = MAPPING_CABANG[kode_cabang]
        jenis_tagihan = MAPPING_JENIS[kode_jenis]

        try:
            df = pd.read_excel(file, dtype={"pasar": "string", "stand": "string"})
        except Exception as e:
            errors.append(f"Gagal baca '{nama_file}': {e}")
            continue

        kolom_hilang = [k for k in KOLOM_DIBUTUHAN if k not in df.columns]
        if kolom_hilang:
            errors.append(f"Skip '{nama_file}': kolom hilang {kolom_hilang}")
            continue

        df = df[KOLOM_DIBUTUHAN].copy()
        df["Kode Cabang"] = kode_cabang
        df["Cabang"] = cabang
        df["Jenis Tagihan"] = jenis_tagihan
        df["Sumber File"] = nama_file

        data_semua.append(df)

        if progress_callback:
            progress_callback((i + 1) / total, nama_file)

    if not data_semua:
        return None, errors

    master = pd.concat(data_semua, ignore_index=True)

    master = master.rename(columns={
        "tglbayar": "Tgl Bayar",
        "tglclosing": "Tgl Closing",
        "pasar": "Pasar",
        "alamat": "Alamat",
        "stand": "Stand",
        "pedagang": "Pedagang",
        "periode": "Periode",
        "nilai": "Nilai"
    })

    master["Tgl Bayar"] = pd.to_datetime(
        master["Tgl Bayar"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
    ).dt.strftime("%d-%m-%Y")

    master["Tgl Closing"] = pd.to_datetime(
        master["Tgl Closing"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
    ).dt.strftime("%d-%m-%Y")

    tgl_dt = pd.to_datetime(master["Tgl Bayar"], format="%d-%m-%Y", errors="coerce")
    master["Tahun"] = tgl_dt.dt.year
    master["Bulan"] = tgl_dt.dt.month
    master["Tahun-Bulan"] = tgl_dt.dt.to_period("M").astype(str)

    master["Nilai"] = pd.to_numeric(master["Nilai"], errors="coerce").fillna(0)
    master["Pasar"] = master["Pasar"].astype(str).str.strip()
    master["Pedagang"] = master["Pedagang"].astype(str).str.strip()
    master["Alamat"] = master["Alamat"].astype(str).str.strip()
    master["Stand"] = master["Stand"].astype(str).str.strip()
    master["Nama Pasar"] = master["Pasar"].map(MAPPING_PASAR).fillna("TIDAK DIKETAHUI")

    # Filter tahun dinamis
    master = master[
        master["Tahun"].between(TAHUN_MINIMAL, TAHUN_MAKSIMAL, inclusive="both")
    ].reset_index(drop=True)

    return master, errors


# =========================================================
# CEK FILE YANG SUDAH ADA DI DATABASE
# =========================================================
def get_existing_files_from_db():
    """
    Ambil daftar 'sumber_file' yang sudah ada di database.
    Return: set of filenames, atau empty set jika gagal.
    """
    try:
        db_url = st.secrets["connections"]["supabase"]["DB_URL"]
        conn = psycopg2.connect(db_url, connect_timeout=30)
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT sumber_file FROM public.tagihan_pasar;")
        files = {row[0] for row in cur.fetchall()}
        cur.close()
        conn.close()
        return files
    except Exception:
        return set()


# =========================================================
# SIMPAN KE SUPABASE VIA COPY (CEPAT!)
# =========================================================
def save_to_supabase_fast(master_df, replace_all=False, progress_callback=None):
    """
    Simpan DataFrame master ke Supabase menggunakan COPY PostgreSQL.
    
    Mode:
        - replace_all=False (default): 
            APPEND. File yang sudah ada di database (berdasarkan 'sumber_file')
            otomatis di-skip. Hanya file baru yang disimpan.
        - replace_all=True: 
            RESET TOTAL. Hapus semua data lama, ganti dengan data baru.
    
    Return: (jumlah_inserted, error_message, info_dict)
    """
    try:
        db_url = st.secrets["connections"]["supabase"]["DB_URL"]
    except Exception:
        return 0, "DB_URL tidak ditemukan di secrets.toml", {}

    # Siapkan DataFrame
    df_db = master_df.copy()

    df_db = df_db.rename(columns={
        "Tgl Bayar":     "tgl_bayar",
        "Tgl Closing":   "tgl_closing",
        "Pasar":         "pasar",
        "Nama Pasar":    "nama_pasar",
        "Alamat":        "alamat",
        "Stand":         "stand",
        "Pedagang":      "pedagang",
        "Periode":       "periode",
        "Nilai":         "nilai",
        "Kode Cabang":   "kode_cabang",
        "Cabang":        "cabang",
        "Jenis Tagihan": "jenis_tagihan",
        "Sumber File":   "sumber_file",
        "Tahun":         "tahun",
        "Bulan":         "bulan",
        "Tahun-Bulan":   "tahun_bulan",
    })

    # Konversi tanggal ke ISO
    df_db["tgl_bayar"] = pd.to_datetime(
        df_db["tgl_bayar"], format="%d-%m-%Y", errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    df_db["tgl_closing"] = pd.to_datetime(
        df_db["tgl_closing"], format="%d-%m-%Y", errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # Konversi tipe numerik
    df_db["tahun"] = pd.to_numeric(df_db["tahun"], errors="coerce").astype("Int64")
    df_db["bulan"] = pd.to_numeric(df_db["bulan"], errors="coerce").astype("Int64")
    df_db["nilai"] = pd.to_numeric(df_db["nilai"], errors="coerce").fillna(0)

    kolom_urut = [
        "tgl_bayar", "tgl_closing", "pasar", "nama_pasar", "alamat",
        "stand", "pedagang", "periode", "nilai",
        "kode_cabang", "cabang", "jenis_tagihan", "sumber_file",
        "tahun", "bulan", "tahun_bulan"
    ]
    df_db = df_db[kolom_urut]
    df_db = df_db.where(pd.notna(df_db), None)

    info = {
        "dilewati": 0,
        "file_baru": [],
        "file_dilewati": [],
    }

    try:
        if progress_callback:
            progress_callback(0.1, "Menghubungkan ke database...")

        conn = psycopg2.connect(db_url, connect_timeout=30)
        conn.autocommit = False
        cur = conn.cursor()

        # ===== MODE RESET TOTAL =====
        if replace_all:
            if progress_callback:
                progress_callback(0.2, "Menghapus data lama...")
            cur.execute("TRUNCATE TABLE public.tagihan_pasar RESTART IDENTITY;")
            info["file_baru"] = sorted(df_db["sumber_file"].unique().tolist())

        # ===== MODE APPEND (default) — CEGAH DUPLIKAT =====
        else:
            if progress_callback:
                progress_callback(0.2, "Mengecek file duplikat di database...")

            # Ambil daftar sumber_file yang sudah ada
            cur.execute("SELECT DISTINCT sumber_file FROM public.tagihan_pasar;")
            file_di_db = {row[0] for row in cur.fetchall()}

            file_batch_baru = sorted(df_db["sumber_file"].unique().tolist())

            if file_di_db:
                file_duplikat = [f for f in file_batch_baru if f in file_di_db]
                file_baru_real = [f for f in file_batch_baru if f not in file_di_db]

                info["file_baru"] = file_baru_real
                info["file_dilewati"] = file_duplikat

                # Buang baris dari file yang sudah ada
                sebelum = len(df_db)
                df_db = df_db[~df_db["sumber_file"].isin(file_di_db)].copy()
                info["dilewati"] = sebelum - len(df_db)

                if info["dilewati"] > 0 and progress_callback:
                    progress_callback(
                        0.3,
                        f"Melewati {info['dilewati']:,} baris dari file duplikat..."
                    )

                if df_db.empty:
                    cur.close()
                    conn.close()
                    return 0, None, info  # Semua duplikat, bukan error
            else:
                info["file_baru"] = file_batch_baru

        # ===== COPY KE DATABASE =====
        if progress_callback:
            progress_callback(0.5, f"Mengirim {len(df_db):,} baris ke database...")

        output = StringIO()
        df_db.to_csv(
            output, index=False, header=False, sep="\t",
            na_rep="\\N", quoting=3, escapechar="\\",
        )
        output.seek(0)

        kolom_str = ", ".join(kolom_urut)
        copy_sql = (
            f"COPY public.tagihan_pasar ({kolom_str}) "
            f"FROM STDIN WITH (FORMAT csv, DELIMITER E'\\t', NULL '\\N', QUOTE E'\\b');"
        )
        cur.copy_expert(copy_sql, output)

        if progress_callback:
            progress_callback(0.9, "Commit transaksi...")

        conn.commit()
        total_inserted = len(df_db)

        cur.close()
        conn.close()

        # Bersihkan cache Streamlit (bukan parquet)
        st.cache_data.clear()

        if progress_callback:
            progress_callback(1.0, "Selesai!")

        return total_inserted, None, info

    except Exception as e:
        try:
            if "conn" in locals():
                conn.rollback()
                conn.close()
        except Exception:
            pass
        return 0, f"Gagal insert ke Supabase via COPY: {e}", info


# =========================================================
# LOAD DARI SUPABASE (LANGSUNG — TANPA CACHE PARQUET)
# =========================================================
@st.cache_data(ttl=600, show_spinner=False)
def load_from_supabase():
    """
    Load data dari Supabase via REST API.
    
    Cache pakai @st.cache_data(ttl=600) → cache 10 menit di memori Streamlit.
    Kalau perlu refresh, panggil st.cache_data.clear().
    """
    conn = st.connection("supabase", type=SupabaseConnection)

    all_data = []
    offset = 0
    limit = 1000

    while True:
        response = (
            conn.table("tagihan_pasar")
            .select("*")
            .order("id")
            .range(offset, offset + limit - 1)
            .execute()
        )
        if not response.data:
            break
        all_data.extend(response.data)
        if len(response.data) < limit:
            break
        offset += limit

    if not all_data:
        return pd.DataFrame()

    df = pd.DataFrame(all_data)

    df = df.rename(columns={
        "tgl_bayar":     "Tgl Bayar",
        "tgl_closing":   "Tgl Closing",
        "pasar":         "Pasar",
        "nama_pasar":    "Nama Pasar",
        "alamat":        "Alamat",
        "stand":         "Stand",
        "pedagang":      "Pedagang",
        "periode":       "Periode",
        "nilai":         "Nilai",
        "kode_cabang":   "Kode Cabang",
        "cabang":        "Cabang",
        "jenis_tagihan": "Jenis Tagihan",
        "sumber_file":   "Sumber File",
        "tahun":         "Tahun",
        "bulan":         "Bulan",
        "tahun_bulan":   "Tahun-Bulan",
    })

    df["Tgl Bayar"] = pd.to_datetime(
        df["Tgl Bayar"], errors="coerce"
    ).dt.strftime("%d-%m-%Y")

    df["Tgl Closing"] = pd.to_datetime(
        df["Tgl Closing"], errors="coerce"
    ).dt.strftime("%d-%m-%Y")

    df["Nilai"] = pd.to_numeric(df["Nilai"], errors="coerce").fillna(0)
    df["Tahun"] = pd.to_numeric(df["Tahun"], errors="coerce").astype("Int64")
    df["Bulan"] = pd.to_numeric(df["Bulan"], errors="coerce").astype("Int64")

    return df


# =========================================================
# ENSURE DATA LOADED
# =========================================================
def ensure_data_loaded():
    """Pastikan session_state['master_df'] terisi."""
    if st.session_state.get("master_df") is not None:
        return st.session_state["master_df"], None

    try:
        df_db = load_from_supabase()
        st.session_state["master_df"] = df_db if not df_db.empty else None
        return st.session_state["master_df"], None
    except Exception as e:
        return None, str(e)
