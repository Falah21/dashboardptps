# def format_rupiah(angka):
#     """Format angka menjadi Rupiah, contoh: 1,234,567"""
#     try:
#         return f"Rp {int(angka):,}".replace(",", ".")
#     except (ValueError, TypeError):
#         return "Rp 0"


# def format_angka(angka):
#     """Format angka dengan pemisah ribuan titik"""
#     try:
#         return f"{int(angka):,}".replace(",", ".")
#     except (ValueError, TypeError):
#         return "0"


# def format_rupiah(angka):
#     try:
#         return f"Rp {int(angka):,}".replace(",", ".")
#     except (ValueError, TypeError):
#         return "Rp 0"


# def format_angka(angka):
#     try:
#         return f"{int(angka):,}".replace(",", ".")
#     except (ValueError, TypeError):
#         return "0"


# def format_rupiah_singkat(angka):
#     try:
#         angka = float(angka)
#     except (ValueError, TypeError):
#         return "Rp 0"

#     if abs(angka) >= 1_000_000_000:
#         return f"Rp {angka / 1_000_000_000:.2f} M".replace(".", ",")
#     elif abs(angka) >= 1_000_000:
#         return f"Rp {angka / 1_000_000:.2f} Jt".replace(".", ",")
#     elif abs(angka) >= 1_000:
#         return f"Rp {angka / 1_000:.1f} Rb".replace(".", ",")
#     else:
#         return f"Rp {angka:,.0f}".replace(",", ".")


# def format_angka_singkat(angka):
#     try:
#         angka = float(angka)
#     except (ValueError, TypeError):
#         return "0"

#     if abs(angka) >= 1_000_000_000:
#         return f"{angka / 1_000_000_000:.1f} B".replace(".", ",")
#     elif abs(angka) >= 1_000_000:
#         return f"{angka / 1_000_000:.1f} M".replace(".", ",")
#     elif abs(angka) >= 1_000:
#         return f"{angka / 1_000:.0f} rb".replace(".", ",")
#     else:
#         return f"{angka:.0f}"

# def format_rupiah(angka):
#     """Format angka menjadi Rupiah lengkap, contoh: Rp 1.234.567"""
#     try:
#         return f"Rp {int(angka):,}".replace(",", ".")
#     except (ValueError, TypeError):
#         return "Rp 0"


# def format_angka(angka):
#     """Format angka dengan pemisah ribuan titik"""
#     try:
#         return f"{int(angka):,}".replace(",", ".")
#     except (ValueError, TypeError):
#         return "0"


# def format_rupiah_singkat(angka):
#     """
#     Format angka singkat untuk KPI card:
#     - >= 1 miliar  -> 'Rp 44,23 M'
#     - >= 1 juta    -> 'Rp 1,5 Jt'
#     - >= 1 ribu    -> 'Rp 12,3 Rb'
#     """
#     try:
#         angka = float(angka)
#     except (ValueError, TypeError):
#         return "Rp 0"

#     if abs(angka) >= 1_000_000_000:
#         return f"Rp {angka / 1_000_000_000:.2f} M".replace(".", ",")
#     elif abs(angka) >= 1_000_000:
#         return f"Rp {angka / 1_000_000:.2f} Jt".replace(".", ",")
#     elif abs(angka) >= 1_000:
#         return f"Rp {angka / 1_000:.1f} Rb".replace(".", ",")
#     else:
#         return f"Rp {angka:,.0f}".replace(",", ".")


# def format_angka_singkat(angka):
#     """Format angka singkat tanpa Rp (untuk chart axis)"""
#     try:
#         angka = float(angka)
#     except (ValueError, TypeError):
#         return "0"

#     if abs(angka) >= 1_000_000_000:
#         return f"{angka / 1_000_000_000:.1f} B".replace(".", ",")
#     elif abs(angka) >= 1_000_000:
#         return f"{angka / 1_000_000:.1f} M".replace(".", ",")
#     elif abs(angka) >= 1_000:
#         return f"{angka / 1_000:.0f} rb".replace(".", ",")
#     else:
#         return f"{angka:.0f}"

def format_rupiah(angka):
    """Format angka menjadi Rupiah lengkap, contoh: Rp 1.234.567"""
    try:
        return f"Rp {int(angka):,}".replace(",", ".")
    except (ValueError, TypeError):
        return "Rp 0"


def format_angka(angka):
    """Format angka dengan pemisah ribuan titik"""
    try:
        return f"{int(angka):,}".replace(",", ".")
    except (ValueError, TypeError):
        return "0"


def format_rupiah_singkat(angka):
    """Format angka singkat untuk list top pasar"""
    try:
        angka = float(angka)
    except (ValueError, TypeError):
        return "Rp 0"

    if abs(angka) >= 1_000_000_000:
        return f"Rp {angka / 1_000_000_000:.2f} M".replace(".", ",")
    elif abs(angka) >= 1_000_000:
        return f"Rp {angka / 1_000_000:.2f} Jt".replace(".", ",")
    elif abs(angka) >= 1_000:
        return f"Rp {angka / 1_000:.1f} Rb".replace(".", ",")
    else:
        return f"Rp {angka:,.0f}".replace(",", ".")


def format_miliar(angka):
    """
    Format angka jadi M (miliar) untuk KPI card.
    Contoh: 44_234_874_750 -> '44,23 M'
    """
    try:
        angka = float(angka)
    except (ValueError, TypeError):
        return "0 M"

    if abs(angka) >= 1_000_000_000:
        return f"{angka / 1_000_000_000:.2f} M".replace(".", ",")
    elif abs(angka) >= 1_000_000:
        return f"{angka / 1_000_000:.2f} Jt".replace(".", ",")
    elif abs(angka) >= 1_000:
        return f"{angka / 1_000:.1f} Rb".replace(".", ",")
    else:
        return f"{angka:,.0f}".replace(",", ".")


def format_angka_singkat(angka):
    """Format angka singkat tanpa Rp (untuk chart axis)"""
    try:
        angka = float(angka)
    except (ValueError, TypeError):
        return "0"

    if abs(angka) >= 1_000_000_000:
        return f"{angka / 1_000_000_000:.1f} B".replace(".", ",")
    elif abs(angka) >= 1_000_000:
        return f"{angka / 1_000_000:.1f} M".replace(".", ",")
    elif abs(angka) >= 1_000:
        return f"{angka / 1_000:.0f} rb".replace(".", ",")
    else:
        return f"{angka:.0f}"