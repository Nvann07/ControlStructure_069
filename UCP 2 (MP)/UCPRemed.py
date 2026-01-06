import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

DB_NAME = 'Management_Lab.db'

# ================= DATABASE =================
def setup_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_perangkat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_perangkat TEXT NOT NULL,
            merk TEXT NOT NULL,
            kategori TEXT NOT NULL,
            tahun_pembelian INTEGER NOT NULL,
            Peminjam TEXT,
            status_peminjaman TEXT NOT NULL,
            kondisi TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# ================= CRUD =================
def insert_data(nama, merk, kategori, tahun, peminjam, status, kondisi):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO data_perangkat 
            (nama_perangkat, merk, kategori, tahun_pembelian, peminjam, status_peminjaman, kondisi)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nama, merk, kategori, tahun, peminjam, status, kondisi))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

def update_data(id_data, nama, merk, kategori, tahun, peminjam, status, kondisi):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE data_perangkat
        SET nama_perangkat=?, merk=?, kategori=?, tahun_pembelian=?,
            peminjam=?, status_peminjaman=?, kondisi=?
        WHERE id=?
    """, (nama, merk, kategori, tahun, peminjam, status, kondisi, id_data))
    conn.commit()
    conn.close()

def delete_data(id_data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM data_perangkat WHERE id=?", (id_data,))
    conn.commit()
    conn.close()



def search_items():
    keyword = entry_search.get()

    # Bersihkan tabel
    tree.delete(*tree.get_children())

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = """
        SELECT * FROM data_perangkat
        WHERE nama_perangkat LIKE ?
        OR merk LIKE ?
        OR kategori LIKE ?
    """

    value = f"%{keyword}%"
    cursor.execute(query, (value, value, value))
    rows = cursor.fetchall()
    conn.close()

    # Tampilkan hasil ke tabel
    for row in rows:
        tree.insert("", tk.END, values=row)

    if not rows:
        messagebox.showinfo("Hasil Pencarian", "Data tidak ditemukan")

# ================= GUI FUNCTION =================
def load_data_to_table():
    for item in tree.get_children():
        tree.delete(item)
        rows = cur.fetchall()
    for row in rows:
        tree.insert('', tk.END, values=row)

def submit_data():
    nama = entry_nama.get()
    merk = entry_merk.get()
    kategori = entry_kategori.get()
    tahun = entry_tahun.get()
    peminjam = entry_Peminjam.get()
    status = status_combo.get()
    kondisi = kondisi_combo.get()

    if not (nama and merk and kategori and tahun):
        messagebox.showwarning("Input Salah", "Field utama wajib diisi")
        return

    if not tahun.isdigit():
        messagebox.showerror("Error", "Tahun harus angka")
        return
        

    insert_data(nama, merk, kategori, int(tahun), peminjam, status, kondisi)
    clear_input()
    load_data_to_table()

def clear_input():
    entry_nama.delete(0, tk.END)
    entry_merk.delete(0, tk.END)
    entry_kategori.delete(0, tk.END)
    entry_tahun.delete(0, tk.END)
    entry_Peminjam.delete(0, tk.END)
    status_combo.set("Tersedia")
    kondisi_combo.set("Baik")

def edit_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Pilih Data", "Pilih data terlebih dahulu")
        return

    data = tree.item(selected[0])['values']

    win = tk.Toplevel(root)
    win.title("Ubah Data Perangkat Keras")
    win.backround = "#9E0559"

    labels = ["Nama Perangkat", "Merk", "Kategori", "Tahun Pembelian", "Peminjam", "Status", "Kondisi"]
    entries = []

    for i, text in enumerate(labels):
        tk.Label(win, text=text).grid(row=i, column=0, pady=5, sticky="w")

        if text == "Status":
            e = ttk.Combobox(win, values=["Tersedia", "Dipinjam"], state="readonly")
        elif text == "Kondisi":
            e = ttk.Combobox(win, values=["Baik", "Rusak"], state="readonly")
        else:
            e = tk.Entry(win)

        e.grid(row=i, column=1, pady=5)
        e.insert(0, data[i+1])
        entries.append(e)

    def simpan():
        update_data(
            data[0],
            entries[0].get(),
            entries[1].get(),
            entries[2].get(),
            int(entries[3].get()),
            entries[4].get(),
            entries[5].get(),
            entries[6].get()
        )
        load_data_to_table()
        win.destroy()



    tk.Button(win, text="Simpan", bg="green", fg="white",
              command=simpan).grid(row=7, column=0, pady=10)
    tk.Button(win,text="🔄 Reset",bg="black", fg="white",command=clear_edit).grid(row=7,column=1,pady=10)
def clear_edit():
    entry_nama.delete(0, tk.END)
    entry_merk.delete(0, tk.END)
    entry_kategori.delete(0, tk.END)
    entry_tahun.delete(0, tk.END)
    entry_Peminjam.delete(0, tk.END)
    status_combo.set("Tersedia")
    kondisi_combo.set("Baik")
  
def delete_selected():
    selected = tree.selection()
    if not selected:
        return

    if messagebox.askyesno("Konfirmasi", "Yakin hapus data?"):
        data_id = tree.item(selected[0])['values'][0]
        delete_data(data_id)
        load_data_to_table()

# ================= MAIN =================
setup_db()

root = tk.Tk()
root.title("Manajemen laboratorium komputer")
root.geometry("2000x550")


frame_input = tk.LabelFrame(root, text="Input Data", padx=10, pady=10)
frame_input.pack(side="left", fill="y", padx=10)

frame_data = tk.LabelFrame(root, text="Data Perangkat", padx=10, pady=10)
frame_data.pack(side="right", fill="both", expand=True)

tk.Label(frame_input, text="Nama Perangkat").grid(row=0, column=0, sticky="w")
entry_nama = tk.Entry(frame_input)
entry_nama.grid(row=0, column=1,pady=4)

tk.Label(frame_input, text="Merk").grid(row=1, column=0, sticky="w")
entry_merk = tk.Entry(frame_input)
entry_merk.grid(row=1, column=1,pady=4)

tk.Label(frame_input, text="Kategori").grid(row=2, column=0, sticky="w")
entry_kategori = tk.Entry(frame_input)
entry_kategori.grid(row=2, column=1,pady=4)

tk.Label(frame_input, text="Tahun Pembelian").grid(row=3, column=0, sticky="w")
entry_tahun = tk.Entry(frame_input)
entry_tahun.grid(row=3, column=1,pady=4)

tk.Label(frame_input, text="Peminjam").grid(row=4, column=0, sticky="w")
entry_Peminjam = ttk.Entry(frame_input)
entry_Peminjam.grid(row=4, column=1,pady=4)


tk.Label(frame_input, text="Status").grid(row=5, column=0, sticky="w")
status_combo = ttk.Combobox(frame_input, values=["Tersedia", "Dipinjam"], state="readonly")
status_combo.grid(row=5, column=1,pady=4)
status_combo.set("Tersedia")

tk.Label(frame_input, text="Kondisi").grid(row=6, column=0, sticky="w")
kondisi_combo = ttk.Combobox(frame_input, values=["Baik", "Rusak"], state="readonly")
kondisi_combo.grid(row=6, column=1,pady=4)
kondisi_combo.set("Baik")

tk.Button(frame_input, text="➕ Tambah", bg="green", fg="white",
          command=submit_data)\
    .grid(row=7, column=0, padx=5, pady=10, sticky="ew")

tk.Button(frame_input, text="🗑 Hapus", bg="red", fg="white",
          command=delete_selected)\
    .grid(row=7, column=1, padx=5, pady=10, sticky="ew")

tk.Button(frame_input, text="✏ Ubah", bg="black", fg="white",
          command=edit_data)\
    .grid(row=7, column=2, padx=5, pady=10, sticky="w")

tk.Button(frame_input, text="🔄 Reset", bg="black", fg="white",
          command=clear_input)\
    .grid(row=7, column=3, padx=5, pady=10, sticky="w")

columns = ("ID_Perangkat", "Nama Perangkat", "Merk", "Kategori", "Tahun Pembelian",
           "Peminjam", "Status", "Kondisi")


separator = ttk.Separator(frame_input, orient='horizontal')
separator.grid(row=8, column=0, columnspan=2, sticky='ew', pady=10,)

info_label = tk.Label(frame_input, text="💡 Klik item di tabel untuk mengubah/menghapus", 
font=('Arial', 9, 'italic'), fg='#666')
info_label.grid(row=9, column=0, columnspan=2, pady=5)


label_search = tk.Label(frame_input, text="🔍 Cari Item:", font=('Arial', 10, 'bold'))
label_search.grid(row=10, column=0, sticky='w', padx=(0, 5))

entry_search = tk.Entry(frame_input, width=20, font=('Arial', 10))
entry_search.grid(row=10, column=1, padx=4)

button_search = tk.Button(frame_input, text="Cari", command=search_items,
                         bg="#720D4D", fg='white', font=('Arial', 9, 'bold'))
button_search.grid(row=10, column=2, padx=4)

button_view = tk.Button(frame_input, text="Lihat Semua", command=search_items,
                       bg='#607D8B', fg='white', font=('Arial', 9, 'bold'))
button_view.grid(row=10, column=3, padx=4)


tree = ttk.Treeview(frame_data, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill="both", expand=True)

load_data_to_table()
root.mainloop()
