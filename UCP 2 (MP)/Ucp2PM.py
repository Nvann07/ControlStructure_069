import tkinter as tk
from tkinter import messagebox, ttk as msg
import sqlite3

DB_NAME = 'db_inventaris.db'


def setup_db():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_Perangkat_Keras(
                id_Perangkat INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_perangkat TEXT NOT NULL,
                merk TEXT NOT NULL ,
                kategori TEXT NOT NUL,
                Tahun_Pembelian INTEGER,
                          )
        """)

        cursor.excute("""
             CREATE TABLE IF NOT EXISTS data_Peminjaman_Perangkat(
               id_Peminjam INTEGER PRIMARY KEY AUTOINCEREMENT, 
               nama_Peminjam TEXT NOT NULL,
               tanggal_peminjaman,
               nama_perangkat,  
                      )
            """)
        conn.commit()
        conn.close()


def insert_Perangkat(Nama_Perangkat,Merk,Tahun_pembelian,Kategori):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Perangkat (nama_perangkat, merk, kategori, Tahun_Pembelian , kategori)
                VALUES (?, ?, ?, ?, ?)
            ''', (Nama_Perangkat, Merk, Tahun_pembelian,Kategori))
            conn.commit()
        finally:
            conn.close()

def add_Peminjaman(nama_Peminjam, Tanggal_peminjaman, Nama_Perangkat):
     try:
          conn = sqlite3.connect(DB_NAME)
          cur = conn.cursor()
          cur.execute("""
          INSERT INTO Peminjaman (Nama_Peminjam, Tanggal_Peminjaman, Nama_Perangkat)
          VALUES (?,?,?)
     
         """, (nama_Peminjam, Tanggal_peminjaman, Nama_Perangkat)) 
          conn.commit()
     finally:
          conn.close

def fetch_perangkat(search=""):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if search.strip() == "":
        cur.execute("SELECT id,code,name,price,stock FROM products ORDER BY id DESC")
    else:
        like = f"%{search}%"
        cur.execute("SELECT id,code,name,price,stock FROM products WHERE code LIKE ? OR name LIKE ? ORDER BY id DESC", (like,like))
    rows = cur.fetchall()
    conn.close()
    return rows


def update_perangkat(nama_perangkat, merk, Tahun_Pembelian,Kategori):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE products SET code=?, name=?, price=?, stock=? WHERE id=?", (nama_perangkat,merk,Tahun_Pembelian, Kategori))
    conn.commit()
    conn.close()


def fetch_all(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * data_Perangkat_Keras FROM  ORDER BY Tahun_Pembelian DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

def fetch_all(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data_Peminjaman ORDER BY Tanggal_Peminjaman DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows




#=== Perngkat Management ===== 
     
def insert_Perangkat(self):
     d = insert_Perangkat(self.root, "Tambah Perangkat")
     if d.result:
      code,name,price,stock = d.result
      try:
       insert_Perangkat(code,name,float(price),int(stock))
       msg.showinfo("OK", "Perangkat Ditambahakan")
       self.load_products()
      except Exception as e:
       msg.showerror("Error", str(e))



     
def load_data_to_table():
    for item in tree.get_children():
        tree.delete(item)
    data = fetch_all_data()
    for row in data:
        tree.insert('', 'end', values=row)

def submit_nilai():
    try:
        nama = entry_nama.get()
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        inggris = int(entry_inggris.get())
        if not nama or not (0 <= biologi <= 100) or not (0 <= fisika <= 100) or not (0 <= inggris <= 100):
            messagebox.showwarning("Input Tidak Valid", "Pastikan nama terisi dan nilai 0-100 valid.")
            return
    except ValueError:
        messagebox.showerror("Error Input", "Nilai harus berupa angka.")
        return

    prediksi = insert_data(nama, biologi, fisika, inggris)
    messagebox.showinfo("Sukses", f"Data {nama} berhasil disimpan.\nPrediksi Fakultas: {prediksi}")
    clear_input()
    load_data_to_table()

def clear_input():
    entry_nama.delete(0, tk.END)
    entry_biologi.delete(0, tk.END)
    entry_fisika.delete(0, tk.END)
    entry_inggris.delete(0, tk.END)

def edit_batal():
    entry_nama.delete(0, tk.END)
    entry_biologi.delete(0, tk.END)
    entry_fisika.delete(0, tk.END)
    entry_inggris.delete(0, tk.END)

def edit_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Pilih Data", "Silakan pilih data yang ingin diedit.")
        return
    item = tree.item(selected[0])
    data = item['values']

    win_n = tk.Toplevel(root)

    win_n.title("Edit Data Siswa")

    tk.Label(win_n, text="Nama Perangkat:").grid(row=0, column=0, pady=5, sticky='w')
    edit_nama = tk.Entry(win_n)
    edit_nama.grid(row=0, column=1, pady=5)
    edit_nama.insert(0, data[1])

    tk.Label(win_n, text="kategori:").grid(row=1, column=0, pady=5, sticky='w')
    edit_bio = tk.Entry(win_n)
    edit_bio.grid(row=1, column=1, pady=5)
    edit_bio.insert(0, data[2])

    tk.Label(win_n, text="Merk:").grid(row=2, column=0, pady=5, sticky='w')
    edit_fis = tk.Entry(win_n)
    edit_fis.grid(row=2, column=1, pady=5)
    edit_fis.insert(0, data[3])

    tk.Label(win_n, text=":").grid(row=3, column=0, pady=5, sticky='w')
    edit_ing = tk.Entry(win_n)
    edit_ing.grid(row=3, column=1, pady=5)
    edit_ing.insert(0, data[4])

    def simpan_edit():
        try:
            nama = edit_nama.get()
            biologi = int(edit_bio.get())
            fisika = int(edit_fis.get())
            inggris = int(edit_ing.get())
            if not nama or not (0 <= biologi <= 100) or not (0 <= fisika <= 100) or not (0 <= inggris <= 100):
                messagebox.showwarning("Input Tidak Valid", "Pastikan nama terisi dan nilai 0-100 valid.")
                return
        except ValueError:
            messagebox.showerror("Error Input", "Nilai harus berupa angka.")
            return
        prediksi = update_data(data[0], nama, biologi, fisika, inggris)
        messagebox.showinfo("Sukses", f"Data berhasil diperbarui.\nPrediksi Fakultas: {prediksi}")
        load_data_to_table()
        win_n.destroy()

    tk.Button(win_n, text="Simpan", command=simpan_edit, bg="red", fg="white").grid(row=4, column=0, columnspan=2, pady=10)
    tk.Button(win_n, text="Batal", command=edit_batal, width=5, bg="black", fg="white").grid(row=6, column=0, columnspan=2, pady=5)

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Pilih Data", "Silakan pilih data yang ingin dihapus.")
        return
    if messagebox.askyesno("Konfirmasi Hapus", "Apakah Anda yakin ingin menghapus data ini?"):
        item = tree.item(selected[0])
        data_id = item['values'][0]
        delete_data(data_id)
        load_data_to_table()

# ---------------- MAIN ----------------
setup_db()
root = tk.Tk()
root.title("Input Nilai Siswa - SQLite")

# Frames
frame_input = tk.LabelFrame(root, text="Form Input", padx=15, pady=15)
frame_input.pack(side='left', fill='y', padx=10, pady=5)

frame_data = tk.LabelFrame(root, text="Data Tersimpan", padx=5, pady=5)
frame_data.pack(side='left', fill='both', expand=True, padx=10, pady=5)
    
# Form Input
tk.Label(frame_input, text="Nama Siswa:").grid(row=0, column=0, sticky='w', pady=5)
entry_nama = tk.Entry(frame_input, width=25)
entry_nama.grid(row=0, column=1, pady=5)

tk.Label(frame_input, text="Biologi:").grid(row=1, column=0, sticky='w', pady=5)
entry_biologi = tk.Entry(frame_input, width=10)
entry_biologi.grid(row=1, column=1, pady=5)

tk.Label(frame_input, text="Fisika:").grid(row=2, column=0, sticky='w', pady=5)   
entry_fisika = tk.Entry(frame_input, width=10)
entry_fisika.grid(row=2, column=1, pady=5)

tk.Label(frame_input, text="Inggris:").grid(row=3, column=0, sticky='w', pady=5)
entry_inggris = tk.Entry(frame_input, width=10)
entry_inggris.grid(row=3, column=1, pady=5)

tk.Button(frame_input, text="Submit", command=submit_nilai, width=8, bg="green", fg="white").grid(row=4, column=0, pady=15)
tk.Button(frame_input, text="Clear", command=clear_input, width=8, bg="blue", fg="white").grid(row=4, column=1, pady=15)
tk.Button(frame_input, text="Edit", command=edit_data, width=20, bg="black", fg="white").grid(row=5, column=0, columnspan=3, pady=5)
tk.Button(frame_input, text="Hapus", command=delete_selected, width=20, bg="red", fg="white").grid(row=6, column=0, columnspan=3, pady=5)


# Treeview
kolom = ('id', 'nama', 'biologi', 'fisika', 'inggris', 'prediksi')
tree = ttk.Treeview(frame_data, columns=kolom, show='headings')
for col in kolom:
    tree.heading(col, text=col.capitalize())
tree.column('id', width=30, anchor='center')
tree.column('nama', width=120, anchor='w')
tree.column('biologi', width=60, anchor='center')
tree.column('fisika', width=60, anchor='center')
tree.column('inggris', width=60, anchor='center')
tree.column('prediksi', width=90, anchor='center')

scrollbar = ttk.Scrollbar(frame_data, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side='right', fill='y')
tree.pack(fill='both', expand=True)

load_data_to_table()
root.mainloop()





