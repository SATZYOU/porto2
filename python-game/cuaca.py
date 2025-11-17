# Import library yang diperlukan
import customtkinter as ctk      # Library GUI modern berbasis Tkinter
import requests                  # Untuk mengambil data dari API cuaca
from PIL import Image, ImageTk  # Untuk memproses gambar/icon cuaca
from io import BytesIO           # Untuk membaca data gambar dari internet

# Set tema tampilan GUI
ctk.set_appearance_mode("dark")       # Mode gelap
ctk.set_default_color_theme("blue")   # Tema warna biru

# Membuat jendela utama
app = ctk.CTk()
app.title("Cek Cuaca Modern")         # Judul aplikasi
app.geometry("1366x768")               # Ukuran jendela

# API key untuk OpenWeatherMap (diganti dengan punyamu sendiri)
API_KEY = "f80fee6bd7e579b9ec34ec10465f4b14"


# ------------------- FUNGSI CEK CUACA -------------------
def cek_cuaca():
    # Mengambil input nama kota dari user
    kota = entry_kota.get().strip()

    # Jika input kosong, tampilkan peringatan
    if kota == "":
        label_hasil.configure(text="⚠ Masukkan nama kota!")
        return

    # Jika user hanya menulis nama kota, tambahkan kode negara otomatis (id = Indonesia)
    if "," not in kota:
        kota = kota + ",id"

    # URL API untuk mengambil data cuaca
    url = f"https://api.openweathermap.org/data/2.5/weather?q={kota}&appid={API_KEY}&units=metric"

    try:
        data = requests.get(url).json()   # Mengambil data API dalam format JSON
    except:
        label_hasil.configure(text="❌ Tidak dapat terhubung ke server.")
        return

    # Jika API mengembalikan error (misal kota tidak ditemukan)
    if data.get("cod") != 200:
        label_hasil.configure(text=f"❌ Error: {data.get('message', 'Tidak diketahui')}")
        icon_label.configure(image="")   # Kosongkan icon
        return

    # Ambil data cuaca penting
    cuaca = data["weather"][0]["description"].title()  # Deskripsi cuaca
    suhu = data["main"]["temp"]                        # Suhu dalam °C
    icon_code = data["weather"][0]["icon"]             # Kode icon cuaca

    # URL icon cuaca berdasarkan kode icon
    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    img_data = requests.get(icon_url).content          # Ambil data gambar dari internet

    # Proses gambar icon
    img = Image.open(BytesIO(img_data)).resize((100, 100))
    img = ImageTk.PhotoImage(img)

    # Tampilkan icon pada label
    icon_label.configure(image=img)
    icon_label.image = img      # Diperlukan agar gambar tidak hilang akibat garbage collector

    # Tampilkan hasil cuaca pada label
    label_hasil.configure(
        text=f"Kota: {data['name']}\n"
             f"Cuaca: {cuaca}\n"
             f"Suhu: {suhu}°C"
    )


# ------------------- BAGIAN UI -------------------

# Judul aplikasi
judul = ctk.CTkLabel(app, text="🌤 CEK CUACA ", font=("Poppins", 22, "bold"))
judul.pack(pady=20)

# Input kota
entry_kota = ctk.CTkEntry(app, placeholder_text="Masukkan nama kota", width=260, height=40)
entry_kota.pack(pady=10)

# Tombol cek cuaca
btn_cek = ctk.CTkButton(app, text="Cek Cuaca", command=cek_cuaca, width=150, height=40)
btn_cek.pack(pady=10)

# Label untuk menampilkan icon cuaca
icon_label = ctk.CTkLabel(app, text="")
icon_label.pack(pady=10)

# Label untuk menampilkan hasil informasi cuaca
label_hasil = ctk.CTkLabel(app, text="", font=("Poppins", 16))
label_hasil.pack(pady=10)

# Menjalankan aplikasi
app.mainloop()
