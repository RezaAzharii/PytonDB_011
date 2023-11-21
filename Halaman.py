# tombol_modul.py

import tkinter as tk
import sqlite3
from tkinter import messagebox

uiApp = tk.Tk()
uiApp.title("Aplikasi Prediksi Fakultas")
uiApp.geometry('600x600')
uiApp.resizable(False, False)

label_nama = tk.Label(uiApp, text="Nama Siswa")
label_nama.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
entry_nama = tk.Entry(uiApp)
entry_nama.grid(row=0, column=1, padx=10, pady=5)

label_biologi = tk.Label(uiApp, text="Nilai Biologi")
label_biologi.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
entry_biologi = tk.Entry(uiApp)
entry_biologi.grid(row=1, column=1, padx=10, pady=5)

label_fisika = tk.Label(uiApp, text="Nilai Fisika")
label_fisika.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
entry_fisika = tk.Entry(uiApp)
entry_fisika.grid(row=2, column=1, padx=10, pady=5)

label_inggris = tk.Label(uiApp, text="Nilai Inggris")
label_inggris.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
entry_inggris = tk.Entry(uiApp)
entry_inggris.grid(row=3, column=1, padx=10, pady=5)


    # Membuat button Hasil Prediksi
button_submit = tk.Button(uiApp, text="Submit", command=lambda: hasil_prediksi(entry_nama, entry_biologi, entry_fisika, entry_inggris, hasil_label))
button_submit.grid(row=4, column=0, columnspan=2, pady=10)


# Membuat label luaran hasil prediksi
hasil_label = tk.Label(uiApp, text="Hasil Prediksi: -", font=("Helvetica", 12))
hasil_label.grid(row=5, column=0, columnspan=2, pady=10)

# Membuat label untuk menampilkan kondisi
kondisi_label = tk.Label(uiApp, text="Kondisi: -", font=("Helvetica", 12))
kondisi_label.grid(row=6, column=0, columnspan=2, pady=10)


def hasil_prediksi(entry_nama, entry_biologi, entry_fisika, entry_inggris, hasil_label):
    # Mendapatkan nilai dari entry
    nama_siswa = entry_nama.get()
    nilai_biologi = int(entry_biologi.get())
    nilai_fisika = int(entry_fisika.get())
    nilai_inggris = int(entry_inggris.get())


    # Menghitung rata-rata nilai
    rata_rata_nilai = (nilai_biologi + nilai_fisika + nilai_inggris) / 3
    # Menentukan prediksi berdasarkan nilai tertinggi dan rata-rata
    prediksi_fakultas = ""
    if nilai_biologi >= 80 and nilai_biologi > nilai_fisika and nilai_biologi > nilai_inggris:
        prediksi_fakultas = "Kedokteran"
    elif nilai_fisika > nilai_biologi and nilai_fisika > nilai_inggris:
        prediksi_fakultas = "Teknik"
    elif nilai_inggris > nilai_biologi and nilai_inggris > nilai_fisika:
        prediksi_fakultas = "Bahasa"
    elif rata_rata_nilai >= 70:
        prediksi_fakultas = "Anda memenuhi syarat untuk beberapa fakultas"
    elif nilai_biologi < 50 or nilai_fisika < 50 or nilai_inggris < 50:
        prediksi_fakultas = "Anda tidak memenuhi syarat untuk fakultas manapun"
    else:
        prediksi_fakultas = "Anda tidak memenuhi syarat untuk fakultas manapun"

    # Menampilkan hasil prediksi
    hasil_label.config(text=f"Hasil Prediksi: {prediksi_fakultas}")

    # Menyimpan data ke database SQLite
    simpan_ke_database(nama_siswa, nilai_biologi, nilai_fisika, nilai_inggris, prediksi_fakultas)

def simpan_ke_database(nama_siswa, biologi, fisika, inggris, prediksi_fakultas):
    try:
        conn = sqlite3.connect("nilai_siswa.db")
        cursor = conn.cursor()

        # Membuat tabel jika belum ada
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nilai_siswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_siswa TEXT,
                biologi INTEGER,
                fisika INTEGER,
                inggris INTEGER,
                prediksi_fakultas TEXT
            )
        ''')

        # Menyimpan data ke tabel
        cursor.execute("INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) VALUES (?, ?, ?, ?, ?)",
                       (nama_siswa, biologi, fisika, inggris, prediksi_fakultas))

        conn.commit()
        conn.close()

        print("Data berhasil disimpan ke database.")
    except Exception as e:
        print(f"Error: {e}")


uiApp.mainloop()