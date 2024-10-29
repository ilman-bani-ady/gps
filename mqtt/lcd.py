import tkinter as tk
import time

# Fungsi untuk memindahkan teks footer
def move_footer_text():
    current_x = footer_label.winfo_x()
    if current_x < -footer_label.winfo_width():
        footer_label.place(x=root.winfo_width(), y=10)  # Reset ke posisi awal
    else:
        footer_label.place(x=current_x - 2, y=10)  # Pindah ke kiri

    root.after(50, move_footer_text)

# Fungsi untuk mengupdate jam dan status GPS
def update_status():
    current_time = time.strftime("%H:%M:%S")  # Ambil jam saat ini
    gps_latitude = "12.345678"  # Contoh latitude
    gps_longitude = "98.765432"  # Contoh longitude
    connection_status = "Connected"  # Status koneksi

    # Update label dengan informasi terbaru
    status_label.config(text=f"Jam: {current_time} | GPS Lat: {gps_latitude} | GPS Lon: {gps_longitude} | Status: {connection_status}")

    # Panggil fungsi ini lagi setiap detik
    root.after(1000, update_status)

# Membuat window utama
root = tk.Tk()
root.title("Hello World GUI")

# Atur ukuran window 1024x600 dan posisikan di tengah layar
width, height = 1024, 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)

root.geometry(f"{width}x{height}+{x}+{y}")
root.resizable(False, False)  # Mengunci ukuran agar tidak bisa diubah

# Membuat frame header dengan warna biru
header = tk.Frame(root, bg="blue", height=50)
header.pack(side="top", fill="x")

# Membuat frame untuk logo dan teks header (horizontal)
header_content = tk.Frame(header, bg="blue")
header_content.pack(side="top", fill="x", pady=10)

# Placeholder untuk logo kiri
logo_left = tk.Label(header_content, text="[Logo Kiri]", bg="blue", fg="white", font=("Arial", 16))
logo_left.pack(side="left", padx=20)

# Teks header di tengah
header_label = tk.Label(header_content, text="Hello World Header", bg="blue", fg="white", font=("Arial", 24))
header_label.pack(side="left", expand=True)

# Placeholder untuk logo kanan
logo_right = tk.Label(header_content, text="[Logo Kanan]", bg="blue", fg="white", font=("Arial", 16))
logo_right.pack(side="right", padx=20)

# Frame untuk status di bawah header
status_frame = tk.Frame(root, bg="lightgray")
status_frame.pack(side="top", fill="x")

# Label untuk menampilkan status jam dan GPS
status_label = tk.Label(status_frame, text="", bg="lightgray", fg="black", font=("Arial", 16))
status_label.pack(pady=10)

# Frame untuk body
body_frame = tk.Frame(root, bg="white")
body_frame.pack(expand=True, fill="both", padx=20, pady=10)

# Menambahkan informasi di bagian kiri body
tk.Label(body_frame, text="Nama Pramudi:", bg="white", fg="black", font=("Arial", 16), anchor="w").pack(anchor="w")
tk.Label(body_frame, text="Speed:", bg="white", fg="black", font=("Arial", 16), anchor="w").pack(anchor="w")
tk.Label(body_frame, text="No Body:", bg="white", fg="black", font=("Arial", 16), anchor="w").pack(anchor="w")
tk.Label(body_frame, text="Device ID:", bg="white", fg="black", font=("Arial", 16), anchor="w").pack(anchor="w")
tk.Label(body_frame, text="No GSM:", bg="white", fg="black", font=("Arial", 16), anchor="w").pack(anchor="w")

# Membuat frame footer dengan warna hijau
footer = tk.Frame(root, bg="green", height=50)
footer.pack(side="bottom", fill="x")

# Teks footer yang akan bergerak
footer_label = tk.Label(footer, text="Hello World Footer", bg="green", fg="white", font=("Arial", 24))
footer_label.place(x=root.winfo_width(), y=10)  # Tempatkan di luar jendela

# Membuat label di tengah sebagai konten utama (tidak berubah)
content = tk.Label(root, text="Hello World!", font=("Arial", 40))
content.pack(expand=True)

# Fungsi untuk tombol Next dan Prev
def on_next():
    footer_label.config(text="Next Page Footer")

def on_prev():
    footer_label.config(text="Prev Page Footer")

# Status toggle untuk teks "Penuh"
penuh_visible = False

# Fungsi toggle untuk tombol merah
def on_red_button_click():
    global penuh_visible
    if penuh_visible:
        penuh_label.config(text="")
    else:
        penuh_label.config(text="Penuh", fg="red")
    penuh_visible = not penuh_visible

# Status toggle untuk "Tidak Melayani"
is_not_serving = False

# Fungsi untuk tombol "Tidak Melayani"
def on_not_serving_click():
    global is_not_serving
    if is_not_serving:
        footer_label.config(text="Hello World Footer")  # Kembali ke teks awal
    else:
        footer_label.config(text="Tidak Melayani")  # Ubah teks menjadi "Tidak Melayani"
    is_not_serving = not is_not_serving

# Membuat frame untuk baris tombol (horizontal) di atas footer
button_row = tk.Frame(root)
button_row.pack(side="bottom", fill="x", pady=10)

# Membuat tombol merah dan label "Penuh" di atasnya
red_button_frame = tk.Frame(button_row)
red_button_frame.pack(side="left", padx=20)

penuh_label = tk.Label(red_button_frame, text="", font=("Arial", 16))
penuh_label.pack()

red_button = tk.Button(red_button_frame, text="Tekan", bg="red", fg="white", font=("Arial", 16), command=on_red_button_click)
red_button.pack(pady=5)

# Membuat tombol "Tidak Melayani" di sebelah tombol merah
not_serving_button = tk.Button(red_button_frame, text="Tidak Melayani", bg="orange", fg="white", font=("Arial", 16), command=on_not_serving_click)
not_serving_button.pack(pady=5)

# Membuat frame untuk tombol Next dan Prev (di kanan)
nav_button_frame = tk.Frame(button_row)
nav_button_frame.pack(side="right", padx=20)

prev_button = tk.Button(nav_button_frame, text="Prev", bg="yellow", font=("Arial", 16), command=on_prev)
next_button = tk.Button(nav_button_frame, text="Next", bg="yellow", font=("Arial", 16), command=on_next)

prev_button.pack(side="left", padx=5)
next_button.pack(side="left", padx=5)

# Memulai pergerakan teks footer
move_footer_text()

# Memulai update status jam dan GPS
update_status()

# Menjalankan loop utama aplikasi
root.mainloop()
