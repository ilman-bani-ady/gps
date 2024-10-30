import tkinter as tk
import time

# List rute
rute_list = ["Jak.001", "Jak.002", "Jak.003", "Jak.004", "Jak.005"]
current_rute_index = 0
is_not_serving = False  # Status 'Tidak Melayani'
is_blinking = False      # Status berkedip teks 'Penuh'

def update_rute():
    selected_rute = rute_list[current_rute_index]
    rute_label.config(text=f"Rute: {selected_rute}")
    footer_rute_label.config(text=f"Rute: {selected_rute}")

def on_next():
    global current_rute_index
    current_rute_index = (current_rute_index + 1) % len(rute_list)
    update_rute()

def on_prev():
    global current_rute_index
    current_rute_index = (current_rute_index - 1) % len(rute_list)
    update_rute()

def set_status(text):
    status_label.config(text=f"Status: {text}")
    # footer_status_label.config(text=text)

def on_melayani_click():
    set_status("Layanan Aktif")

def on_not_serving_click():
    global is_not_serving
    text = "Tidak Melayani" if not is_not_serving else "Layanan Aktif"
    set_status(text)
    is_not_serving = not is_not_serving

def blink_penuh():
    if is_blinking:
        current_text = penuh_label.cget("text")
        penuh_label.config(text="Penuh" if current_text == "" else "")
        root.after(500, blink_penuh)

def on_red_button_click():
    global is_blinking
    if is_blinking:
        is_blinking = False
        penuh_label.config(text="")
    else:
        is_blinking = True
        blink_penuh()

def on_isi_bbm_click():
    set_status("Sedang Mengisi BBM")

def move_footer_text():
    current_x = footer_rute_label.winfo_x()
    if current_x < -footer_rute_label.winfo_width():
        footer_rute_label.place(x=root.winfo_width(), y=10)
    else:
        footer_rute_label.place(x=current_x - 2, y=10)
    root.after(50, move_footer_text)

def update_status():
    current_time = time.strftime("%H:%M:%S")
    gps_latitude = "12.345678"
    gps_longitude = "98.765432"
    connection_status = "Connected"
    gps_status_label.config(
        text=f"Jam: {current_time} | GPS Lat: {gps_latitude} | GPS Lon: {gps_longitude} | Status: {connection_status}"
    )
    root.after(1000, update_status)

# Window Utama
root = tk.Tk()
root.title("Hello World GUI")
root.geometry("1024x600")
root.resizable(False, False)

# Header dan Logo
header = tk.Frame(root, bg="blue", height=50)
header.pack(side="top", fill="x")
header_content = tk.Frame(header, bg="blue")
header_content.pack(side="top", fill="x", pady=10)

tk.Label(header_content, text="[Logo Kiri]", bg="blue", fg="white", font=("Arial", 16)).pack(side="left", padx=20)
tk.Label(header_content, text="Hello World Header", bg="blue", fg="white", font=("Arial", 24)).pack(side="left", expand=True)
tk.Label(header_content, text="[Logo Kanan]", bg="blue", fg="white", font=("Arial", 16)).pack(side="right", padx=20)

# Status GPS dan Waktu
status_frame = tk.Frame(root, bg="lightgray")
status_frame.pack(side="top", fill="x")
gps_status_label = tk.Label(status_frame, text="", bg="lightgray", fg="black", font=("Arial", 16))
gps_status_label.pack(pady=10)

# Body
body_frame = tk.Frame(root, bg="white")
body_frame.pack(expand=True, fill="both", padx=20, pady=10)

tk.Label(body_frame, text="Nama Pramudi:", bg="white", font=("Arial", 16), anchor="w").pack(anchor="w")
tk.Label(body_frame, text="Speed:", bg="white", font=("Arial", 16), anchor="w").pack(anchor="w")
tk.Label(body_frame, text="No Body:", bg="white", font=("Arial", 16), anchor="w").pack(anchor="w")
tk.Label(body_frame, text="Device ID:", bg="white", font=("Arial", 16), anchor="w").pack(anchor="w")
tk.Label(body_frame, text="No GSM:", bg="white", font=("Arial", 16), anchor="w").pack(anchor="w")

rute_label = tk.Label(body_frame, text="Rute: ", bg="white", font=("Arial", 16), anchor="w")
rute_label.pack(anchor="w")

status_label = tk.Label(body_frame, text="Status: Layanan Aktif", bg="white", font=("Arial", 16), anchor="w")
status_label.pack(anchor="w")

# Label untuk 'Penuh'
penuh_label = tk.Label(body_frame, text="", bg="white", fg="red", font=("Arial", 16), anchor="w")
penuh_label.pack(anchor="w")

# Footer
footer = tk.Frame(root, bg="green", height=50)
footer.pack(side="bottom", fill="x")
footer_rute_label = tk.Label(footer, text="Rute: Jak.001", bg="green", fg="white", font=("Arial", 16))
footer_rute_label.place(x=root.winfo_width(), y=10)

# footer_status_label = tk.Label(footer, text="Layanan Aktif", bg="green", fg="white", font=("Arial", 16))
# footer_status_label.pack(side="right", padx=20)

# Tombol dan Navigasi
button_row = tk.Frame(root)
button_row.pack(side="bottom", fill="x", pady=10)

button_group = tk.Frame(button_row)
button_group.pack(side="left", padx=20)

melayani_button = tk.Button(button_group, text="Melayani", bg="green", fg="white", font=("Arial", 16), command=on_melayani_click)
melayani_button.grid(row=0, column=0, padx=5, pady=2)

not_serving_button = tk.Button(button_group, text="Tidak Melayani", bg="orange", fg="white", font=("Arial", 16), command=on_not_serving_click)
not_serving_button.grid(row=1, column=0, padx=5, pady=2)

red_button = tk.Button(button_group, text="Penuh", bg="red", fg="white", font=("Arial", 16), command=on_red_button_click)
red_button.grid(row=0, column=1, padx=5, pady=2)

isi_bbm_button = tk.Button(button_group, text="Isi BBM", bg="blue", fg="white", font=("Arial", 16), command=on_isi_bbm_click)
isi_bbm_button.grid(row=1, column=1, padx=5, pady=2)

nav_button_frame = tk.Frame(button_row)
nav_button_frame.pack(side="right", padx=20)

prev_button = tk.Button(nav_button_frame, text="Prev", bg="yellow", font=("Arial", 16), command=on_prev)
prev_button.pack(side="left", padx=5)

next_button = tk.Button(nav_button_frame, text="Next", bg="yellow", font=("Arial", 16), command=on_next)
next_button.pack(side="left", padx=5)

# Memulai Animasi dan Pembaruan
move_footer_text()
update_status()
update_rute()

root.mainloop()
