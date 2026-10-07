import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helper import (
    format_rupiah, format_angka,
    format_rupiah_singkat, format_angka_singkat,
    format_miliar,
)
from utils.preprocessing import ensure_data_loaded   # ⭐ TAMBAHAN

st.set_page_config(
    page_title="Dashboard Data Pasar",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
    .main-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1f2937;
        margin: 4px 0 12px 0;
        padding-bottom: 6px;
        border-bottom: 2px solid #e2e8f0;
    }
    .top-pasar-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 8px 12px;
        max-height: 420px;
        overflow-y: auto;
    }
    .top-pasar-item {
        display: flex;
        align-items: center;
        padding: 9px 6px;
        border-bottom: 1px solid #f1f5f9;
        font-size: 0.92rem;
    }
    .top-pasar-item:last-child { border-bottom: none; }
    .top-pasar-rank {
        font-weight: 700;
        color: #3b82f6;
        width: 34px;
        text-align: right;
        margin-right: 12px;
    }
    .top-pasar-name {
        font-weight: 600;
        color: #0f172a;
        flex: 1;
    }
    .top-pasar-value {
        font-weight: 600;
        color: #16a34a;
        font-size: 0.88rem;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# AUTO-LOAD DARI SUPABASE
# =========================================================
if st.session_state.get("master_df") is None:
    with st.spinner("Memuat data dari database..."):
        df_loaded, err = ensure_data_loaded()

    if err:
        st.error(f"Gagal memuat data dari database: {err}")
        st.info("Silakan buka menu **Upload Data** untuk upload manual.")
        st.stop()

    if df_loaded is None or df_loaded.empty:
        st.warning("Belum ada data di database.")
        st.info("Silakan buka menu **Upload Data** terlebih dahulu.")
        st.stop()


# =========================================================
# AMBIL DATA DARI SESSION
# =========================================================
df = st.session_state["master_df"].copy()
df["Tgl Bayar_dt"] = pd.to_datetime(df["Tgl Bayar"], format="%d-%m-%Y", errors="coerce")


# =========================================================
# JUDUL
# =========================================================
st.markdown(
    '<div class="main-title">Dashboard Data Pasar Tahun 2020 - 2025</div>',
    unsafe_allow_html=True
)
st.info("Data terakhir pada tanggal 30-12-2025")


# =========================================================
# SIDEBAR FILTER
# =========================================================
with st.sidebar:
    st.markdown("### Filter")

    tgl_min = df["Tgl Bayar_dt"].min()
    tgl_max = df["Tgl Bayar_dt"].max()

    if pd.notna(tgl_min) and pd.notna(tgl_max):
        tgl_range = st.date_input(
            "Tgl Bayar",
            value=(tgl_min.date(), tgl_max.date()),
            min_value=tgl_min.date(),
            max_value=tgl_max.date()
        )
    else:
        tgl_range = None

    pasar_opts = sorted(df["Nama Pasar"].dropna().unique().tolist())
    pasar_sel = st.multiselect("Nama Pasar", pasar_opts, default=[])

    alamat_opts = sorted(df["Alamat"].dropna().unique().tolist())
    alamat_sel = st.multiselect("Alamat", alamat_opts, default=[])

    stand_opts = sorted(df["Stand"].dropna().unique().tolist())
    stand_sel = st.multiselect("Stand", stand_opts, default=[])

    pedagang_opts = sorted(df["Pedagang"].dropna().unique().tolist())
    pedagang_sel = st.multiselect("Pedagang", pedagang_opts, default=[])

    cabang_opts = sorted(df["Cabang"].dropna().unique().tolist())
    cabang_sel = st.multiselect("Cabang", cabang_opts, default=[])

    jenis_opts = sorted(df["Jenis Tagihan"].dropna().unique().tolist())
    jenis_sel = st.multiselect("Jenis Tagihan", jenis_opts, default=[])


# =========================================================
# APPLY FILTER
# =========================================================
filtered = df.copy()

if tgl_range and len(tgl_range) == 2:
    start, end = pd.Timestamp(tgl_range[0]), pd.Timestamp(tgl_range[1])
    filtered = filtered[
        (filtered["Tgl Bayar_dt"] >= start) &
        (filtered["Tgl Bayar_dt"] <= end)
    ]

if pasar_sel:
    filtered = filtered[filtered["Nama Pasar"].isin(pasar_sel)]
if alamat_sel:
    filtered = filtered[filtered["Alamat"].isin(alamat_sel)]
if stand_sel:
    filtered = filtered[filtered["Stand"].isin(stand_sel)]
if pedagang_sel:
    filtered = filtered[filtered["Pedagang"].isin(pedagang_sel)]
if cabang_sel:
    filtered = filtered[filtered["Cabang"].isin(cabang_sel)]
if jenis_sel:
    filtered = filtered[filtered["Jenis Tagihan"].isin(jenis_sel)]

if filtered.empty:
    st.warning("Tidak ada data yang cocok dengan filter.")
    st.stop()

warna_jenis = {
    "Listrik": "#3b82f6",
    "Tempat":  "#f59e0b",
    "Air":     "#8b5cf6",
}
urutan_jenis = ["Listrik", "Tempat", "Air"]


# =========================================================
# KPI CARDS
# =========================================================
k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Total Data", format_angka(len(filtered)))
k2.metric("Total Pendapatan", format_miliar(filtered["Nilai"].sum()))
k3.metric("Total Pasar", format_angka(filtered["Nama Pasar"].nunique()))
k4.metric("Total Stand", format_angka(filtered["Stand"].nunique()))
k5.metric("Total Pedagang", format_angka(filtered["Pedagang"].nunique()))

st.markdown("---")


# =========================================================
# BARIS 1: Top Pendapatan Pasar (kiri) + Nilai Tagihan per Cabang (kanan)
# =========================================================
col_left, col_right = st.columns([1, 2], gap="medium")

with col_left:
    st.markdown('<div class="section-title">Top Pendapatan Pasar</div>',
                unsafe_allow_html=True)

    top_pasar = (
        filtered.groupby("Nama Pasar", as_index=False)["Nilai"]
        .sum()
        .sort_values("Nilai", ascending=False)
        .reset_index(drop=True)
    )

    html_items = []
    for i, row in top_pasar.iterrows():
        html_items.append(
            f'<div class="top-pasar-item">'
            f'  <div class="top-pasar-rank">{i + 1}.</div>'
            f'  <div class="top-pasar-name">{row["Nama Pasar"]}</div>'
            f'  <div class="top-pasar-value">{format_rupiah_singkat(row["Nilai"])}</div>'
            f'</div>'
        )

    html = '<div class="top-pasar-container">' + "".join(html_items) + '</div>'
    st.markdown(html, unsafe_allow_html=True)
    st.caption(f"1 - {len(top_pasar)} / {len(top_pasar)}")


with col_right:
    st.markdown('<div class="section-title">Nilai Tagihan per Cabang</div>',
                unsafe_allow_html=True)

    grouped_cabang = (
        filtered.groupby("Cabang", as_index=False)["Nilai"]
        .sum()
        .sort_values("Nilai", ascending=False)
    )

    grouped_cabang["Cabang_label"] = "Cabang " + grouped_cabang["Cabang"].astype(str)

    fig_cabang = go.Figure(go.Bar(
        x=grouped_cabang["Cabang_label"],
        y=grouped_cabang["Nilai"],
        marker_color="#3b82f6",
        text=[format_angka_singkat(v) for v in grouped_cabang["Nilai"]],
        textposition="outside",
        textfont=dict(size=11, color="#374151"),
        hovertemplate="<b>%{x}</b><br>Rp %{y:,.0f}<extra></extra>",
        width=0.5,
    ))

    fig_cabang.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=12, color="#374151"),
            type="category",
            categoryorder="array",
            categoryarray=grouped_cabang["Cabang_label"].tolist(),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#f1f5f9",
            tickfont=dict(size=11, color="#6b7280"),
            tickformat=".2s",
        ),
        font=dict(family="Arial, sans-serif"),
    )

    st.plotly_chart(fig_cabang, use_container_width=True, config={"displayModeBar": False})


# =========================================================
# BARIS 2: Distribusi Jenis Tagihan (kiri) + Nilai Tagihan per Pasar (kanan)
# =========================================================
col_a, col_b = st.columns([1, 2], gap="medium")

with col_a:
    st.markdown('<div class="section-title">Distribusi Jenis Tagihan</div>',
                unsafe_allow_html=True)

    distribusi = (
        filtered.groupby("Jenis Tagihan", as_index=False)["Nilai"]
        .sum()
        .sort_values("Nilai", ascending=False)
    )

    total_nilai = distribusi["Nilai"].sum()

    fig_pie = go.Figure(data=[go.Pie(
        labels=distribusi["Jenis Tagihan"],
        values=distribusi["Nilai"],
        hole=0.55,
        marker=dict(colors=[
            warna_jenis.get(j, "#94a3b8") for j in distribusi["Jenis Tagihan"]
        ]),
        textinfo="label+percent",
        textfont=dict(size=12),
        hovertemplate="<b>%{label}</b><br>Rp %{value:,.0f}<br>%{percent}<extra></extra>",
    )])

    fig_pie.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=-0.05,
            xanchor="center", x=0.5,
            font=dict(size=11),
        ),
        annotations=[
            dict(
                text=f"<b>{format_angka_singkat(total_nilai)}</b><br>"
                     f"<span style='font-size:11px;color:#6b7280'>Total</span>",
                x=0.5, y=0.5,
                font=dict(size=16, color="#0f172a"),
                showarrow=False,
            )
        ],
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif"),
    )

    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})


with col_b:
    st.markdown('<div class="section-title">Nilai Tagihan per Pasar (Top 5)</div>',
                unsafe_allow_html=True)

    # Ambil Top 5 pasar berdasarkan total nilai
    top5_df = (
        filtered.groupby("Nama Pasar", as_index=False)["Nilai"]
        .sum()
        .sort_values("Nilai", ascending=False)
        .head(5)
    )
    top5_list = top5_df["Nama Pasar"].astype(str).tolist()

    # Filter hanya untuk Top 5 pasar
    df_top = filtered[filtered["Nama Pasar"].astype(str).isin(top5_list)].copy()

    # Agregasi: Pasar x Jenis Tagihan
    grouped_pasar = (
        df_top.groupby(["Nama Pasar", "Jenis Tagihan"], as_index=False)["Nilai"]
        .sum()
    )

    # ⭐ Konversi ke string biasa (BUKAN pyarrow) supaya bisa di-reindex
    grouped_pasar["Nama Pasar"] = grouped_pasar["Nama Pasar"].astype(str)
    grouped_pasar["Pasar_label"] = "Pasar " + grouped_pasar["Nama Pasar"]

    # ⭐ Konversi kolom ke object string biasa
    grouped_pasar["Pasar_label"] = grouped_pasar["Pasar_label"].astype(object)
    grouped_pasar["Jenis Tagihan"] = grouped_pasar["Jenis Tagihan"].astype(object)
    grouped_pasar["Nilai"] = pd.to_numeric(grouped_pasar["Nilai"], errors="coerce").fillna(0)

    fig_pasar = go.Figure()

    for jenis in urutan_jenis:
        subset = grouped_pasar[grouped_pasar["Jenis Tagihan"] == jenis].copy()

        # ⭐ Konversi jadi pandas string biasa SEBELUM reindex
        subset["Pasar_label"] = subset["Pasar_label"].astype("string[python]")
        subset["Nilai"] = pd.to_numeric(subset["Nilai"], errors="coerce").fillna(0)

        # Target index
        # target_labels = [f"Pasar {p}" for p in top5_list]

        # Reindex dengan fill_value=0 (Nilai numerik, aman)
        subset = (
            subset.set_index("Pasar_label")
            .reindex([f"Pasar {p}" for p in top10_list], fill_value=0)
            .reset_index()
        )

        # Pastikan Nilai numerik
        subset["Nilai"] = pd.to_numeric(subset["Nilai"], errors="coerce").fillna(0)

        fig_pasar.add_trace(go.Bar(
            name=jenis,
            x=subset["Pasar_label"].astype(str),
            y=subset["Nilai"],
            marker_color=warna_jenis[jenis],
            text=[format_angka_singkat(v) if v > 0 else "" for v in subset["Nilai"]],
            textposition="outside",
            textfont=dict(size=9, color="#374151"),
            hovertemplate=(
                "<b>%{x}</b><br>"
                f"Jenis: {jenis}<br>"
                "Nilai: Rp %{y:,.0f}<extra></extra>"
            ),
            width=0.22,
        ))

    fig_pasar.update_layout(
        barmode="group",
        bargap=0.30,
        bargroupgap=0.10,
        height=420,
        margin=dict(l=10, r=10, t=30, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="left", x=0,
            font=dict(size=11),
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=10, color="#374151"),
            type="category",
            categoryorder="array",
            categoryarray=[f"Pasar {p}" for p in top5_list],
            tickangle=-30,
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#f1f5f9",
            tickfont=dict(size=11, color="#6b7280"),
            tickformat=".2s",
        ),
        font=dict(family="Arial, sans-serif"),
    )

    st.plotly_chart(fig_pasar, use_container_width=True, config={"displayModeBar": False})


# =========================================================
# BARIS 3: Tren Nilai per Bulan
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Tren Nilai Tagihan per Bulan</div>',
            unsafe_allow_html=True)

tren = (
    filtered.groupby("Tahun-Bulan", as_index=False)["Nilai"]
    .sum()
    .sort_values("Tahun-Bulan")
)

fig_tren = px.area(
    tren, x="Tahun-Bulan", y="Nilai",
    labels={"Tahun-Bulan": "", "Nilai": ""},
    color_discrete_sequence=["#3b82f6"]
)
fig_tren.update_layout(
    height=280,
    margin=dict(l=10, r=10, t=10, b=10),
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis=dict(showgrid=False, tickfont=dict(size=11)),
    yaxis=dict(showgrid=True, gridcolor="#f1f5f9", tickformat=".2s",
               tickfont=dict(size=11)),
)
fig_tren.update_traces(
    hovertemplate="<b>%{x}</b><br>Rp %{y:,.0f}<extra></extra>",
    line=dict(width=2),
)
st.plotly_chart(fig_tren, use_container_width=True, config={"displayModeBar": False})


# =========================================================
# TABEL DETAIL + DOWNLOAD
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)

with st.expander("Tampilkan tabel data lengkap & download", expanded=True):

    kolom_urut = [
        "Tgl Bayar",
        "Tgl Closing",
        "Cabang",
        "Nama Pasar",
        "Alamat",
        "Stand",
        "Pedagang",
        "Jenis Tagihan",
        "Periode",
        "Nilai"
    ]

    data_tampil = filtered[
        [kolom for kolom in kolom_urut if kolom in filtered.columns]
    ]

    st.dataframe(
        data_tampil,
        use_container_width=True,
        height=400
    )

    csv = data_tampil.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download hasil filter (CSV)",
        data=csv,
        file_name="data_pasar_filtered.csv",
        mime="text/csv"
    )
