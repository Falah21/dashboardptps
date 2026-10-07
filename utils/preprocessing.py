# # import pandas as pd
# # import os
# # import streamlit as st
# # from st_supabase_connection import SupabaseConnection

# # MAPPING_CABANG = {
# #     "100": "Selatan",
# #     "200": "Timur",
# #     "300": "Utara"
# # }

# # MAPPING_JENIS = {
# #     "A": "Air",
# #     "T": "Tempat",
# #     "L": "Listrik"
# # }

# # KOLOM_DIBUTUHAN = [
# #     "tglbayar", "tglclosing", "pasar", "alamat",
# #     "stand", "pedagang", "periode", "nilai"
# # ]

# # MAPPING_PASAR = {
# #     "101": "BENDUL MERISI",
# #     "102": "GAYUNG SARI",
# #     "103": "WONOKROMO LAMA",
# #     "104": "DUKUH KUPANG",
# #     "105": "DUKUH KUPANG BARAT",
# #     "106": "GENTENG BARU",
# #     "107": "KARANG PILANG",
# #     "108": "LAKARSANTRI",
# #     "109": "BANGKINGAN",
# #     "110": "HWN KARANG PILANG",
# #     "111": "KEMBANG",
# #     "112": "KEDUNGSARI",
# #     "113": "KEDUNGDORO",
# #     "114": "KUPANG",
# #     "115": "PANDEGILING",
# #     "116": "KUPANG GUNUNG",
# #     "117": "PAKIS",
# #     "118": "WONOKITRI",
# #     "119": "TUNJUNGAN",
# #     "120": "WONOKROMO",
# #     "201": "BUNGA BRATANG",
# #     "202": "BURUNG BRATANG",
# #     "203": "INPRES BRATANG",
# #     "204": "KEPUTIH",
# #     "205": "GUBENG MASJID",
# #     "206": "GUBENG KERTAJAYA",
# #     "207": "KAPASAN",
# #     "208": "ASWOTOMO",
# #     "209": "KERTOPATEN",
# #     "210": "KENDANGSARI",
# #     "211": "TENGGILIS",
# #     "212": "PANJANGJIWO",
# #     "213": "KEPUTRAN UTARA",
# #     "214": "KEPUTRAN SELATAN",
# #     "215": "DINOYO TANGSI",
# #     "216": "KAYOON",
# #     "217": "KRUKAH",
# #     "218": "PACAR KELING",
# #     "219": "INDRAKILA INDUK",
# #     "220": "INDRAKILA DRT",
# #     "221": "AMBENGAN BATU",
# #     "222": "JL. KELAPA",
# #     "223": "SUTOREJO",
# #     "224": "KALI KEDINDING",
# #     "225": "PUCANG ANOM",
# #     "226": "RUNGKUT BARU",
# #     "227": "TAMBAH REJO",
# #     "228": "KAPASAN BARU",
# #     "301": "ASEM ROWO",
# #     "302": "TIDAR",
# #     "303": "TEMBOK DUKUH",
# #     "304": "BABA'AN",
# #     "305": "KEBALEN BARAT DRT",
# #     "306": "BALONGSARI",
# #     "307": "MANUKAN KULON",
# #     "308": "BANJAR SUGIHAN",
# #     "309": "BLAURAN BARU",
# #     "310": "KOBLEN",
# #     "311": "KEPATIHAN",
# #     "312": "DUPAK BANDEROJO",
# #     "313": "DUPAK BANGUNREJO",
# #     "314": "DUPAK RUKUN",
# #     "315": "KREMBANGAN",
# #     "316": "PESAPEN",
# #     "317": "PESAPEN CIKAR",
# #     "318": "JL GRESIK",
# #     "319": "JEMBATAN MERAH",
# #     "320": "PABEAN",
# #     "321": "BIBIS",
# #     "322": "JL. DUKUH",
# #     "323": "PECINDILAN",
# #     "324": "KALIANYAR",
# #     "325": "GEMBONG TEBASAN",
# #     "326": "GEMBONG TEBASAN DRT",
# #     "327": "JAGALAN",
# #     "328": "PEGIRIAN",
# #     "329": "AMPEL",
# #     "330": "SUKODONO",
# #     "331": "SIMO",
# #     "332": "SIMO GUNUNG",
# #     "333": "SIMO MULYO",
# #     "334": "WONOKUSUMO"
# # }


# # def preprocess_files(uploaded_files, progress_callback=None):
# #     """Sama seperti sebelumnya — tidak diubah."""
# #     data_semua = []
# #     errors = []
# #     total = len(uploaded_files)

# #     for i, file in enumerate(uploaded_files):
# #         nama_file = file.name
# #         nama_tanpa_ext = os.path.splitext(nama_file)[0]
# #         bagian = nama_tanpa_ext.split()

# #         if len(bagian) < 2:
# #             errors.append(f"Skip '{nama_file}': format nama tidak valid")
# #             continue

# #         kode_cabang = bagian[0]
# #         kode_jenis = bagian[1]

# #         if kode_cabang not in MAPPING_CABANG:
# #             errors.append(f"Skip '{nama_file}': kode cabang '{kode_cabang}' tidak dikenal")
# #             continue

# #         if kode_jenis not in MAPPING_JENIS:
# #             errors.append(f"Skip '{nama_file}': kode jenis '{kode_jenis}' tidak dikenal")
# #             continue

# #         cabang = MAPPING_CABANG[kode_cabang]
# #         jenis_tagihan = MAPPING_JENIS[kode_jenis]

# #         try:
# #             df = pd.read_excel(file, dtype={"pasar": "string", "stand": "string"})
# #         except Exception as e:
# #             errors.append(f"Gagal baca '{nama_file}': {e}")
# #             continue

# #         kolom_hilang = [k for k in KOLOM_DIBUTUHAN if k not in df.columns]
# #         if kolom_hilang:
# #             errors.append(f"Skip '{nama_file}': kolom hilang {kolom_hilang}")
# #             continue

# #         df = df[KOLOM_DIBUTUHAN].copy()
# #         df["Kode Cabang"] = kode_cabang
# #         df["Cabang"] = cabang
# #         df["Jenis Tagihan"] = jenis_tagihan
# #         df["Sumber File"] = nama_file

# #         data_semua.append(df)

# #         if progress_callback:
# #             progress_callback((i + 1) / total, nama_file)

# #     if not data_semua:
# #         return None, errors

# #     master = pd.concat(data_semua, ignore_index=True)

# #     master = master.rename(columns={
# #         "tglbayar": "Tgl Bayar",
# #         "tglclosing": "Tgl Closing",
# #         "pasar": "Pasar",
# #         "alamat": "Alamat",
# #         "stand": "Stand",
# #         "pedagang": "Pedagang",
# #         "periode": "Periode",
# #         "nilai": "Nilai"
# #     })

# #     master["Tgl Bayar"] = pd.to_datetime(
# #         master["Tgl Bayar"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
# #     ).dt.strftime("%d-%m-%Y")

# #     master["Tgl Closing"] = pd.to_datetime(
# #         master["Tgl Closing"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
# #     ).dt.strftime("%d-%m-%Y")

# #     tgl_dt = pd.to_datetime(master["Tgl Bayar"], format="%d-%m-%Y", errors="coerce")
# #     master["Tahun"] = tgl_dt.dt.year
# #     master["Bulan"] = tgl_dt.dt.month
# #     master["Tahun-Bulan"] = tgl_dt.dt.to_period("M").astype(str)

# #     master["Nilai"] = pd.to_numeric(master["Nilai"], errors="coerce").fillna(0)
# #     master["Pasar"] = master["Pasar"].astype(str).str.strip()
# #     master["Pedagang"] = master["Pedagang"].astype(str).str.strip()
# #     master["Alamat"] = master["Alamat"].astype(str).str.strip()
# #     master["Stand"] = master["Stand"].astype(str).str.strip()
# #     master["Nama Pasar"] = master["Pasar"].map(MAPPING_PASAR).fillna("TIDAK DIKETAHUI")

# #     master = master[master["Tahun"].between(2020, 2025, inclusive="both")].reset_index(drop=True)

# #     return master, errors


# # # =========================================================
# # # FUNGSI BARU: Simpan & Load dari Supabase
# # # =========================================================

# # def save_to_supabase(master_df, replace_all=True):
# #     """
# #     Simpan DataFrame master ke Supabase.
    
# #     Args:
# #         master_df: DataFrame hasil preprocessing
# #         replace_all: kalau True, hapus semua data lama dulu (biar tidak dobel)
    
# #     Returns:
# #         (jumlah_inserted, error_message)
# #     """
# #     try:
# #         conn = st.connection("supabase", type=SupabaseConnection)
# #     except Exception as e:
# #         return 0, f"Gagal koneksi ke Supabase: {e}"

# #     df_db = master_df.copy()

# #     # Rename kolom ke snake_case
# #     df_db = df_db.rename(columns={
# #         "Tgl Bayar":     "tgl_bayar",
# #         "Tgl Closing":   "tgl_closing",
# #         "Pasar":         "pasar",
# #         "Nama Pasar":    "nama_pasar",
# #         "Alamat":        "alamat",
# #         "Stand":         "stand",
# #         "Pedagang":      "pedagang",
# #         "Periode":       "periode",
# #         "Nilai":         "nilai",
# #         "Kode Cabang":   "kode_cabang",
# #         "Cabang":        "cabang",
# #         "Jenis Tagihan": "jenis_tagihan",
# #         "Sumber File":   "sumber_file",
# #         "Tahun":         "tahun",
# #         "Bulan":         "bulan",
# #         "Tahun-Bulan":   "tahun_bulan",
# #     })

# #     # Konversi tanggal dd-mm-yyyy -> yyyy-mm-dd (Postgres butuh format ISO)
# #     df_db["tgl_bayar"] = pd.to_datetime(
# #         df_db["tgl_bayar"], format="%d-%m-%Y", errors="coerce"
# #     ).dt.strftime("%Y-%m-%d")

# #     df_db["tgl_closing"] = pd.to_datetime(
# #         df_db["tgl_closing"], format="%d-%m-%Y", errors="coerce"
# #     ).dt.strftime("%Y-%m-%d")

# #     # Konversi tipe
# #     df_db["tahun"] = df_db["tahun"].astype("Int64")
# #     df_db["bulan"] = df_db["bulan"].astype("Int64")
# #     df_db["nilai"] = pd.to_numeric(df_db["nilai"], errors="coerce").fillna(0)

# #     # Ganti NaN dengan None biar Postgres bisa terima
# #     df_db = df_db.where(pd.notna(df_db), None)

# #     # Buang kolom yang tidak perlu
# #     kolom_buang = ["Tgl Bayar_dt"] if "Tgl Bayar_dt" in df_db.columns else []
# #     if kolom_buang:
# #         df_db = df_db.drop(columns=kolom_buang)

# #     records = df_db.to_dict(orient="records")

# #     try:
# #         # Hapus semua data lama (replace total)
# #         if replace_all:
# #             conn.table("tagihan_pasar").delete().neq("id", 0).execute()

# #         # Insert per chunk (Supabase limit ~1000 per request)
# #         CHUNK_SIZE = 500
# #         total_inserted = 0

# #         for i in range(0, len(records), CHUNK_SIZE):
# #             chunk = records[i:i + CHUNK_SIZE]
# #             conn.table("tagihan_pasar").insert(chunk).execute()
# #             total_inserted += len(chunk)

# #         return total_inserted, None

# #     except Exception as e:
# #         return 0, f"Gagal insert ke Supabase: {e}"


# # @st.cache_data(ttl=600, show_spinner=False)
# # def load_from_supabase():
# #     """
# #     Load semua data dari tabel tagihan_pasar di Supabase.
# #     Return DataFrame dengan format kolom seperti master.
# #     """
# #     conn = st.connection("supabase", type=SupabaseConnection)

# #     all_data = []
# #     offset = 0
# #     limit = 1000  # Supabase default max 1000 baris per request

# #     while True:
# #         response = (
# #             conn.table("tagihan_pasar")
# #             .select("*")
# #             .order("id")
# #             .range(offset, offset + limit - 1)
# #             .execute()
# #         )
# #         if not response.data:
# #             break
# #         all_data.extend(response.data)
# #         if len(response.data) < limit:
# #             break
# #         offset += limit

# #     if not all_data:
# #         return pd.DataFrame()

# #     df = pd.DataFrame(all_data)

# #     # Rename balik ke format rapi untuk dashboard
# #     df = df.rename(columns={
# #         "tgl_bayar":     "Tgl Bayar",
# #         "tgl_closing":   "Tgl Closing",
# #         "pasar":         "Pasar",
# #         "nama_pasar":    "Nama Pasar",
# #         "alamat":        "Alamat",
# #         "stand":         "Stand",
# #         "pedagang":      "Pedagang",
# #         "periode":       "Periode",
# #         "nilai":         "Nilai",
# #         "kode_cabang":   "Kode Cabang",
# #         "cabang":        "Cabang",
# #         "jenis_tagihan": "Jenis Tagihan",
# #         "sumber_file":   "Sumber File",
# #         "tahun":         "Tahun",
# #         "bulan":         "Bulan",
# #         "tahun_bulan":   "Tahun-Bulan",
# #     })

# #     # Konversi tanggal dari yyyy-mm-dd ke dd-mm-yyyy
# #     df["Tgl Bayar"] = pd.to_datetime(
# #         df["Tgl Bayar"], errors="coerce"
# #     ).dt.strftime("%d-%m-%Y")

# #     df["Tgl Closing"] = pd.to_datetime(
# #         df["Tgl Closing"], errors="coerce"
# #     ).dt.strftime("%d-%m-%Y")

# #     # Pastikan tipe data benar
# #     df["Nilai"] = pd.to_numeric(df["Nilai"], errors="coerce").fillna(0)
# #     df["Tahun"] = pd.to_numeric(df["Tahun"], errors="coerce").astype("Int64")
# #     df["Bulan"] = pd.to_numeric(df["Bulan"], errors="coerce").astype("Int64")

# #     return df

# import pandas as pd
# import os
# import streamlit as st
# from st_supabase_connection import SupabaseConnection


# # =========================================================
# # MAPPING
# # =========================================================
# MAPPING_CABANG = {
#     "100": "Selatan",
#     "200": "Timur",
#     "300": "Utara"
# }

# MAPPING_JENIS = {
#     "A": "Air",
#     "T": "Tempat",
#     "L": "Listrik"
# }

# KOLOM_DIBUTUHAN = [
#     "tglbayar", "tglclosing", "pasar", "alamat",
#     "stand", "pedagang", "periode", "nilai"
# ]

# MAPPING_PASAR = {
#     "101": "BENDUL MERISI",
#     "102": "GAYUNG SARI",
#     "103": "WONOKROMO LAMA",
#     "104": "DUKUH KUPANG",
#     "105": "DUKUH KUPANG BARAT",
#     "106": "GENTENG BARU",
#     "107": "KARANG PILANG",
#     "108": "LAKARSANTRI",
#     "109": "BANGKINGAN",
#     "110": "HWN KARANG PILANG",
#     "111": "KEMBANG",
#     "112": "KEDUNGSARI",
#     "113": "KEDUNGDORO",
#     "114": "KUPANG",
#     "115": "PANDEGILING",
#     "116": "KUPANG GUNUNG",
#     "117": "PAKIS",
#     "118": "WONOKITRI",
#     "119": "TUNJUNGAN",
#     "120": "WONOKROMO",
#     "201": "BUNGA BRATANG",
#     "202": "BURUNG BRATANG",
#     "203": "INPRES BRATANG",
#     "204": "KEPUTIH",
#     "205": "GUBENG MASJID",
#     "206": "GUBENG KERTAJAYA",
#     "207": "KAPASAN",
#     "208": "ASWOTOMO",
#     "209": "KERTOPATEN",
#     "210": "KENDANGSARI",
#     "211": "TENGGILIS",
#     "212": "PANJANGJIWO",
#     "213": "KEPUTRAN UTARA",
#     "214": "KEPUTRAN SELATAN",
#     "215": "DINOYO TANGSI",
#     "216": "KAYOON",
#     "217": "KRUKAH",
#     "218": "PACAR KELING",
#     "219": "INDRAKILA INDUK",
#     "220": "INDRAKILA DRT",
#     "221": "AMBENGAN BATU",
#     "222": "JL. KELAPA",
#     "223": "SUTOREJO",
#     "224": "KALI KEDINDING",
#     "225": "PUCANG ANOM",
#     "226": "RUNGKUT BARU",
#     "227": "TAMBAH REJO",
#     "228": "KAPASAN BARU",
#     "301": "ASEM ROWO",
#     "302": "TIDAR",
#     "303": "TEMBOK DUKUH",
#     "304": "BABA'AN",
#     "305": "KEBALEN BARAT DRT",
#     "306": "BALONGSARI",
#     "307": "MANUKAN KULON",
#     "308": "BANJAR SUGIHAN",
#     "309": "BLAURAN BARU",
#     "310": "KOBLEN",
#     "311": "KEPATIHAN",
#     "312": "DUPAK BANDEROJO",
#     "313": "DUPAK BANGUNREJO",
#     "314": "DUPAK RUKUN",
#     "315": "KREMBANGAN",
#     "316": "PESAPEN",
#     "317": "PESAPEN CIKAR",
#     "318": "JL GRESIK",
#     "319": "JEMBATAN MERAH",
#     "320": "PABEAN",
#     "321": "BIBIS",
#     "322": "JL. DUKUH",
#     "323": "PECINDILAN",
#     "324": "KALIANYAR",
#     "325": "GEMBONG TEBASAN",
#     "326": "GEMBONG TEBASAN DRT",
#     "327": "JAGALAN",
#     "328": "PEGIRIAN",
#     "329": "AMPEL",
#     "330": "SUKODONO",
#     "331": "SIMO",
#     "332": "SIMO GUNUNG",
#     "333": "SIMO MULYO",
#     "334": "WONOKUSUMO"
# }


# # =========================================================
# # PREPROCESSING
# # =========================================================
# def preprocess_files(uploaded_files, progress_callback=None):
#     data_semua = []
#     errors = []
#     total = len(uploaded_files)

#     for i, file in enumerate(uploaded_files):
#         nama_file = file.name
#         nama_tanpa_ext = os.path.splitext(nama_file)[0]
#         bagian = nama_tanpa_ext.split()

#         if len(bagian) < 2:
#             errors.append(f"Skip '{nama_file}': format nama tidak valid")
#             continue

#         kode_cabang = bagian[0]
#         kode_jenis = bagian[1]

#         if kode_cabang not in MAPPING_CABANG:
#             errors.append(f"Skip '{nama_file}': kode cabang '{kode_cabang}' tidak dikenal")
#             continue

#         if kode_jenis not in MAPPING_JENIS:
#             errors.append(f"Skip '{nama_file}': kode jenis '{kode_jenis}' tidak dikenal")
#             continue

#         cabang = MAPPING_CABANG[kode_cabang]
#         jenis_tagihan = MAPPING_JENIS[kode_jenis]

#         try:
#             df = pd.read_excel(file, dtype={"pasar": "string", "stand": "string"})
#         except Exception as e:
#             errors.append(f"Gagal baca '{nama_file}': {e}")
#             continue

#         kolom_hilang = [k for k in KOLOM_DIBUTUHAN if k not in df.columns]
#         if kolom_hilang:
#             errors.append(f"Skip '{nama_file}': kolom hilang {kolom_hilang}")
#             continue

#         df = df[KOLOM_DIBUTUHAN].copy()
#         df["Kode Cabang"] = kode_cabang
#         df["Cabang"] = cabang
#         df["Jenis Tagihan"] = jenis_tagihan
#         df["Sumber File"] = nama_file

#         data_semua.append(df)

#         if progress_callback:
#             progress_callback((i + 1) / total, nama_file)

#     if not data_semua:
#         return None, errors

#     master = pd.concat(data_semua, ignore_index=True)

#     master = master.rename(columns={
#         "tglbayar": "Tgl Bayar",
#         "tglclosing": "Tgl Closing",
#         "pasar": "Pasar",
#         "alamat": "Alamat",
#         "stand": "Stand",
#         "pedagang": "Pedagang",
#         "periode": "Periode",
#         "nilai": "Nilai"
#     })

#     master["Tgl Bayar"] = pd.to_datetime(
#         master["Tgl Bayar"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
#     ).dt.strftime("%d-%m-%Y")

#     master["Tgl Closing"] = pd.to_datetime(
#         master["Tgl Closing"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
#     ).dt.strftime("%d-%m-%Y")

#     tgl_dt = pd.to_datetime(master["Tgl Bayar"], format="%d-%m-%Y", errors="coerce")
#     master["Tahun"] = tgl_dt.dt.year
#     master["Bulan"] = tgl_dt.dt.month
#     master["Tahun-Bulan"] = tgl_dt.dt.to_period("M").astype(str)

#     master["Nilai"] = pd.to_numeric(master["Nilai"], errors="coerce").fillna(0)
#     master["Pasar"] = master["Pasar"].astype(str).str.strip()
#     master["Pedagang"] = master["Pedagang"].astype(str).str.strip()
#     master["Alamat"] = master["Alamat"].astype(str).str.strip()
#     master["Stand"] = master["Stand"].astype(str).str.strip()
#     master["Nama Pasar"] = master["Pasar"].map(MAPPING_PASAR).fillna("TIDAK DIKETAHUI")

#     master = master[
#         master["Tahun"].between(2020, 2025, inclusive="both")
#     ].reset_index(drop=True)

#     return master, errors


# # =========================================================
# # SIMPAN KE SUPABASE
# # =========================================================
# def save_to_supabase(master_df, replace_all=True):
#     """
#     Simpan DataFrame master ke Supabase.
#     Return: (jumlah_inserted, error_message)
#     """
#     try:
#         conn = st.connection("supabase", type=SupabaseConnection)
#     except Exception as e:
#         return 0, f"Gagal koneksi ke Supabase: {e}"

#     df_db = master_df.copy()

#     df_db = df_db.rename(columns={
#         "Tgl Bayar":     "tgl_bayar",
#         "Tgl Closing":   "tgl_closing",
#         "Pasar":         "pasar",
#         "Nama Pasar":    "nama_pasar",
#         "Alamat":        "alamat",
#         "Stand":         "stand",
#         "Pedagang":      "pedagang",
#         "Periode":       "periode",
#         "Nilai":         "nilai",
#         "Kode Cabang":   "kode_cabang",
#         "Cabang":        "cabang",
#         "Jenis Tagihan": "jenis_tagihan",
#         "Sumber File":   "sumber_file",
#         "Tahun":         "tahun",
#         "Bulan":         "bulan",
#         "Tahun-Bulan":   "tahun_bulan",
#     })

#     df_db["tgl_bayar"] = pd.to_datetime(
#         df_db["tgl_bayar"], format="%d-%m-%Y", errors="coerce"
#     ).dt.strftime("%Y-%m-%d")

#     df_db["tgl_closing"] = pd.to_datetime(
#         df_db["tgl_closing"], format="%d-%m-%Y", errors="coerce"
#     ).dt.strftime("%Y-%m-%d")

#     df_db["tahun"] = df_db["tahun"].astype("Int64")
#     df_db["bulan"] = df_db["bulan"].astype("Int64")
#     df_db["nilai"] = pd.to_numeric(df_db["nilai"], errors="coerce").fillna(0)

#     df_db = df_db.where(pd.notna(df_db), None)

#     kolom_buang = ["Tgl Bayar_dt"] if "Tgl Bayar_dt" in df_db.columns else []
#     if kolom_buang:
#         df_db = df_db.drop(columns=kolom_buang)

#     records = df_db.to_dict(orient="records")

#     try:
#         if replace_all:
#             conn.table("tagihan_pasar").delete().neq("id", 0).execute()

#         CHUNK_SIZE = 500
#         total_inserted = 0

#         for i in range(0, len(records), CHUNK_SIZE):
#             chunk = records[i:i + CHUNK_SIZE]
#             conn.table("tagihan_pasar").insert(chunk).execute()
#             total_inserted += len(chunk)

#         # Hapus cache parquet biar data baru langsung kelihatan
#         try:
#             if os.path.exists("data/master_cache.parquet"):
#                 os.remove("data/master_cache.parquet")
#         except Exception:
#             pass

#         # Bersihkan cache Streamlit
#         st.cache_data.clear()

#         return total_inserted, None

#     except Exception as e:
#         return 0, f"Gagal insert ke Supabase: {e}"


# # =========================================================
# # LOAD DARI SUPABASE (dengan cache parquet lokal)
# # =========================================================
# @st.cache_data(ttl=600, show_spinner=False)
# def load_from_supabase(use_local_cache=True):
#     """
#     Load data dari Supabase dengan cache parquet lokal.
#     Cache parquet berlaku 10 menit — kalau lebih lama, query ulang ke Supabase.
#     """
#     CACHE_PATH = "data/master_cache.parquet"

#     # Cek cache parquet lokal
#     if use_local_cache and os.path.exists(CACHE_PATH):
#         try:
#             cache_age = pd.Timestamp.now().timestamp() - os.path.getmtime(CACHE_PATH)
#             if cache_age < 600:  # 10 menit
#                 df = pd.read_parquet(CACHE_PATH)
#                 return df
#         except Exception:
#             pass

#     # Query dari Supabase
#     conn = st.connection("supabase", type=SupabaseConnection)

#     all_data = []
#     offset = 0
#     limit = 1000

#     while True:
#         response = (
#             conn.table("tagihan_pasar")
#             .select("*")
#             .order("id")
#             .range(offset, offset + limit - 1)
#             .execute()
#         )
#         if not response.data:
#             break
#         all_data.extend(response.data)
#         if len(response.data) < limit:
#             break
#         offset += limit

#     if not all_data:
#         return pd.DataFrame()

#     df = pd.DataFrame(all_data)

#     df = df.rename(columns={
#         "tgl_bayar":     "Tgl Bayar",
#         "tgl_closing":   "Tgl Closing",
#         "pasar":         "Pasar",
#         "nama_pasar":    "Nama Pasar",
#         "alamat":        "Alamat",
#         "stand":         "Stand",
#         "pedagang":      "Pedagang",
#         "periode":       "Periode",
#         "nilai":         "Nilai",
#         "kode_cabang":   "Kode Cabang",
#         "cabang":        "Cabang",
#         "jenis_tagihan": "Jenis Tagihan",
#         "sumber_file":   "Sumber File",
#         "tahun":         "Tahun",
#         "bulan":         "Bulan",
#         "tahun_bulan":   "Tahun-Bulan",
#     })

#     df["Tgl Bayar"] = pd.to_datetime(
#         df["Tgl Bayar"], errors="coerce"
#     ).dt.strftime("%d-%m-%Y")

#     df["Tgl Closing"] = pd.to_datetime(
#         df["Tgl Closing"], errors="coerce"
#     ).dt.strftime("%d-%m-%Y")

#     df["Nilai"] = pd.to_numeric(df["Nilai"], errors="coerce").fillna(0)
#     df["Tahun"] = pd.to_numeric(df["Tahun"], errors="coerce").astype("Int64")
#     df["Bulan"] = pd.to_numeric(df["Bulan"], errors="coerce").astype("Int64")

#     # Simpan ke cache parquet lokal
#     try:
#         os.makedirs("data", exist_ok=True)
#         df.to_parquet(CACHE_PATH, index=False)
#     except Exception:
#         pass

#     return df


# # =========================================================
# # ENSURE DATA LOADED — dipanggil di setiap halaman
# # =========================================================
# def ensure_data_loaded():
#     """
#     Pastikan session_state['master_df'] terisi.
#     Kalau kosong, coba load dari Supabase.
    
#     Return: (df, error_message)
#     """
#     # Kalau sudah ada di session, langsung pakai
#     if st.session_state.get("master_df") is not None:
#         return st.session_state["master_df"], None

#     # Coba load dari Supabase
#     try:
#         df_db = load_from_supabase()
#         st.session_state["master_df"] = df_db if not df_db.empty else None
#         return st.session_state["master_df"], None
#     except Exception as e:
#         return None, str(e)

import pandas as pd
import os
import streamlit as st
from st_supabase_connection import SupabaseConnection
import psycopg2
from io import StringIO


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
# PREPROCESSING (tidak berubah)
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

    master = master[
        master["Tahun"].between(2020, 2025, inclusive="both")
    ].reset_index(drop=True)

    return master, errors


# =========================================================
# ⭐ SIMPAN KE SUPABASE VIA COPY (CEPAT!)
# =========================================================
def save_to_supabase_fast(master_df, replace_all=True, progress_callback=None):
    """
    Simpan DataFrame master ke Supabase menggunakan COPY PostgreSQL.
    Jauh lebih cepat daripada insert via REST API.
    
    Return: (jumlah_inserted, error_message)
    """
    # Ambil connection string dari secrets
    try:
        db_url = st.secrets["connections"]["supabase"]["DB_URL"]
    except Exception:
        return 0, "DB_URL tidak ditemukan di secrets.toml"

    # Siapkan DataFrame — rename & konversi tipe
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

    # Konversi tanggal ke format ISO
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

    # Urutan kolom HARUS SAMA dengan urutan kolom di tabel Supabase (kecuali id & created_at)
    kolom_urut = [
        "tgl_bayar", "tgl_closing", "pasar", "nama_pasar", "alamat",
        "stand", "pedagang", "periode", "nilai",
        "kode_cabang", "cabang", "jenis_tagihan", "sumber_file",
        "tahun", "bulan", "tahun_bulan"
    ]
    df_db = df_db[kolom_urut]

    # Ganti NaN dengan None biar jadi \N di CSV
    df_db = df_db.where(pd.notna(df_db), None)

    try:
        if progress_callback:
            progress_callback(0.1, "Menghubungkan ke database...")

        # Koneksi ke PostgreSQL
        conn = psycopg2.connect(db_url, connect_timeout=30)
        conn.autocommit = False
        cur = conn.cursor()

        if progress_callback:
            progress_callback(0.2, "Menyiapkan tabel...")

        # Hapus data lama kalau replace_all
        if replace_all:
            cur.execute("TRUNCATE TABLE public.tagihan_pasar RESTART IDENTITY;")

        if progress_callback:
            progress_callback(0.4, "Mengirim data ke database...")

        # Konversi DataFrame ke TSV di memori
        output = StringIO()
        df_db.to_csv(
            output,
            index=False,
            header=False,
            sep="\t",
            na_rep="\\N",
            quoting=3,  # QUOTE_NONE — biar tidak ada quote yang bikin error
            escapechar="\\",
        )
        output.seek(0)

        # COPY FROM STDIN — ini yang bikin cepat
        kolom_str = ", ".join(kolom_urut)
        copy_sql = f"COPY public.tagihan_pasar ({kolom_str}) FROM STDIN WITH (FORMAT csv, DELIMITER E'\\t', NULL '\\N', QUOTE E'\\b');"
        cur.copy_expert(copy_sql, output)

        if progress_callback:
            progress_callback(0.8, "Commit transaksi...")

        conn.commit()

        # Hitung total
        total_inserted = len(df_db)

        cur.close()
        conn.close()

        # Bersihkan cache parquet lokal
        try:
            if os.path.exists("data/master_cache.parquet"):
                os.remove("data/master_cache.parquet")
        except Exception:
            pass

        # Bersihkan cache Streamlit
        st.cache_data.clear()

        if progress_callback:
            progress_callback(1.0, "Selesai!")

        return total_inserted, None

    except Exception as e:
        try:
            if "conn" in locals():
                conn.rollback()
                conn.close()
        except Exception:
            pass
        return 0, f"Gagal insert ke Supabase via COPY: {e}"


# Alias supaya kode lama tetap kompatibel
def save_to_supabase(master_df, replace_all=True, progress_callback=None):
    """Wrapper ke versi cepat."""
    return save_to_supabase_fast(master_df, replace_all, progress_callback)


# =========================================================
# LOAD DARI SUPABASE (dengan cache parquet lokal)
# =========================================================
@st.cache_data(ttl=600, show_spinner=False)
def load_from_supabase(use_local_cache=True):
    """
    Load data dari Supabase dengan cache parquet lokal.
    Cache parquet berlaku 10 menit — kalau lebih lama, query ulang.
    """
    CACHE_PATH = "data/master_cache.parquet"

    # Cek cache parquet lokal
    if use_local_cache and os.path.exists(CACHE_PATH):
        try:
            cache_age = pd.Timestamp.now().timestamp() - os.path.getmtime(CACHE_PATH)
            if cache_age < 600:
                df = pd.read_parquet(CACHE_PATH)
                return df
        except Exception:
            pass

    # Query dari Supabase via REST API
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

    # Simpan ke cache parquet lokal
    try:
        os.makedirs("data", exist_ok=True)
        df.to_parquet(CACHE_PATH, index=False)
    except Exception:
        pass

    return df


# =========================================================
# ENSURE DATA LOADED
# =========================================================
def ensure_data_loaded():
    """
    Pastikan session_state['master_df'] terisi.
    Return: (df, error_message)
    """
    if st.session_state.get("master_df") is not None:
        return st.session_state["master_df"], None

    try:
        df_db = load_from_supabase()
        st.session_state["master_df"] = df_db if not df_db.empty else None
        return st.session_state["master_df"], None
    except Exception as e:
        return None, str(e)