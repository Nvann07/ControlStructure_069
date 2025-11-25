
import sqlite3
import tkinter as tk 
import tkinter.messagebox as msg

# ==== SETUP FATABASE ===
conn = conn = sqlite3.connect("data_siswa.db")
cursor = conn.cursor()
cursor.execute(""" CREATE TABLE IF NOT EXISTS nilai_siswa(
    nama_siswa TEXT,
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi_fakultas TEXT
    )
    """)
conn.commit()

root = tk.Tk()
root.title("Input Nilai Siswa")
root.geometry("350x420")

judul = tk.Label(root, text="Forum Input")
judul.pack(side="top")


label_nama = tk.Label(root, text="Nama siswa")
label_nama.pack()
ne = tk.Entry()
ne.pack(pady=3)

label_bio = tk.Label(root, text="Nilai Biologi")
label_bio.pack()
be = tk.Entry(root)
be.pack(pady=3)

label_fis = tk.Label(root, text="Nilai Fisika")
label_fis.pack()
fe = tk.Entry(root)
fe.pack(pady=3)

label_ing = tk.Label(root, text="Nilai Bahasa Inggris")
label_ing.pack()
ie = tk.Entry(root,)
ie.pack(pady=3)

def Prediksi():
    try:
        nama = ne.get()
        bio = int(be.get())
        fis = int(fe.get())
        ing = int(ie.get())
    except ValueError:
        msg.showerror("Error", "Masukkan nilai angka yang valid!")
        return


    if bio > fis and bio > ing:
        prediksi = "Kedokteran"
    elif fis > bio and fis > ing:
        prediksi = "Teknik"
    else:
        prediksi = "Bahasa"

    
    conn.execute("INSERT INTO nilai_siswa VALUES (?, ?, ?, ?, ?)",
              (nama, bio, fis, ing, prediksi))
    conn.commit()

    msg.showinfo("Hasil Prediksi", f"Prediksi Fakultas: {prediksi}")

submit_btn = tk.Button(root, text="Submit Nilai", command=Prediksi)
submit_btn.pack(pady=10)

root.mainloop()





