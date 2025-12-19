import json
import os
from datetime import datetime
from openpyxl import Workbook

DATA_FILE = "cinema_data.json"
DEFAULT_THEME = {
    "primary": "#800000",
    "accent": "#FFD700",
    "bg": "#000000",
    "card": "#FFFFFF",
    "sold": "#4D0000",
    "available": "#FFFFFF",
    "selected": "#FFD700"
}

DEFAULT_DATA = {
    "saldo": 0,
    "riwayat_tiket": [],
    "kursi_terisi": {},
    "films": [
        {"id": 1, "judul": "Film A: Interstellar", "deskripsi": "Sci-fi epic"},
        {"id": 2, "judul": "Film B: The Dark Knight", "deskripsi": "Action/Crime"},
        {"id": 3, "judul": "Film C: Avatar 3D", "deskripsi": "Fantasy/Sci-fi"},
        {"id": 4, "judul": "Film D: Titanic", "deskripsi": "Drama/Romance"}
    ],
    "next_film_id": 5,
    "theme": DEFAULT_THEME
}

def ensure_file():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)

def load_data():
    ensure_file()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA.copy()

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_saldo():
    return load_data().get("saldo", 0)

def set_saldo(value):
    d = load_data()
    d["saldo"] = value
    save_data(d)

def get_riwayat():
    return load_data().get("riwayat_tiket", [])

def add_riwayat(ticket_obj):
    d = load_data()
    if "tanggal" not in ticket_obj:
        ticket_obj["tanggal"] = datetime.now().strftime("%Y-%m-%d")
    d.setdefault("riwayat_tiket", []).append(ticket_obj)
    save_data(d)

def get_riwayat_bulan_ini():
    riw = get_riwayat()
    now = datetime.now()
    awal_bulan = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    hasil = []
    for r in riw:
        try:
            tgl_str = r.get("tanggal")
            if not tgl_str:
                continue
            tgl = datetime.strptime(tgl_str, "%Y-%m-%d")
            if tgl >= awal_bulan:
                hasil.append(r)
        except Exception:
            continue
    return hasil

def export_riwayat_excel():
    data = get_riwayat_bulan_ini()
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Riwayat Pemesanan"
    
    # Kolom Header
    ws.append(["Tanggal", "Judul Film", "Studio", "Jam", "Kursi", "Total"])
    
    if not data:
        print("Peringatan: Tidak ada data riwayat untuk bulan ini.")
    else:
        for d in data:
            kursi = d.get("kursi", [])
            kursi_str = ", ".join(kursi) if isinstance(kursi, list) else str(kursi)
            ws.append([
                str(d.get("tanggal", "-")),
                str(d.get("judul", "-")),
                str(d.get("studio", "-")),
                str(d.get("jam", "-")),
                kursi_str,
                d.get("total", 0)
            ])
    
    output_file = "riwayat_pemesanan_bulan_ini.xlsx"
    try:
        wb.save(output_file)
        print(f"Sukses! File '{output_file}' berhasil dibuat.")
    except Exception as e:
        print(f"Gagal menyimpan file: {e}")

def get_kursi_terisi(key):
    return load_data().get("kursi_terisi", {}).get(key, [])

def add_kursi_terisi(key, seats):
    d = load_data()
    d.setdefault("kursi_terisi", {}).setdefault(key, []).extend(seats)
    d["kursi_terisi"][key] = sorted(list(set(d["kursi_terisi"][key])))
    save_data(d)

def get_films():
    return load_data().get("films", [])

def add_film(judul, deskripsi=""):
    d = load_data()
    fid = d.get("next_film_id", 1)
    f = {"id": fid, "judul": judul, "deskripsi": deskripsi}
    d.setdefault("films", []).append(f)
    d["next_film_id"] = fid + 1
    save_data(d)
    return f

def find_film(film_id):
    for f in get_films():
        if f["id"] == film_id:
            return f
    return None

def get_theme():
    return load_data().get("theme", DEFAULT_THEME.copy())