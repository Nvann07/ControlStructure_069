
import tkinter as tk
from tkinter import messagebox

def prediksi():
  try:
    for entry in nmp: 
      nilai = int(entry.get())

    hasil_label.config(text="Prediksi Prodi: Teknologi Informasi")
  except ValueError:
        messagebox.showerror("Input Error", "Pastikan semua input adalah angka antara 0 dan 100.")


root = tk.Tk()
root.title("Aplikasi Prediksi Prodi Pilihan") 
root.geometry("500x600") 
root.configure(bg="#EDEAF0") 


judul_label = tk.Label(root, text="Aplikasi Prediksi Prodi Pilihan", font=("Times New Roman", 18, "bold"), bg="#E92020")
judul_label.pack(pady=20) 

frame_input = tk.Frame(root, bg="#E8E0E0")  
frame_input.pack(pady=10) 


nmp = []
for i in range(10): 
    label = tk.Label(frame_input, text=f"Nilai Mata Pelajaran {i+1}:", font=("Times New Roman", 12), bg="#E71616")
    label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
  
    entry = tk.Entry(frame_input, width=10, font=("Times New Roman", 12))
    entry.grid(row=i, column=1, padx=10, pady=5)
    nmp.append(entry)    


prediksi_button = tk.Button(root, text="Hasil Prediksi", command=prediksi, font=("Bookman Old Style", 12, "bold"))
prediksi_button.pack(pady=30)

hasil_label = tk.Label(root, text="", font=("Times New Roman", 14, "italic"), fg="blue", bg="#0F0404")
hasil_label.pack(pady=20)

root.mainloop() 