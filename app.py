# # import streamlit as st
# # import os
# # import pandas as pd
# # import sys

# # sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# # from utils.preprocessing import load_from_supabase

# # st.set_page_config(
# #     page_title="Dashboard Data Pasar 2020-2025",
# #     layout="wide",
# #     initial_sidebar_state="expanded"
# # )

# # # =========================================================
# # # AUTO-LOAD DARI SUPABASE
# # # Kalau session_state kosong, coba load dari Supabase
# # # =========================================================
# # if st.session_state.get("master_df") is None:
# #     try:
# #         with st.spinner("Memuat data dari database..."):
# #             df_db = load_from_supabase()
# #             if not df_db.empty:
# #                 st.session_state["master_df"] = df_db
# #             else:
# #                 st.session_state["master_df"] = None
# #     except Exception as e:
# #         st.session_state["master_df"] = None
# #         st.session_state["load_error"] = str(e)

# # st.title("Dashboard Data Pasar Tahun 2020 - 2025")
# # st.markdown("---")

# # st.markdown("""
# # ### Selamat Datang!

# # Aplikasi ini digunakan untuk menganalisis data tagihan pasar tahun **2020 - 2025**.

# # ### Cara Menggunakan:

# # 1. **Upload Data** — Buka menu *Upload Data* di sidebar untuk upload file Excel mentah
# # 2. **Preprocessing** — Sistem akan otomatis menggabungkan dan membersihkan data
# # 3. **Simpan ke Database** — Data akan otomatis tersimpan di Supabase
# # 4. **Dashboard** — Buka menu *Dashboard* untuk melihat visualisasi & filter

# # Data yang sudah pernah diupload **tidak perlu diupload ulang** — otomatis dimuat dari database.
# # """)

# # # =========================================================
# # # STATUS DATA
# # # =========================================================
# # if st.session_state.get("master_df") is not None:
# #     df = st.session_state["master_df"]
# #     st.success(
# #         f"Data siap! Total **{len(df):,} baris** dari "
# #         f"**{df['Nama Pasar'].nunique()} pasar** dan "
# #         f"**{df['Pedagang'].nunique():,} pedagang**."
# #     )
# #     st.info("Buka menu **Dashboard** di sidebar kiri untuk melihat visualisasi.")

# #     # Preview singkat
# #     with st.expander("Preview data (10 baris pertama)"):
# #         st.dataframe(df.head(10), use_container_width=True)

# # elif "load_error" in st.session_state:
# #     st.error(f"Gagal memuat data dari database: {st.session_state['load_error']}")
# #     st.info("Silakan buka menu **Upload Data** untuk upload manual.")

# # else:
# #     st.warning("Belum ada data di database.")
# #     st.info("Buka menu **Upload Data** di sidebar untuk upload file Excel pertama kali.")

# import streamlit as st
# import os
# import pandas as pd
# import sys

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# from utils.preprocessing import ensure_data_loaded

# st.set_page_config(
#     page_title="Dashboard Data Pasar 2020-2025",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # =========================================================
# # AUTO-LOAD DARI SUPABASE
# # =========================================================
# if st.session_state.get("master_df") is None:
#     with st.spinner("Memuat data dari database..."):
#         df_loaded, err = ensure_data_loaded()

#     if err:
#         st.session_state["load_error"] = err

# st.title("Dashboard Data Pasar Tahun 2020 - 2025")
# st.markdown("---")

# st.markdown("""
# ### Selamat Datang!

# Aplikasi ini digunakan untuk menganalisis data tagihan pasar tahun **2020 - 2025**.

# ### Cara Menggunakan:

# 1. **Upload Data** — Buka menu *Upload Data* di sidebar untuk upload file Excel mentah
# 2. **Preprocessing** — Sistem akan otomatis menggabungkan dan membersihkan data
# 3. **Simpan ke Database** — Data akan otomatis tersimpan di Supabase
# 4. **Dashboard** — Buka menu *Dashboard* untuk melihat visualisasi & filter

# Data yang sudah pernah diupload **tidak perlu diupload ulang** — otomatis dimuat dari database.
# """)

# # =========================================================
# # STATUS DATA
# # =========================================================
# if st.session_state.get("master_df") is not None:
#     df = st.session_state["master_df"]
#     st.success(
#         f"Data siap! Total **{len(df):,} baris** dari "
#         f"**{df['Nama Pasar'].nunique()} pasar** dan "
#         f"**{df['Pedagang'].nunique():,} pedagang**."
#     )
#     st.info("Buka menu **Dashboard** di sidebar kiri untuk melihat visualisasi.")

#     with st.expander("Preview data (10 baris pertama)"):
#         st.dataframe(df.head(10), use_container_width=True)

# elif "load_error" in st.session_state:
#     st.error(f"Gagal memuat data dari database: {st.session_state['load_error']}")
#     st.info("Silakan buka menu **Upload Data** untuk upload manual.")

# else:
#     st.warning("Belum ada data di database.")
#     st.info("Buka menu **Upload Data** di sidebar untuk upload file Excel pertama kali.")

import streamlit as st
import os
import pandas as pd
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.preprocessing import ensure_data_loaded

st.set_page_config(
    page_title="Dashboard Data Pasar 2020-2025",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# AUTO-LOAD DARI SUPABASE
# =========================================================
if st.session_state.get("master_df") is None:
    with st.spinner("Memuat data dari database..."):
        df_loaded, err = ensure_data_loaded()

    if err:
        st.session_state["load_error"] = err

st.title("Dashboard Data Pasar Tahun 2020 - 2025")
st.markdown("---")

st.markdown("""
### Selamat Datang di Sistem Dashboard PT Pasar Surya!
Aplikasi ini digunakan untuk memvisualisasikan data tagihan pasar dari tahun **2020 - 2025**.

### Cara Menggunakan:
1. **Upload Data** — Silahkan buka menu *Upload Data* untuk upload file Excel mentah.
2. **Preprocessing** — Sistem akan otomatis menggabungkan dan membersihkan data.
3. **Simpan ke Database** — Data akan otomatis tersimpan di Database.
4. **Dashboard** — Buka menu *Dashboard* untuk melihat visualisasi & filter.

Catatan: Data yang sudah pernah diupload **tidak perlu diupload ulang** dan otomatis dimuat dari database.
""")

if st.session_state.get("master_df") is not None:
    df = st.session_state["master_df"]
    st.success(
        f"Data sudah tersedia di database!! Total **{len(df):,} baris** dari "
        f"**{df['Nama Pasar'].nunique()} pasar** dan "
        f"**{df['Pedagang'].nunique():,} pedagang**."
    )
    st.info("Silahkan buka menu **Dashboard** di sidebar kiri untuk melihat visualisasi.")

    # with st.expander("Preview data (10 baris pertama)"):
    #     st.dataframe(df.head(10), use_container_width=True)

elif "load_error" in st.session_state:
    st.error(f"Gagal memuat data dari database: {st.session_state['load_error']}")
    st.info("Silakan buka menu **Upload Data** untuk upload manual.")

else:
    st.warning("Belum ada data di database.")
    st.info("Buka menu **Upload Data** di sidebar untuk upload file Excel pertama kali.")
