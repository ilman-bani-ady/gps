import tkinter as tk
import time
import csv
from math import radians, sin, cos, sqrt, atan2

# List rute
rute_list = [
             "JAK.01-R01	TANJUNG PRIOK - PLUMPANG",
             "JAK.01-R02	PLUMPANG - TANJUNG PRIOK",
             "JAK.02-R04	DUREN SAWIT - KAMPUNG MELAYU",
             "JAK.02-R02	DUREN SAWIT - KAMPUNG MELAYU"
             
             ]
current_rute_index = 0
is_not_serving = False  # Status 'Tidak Melayani'
is_blinking = False      # Status berkedip teks 'Penuh'

# Add at the top of the file with other global variables
route_data = []  # Initialize empty list

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

def load_route_data(filename):
    route_data = []
    with open(filename, 'r') as file:
        # Skip header line if it exists
        next(file, None)  # This skips the first line
        
        for line in file:
            if line.strip():  # Skip empty lines
                try:
                    parts = line.strip().split(',')
                    route_data.append({
                        'route': parts[0],
                        'lon': float(parts[1]),
                        'lat': float(parts[2]),
                        'code': parts[3],
                        'name': parts[4],
                        'sound': parts[5]
                    })
                except (ValueError, IndexError) as e:
                    print(f"Skipping invalid line: {line.strip()}")
                    continue
    return route_data

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c * 1000  # Convert to meters
    
    return distance

def read_current_location():
    try:
        with open('/root/tesis/gps/mqtt/assets/current_location.txt', 'r') as file:
            lon, lat = file.read().strip().split(',')
            return float(lon), float(lat)
    except Exception as e:
        print(f"Error reading location: {e}")
        return None, None

def update_status():
    global route_data
    current_time = time.strftime("%H:%M:%S")
    
    # Read GPS coordinates from file
    gps_longitude, gps_latitude = read_current_location()
    if gps_longitude is None or gps_latitude is None:
        connection_status = "Disconnected"
    else:
        connection_status = "Connected"
    
    # Update GPS status
    gps_status_label.config(
        text=f"Jam: {current_time} | GPS Lat: {gps_latitude} | GPS Lon: {gps_longitude} | Status: {connection_status}"
    )
    
    # Check for nearby locations
    if gps_latitude and gps_longitude:
        for location in route_data:
            distance = calculate_distance(gps_latitude, gps_longitude, 
                                       location['lat'], location['lon'])
            
            # If within 30 meters of a location
            if distance <= 30:
                footer_rute_label.config(text=f"Lokasi: {location['name']} | Jarak: {distance:.1f}m")
                print(f"Near {location['name']}: {distance:.1f}m")  # Debug info
                break
            else:
                footer_rute_label.config(text="Sedang Dalam Perjalanan")
    
    root.after(1000, update_status)

def read_device_id():
    try:
        with open('/root/tesis/gps/mqtt/assets/bustrack.txt', 'r') as file:
            for line in file:
                if line.startswith('DEVICEID='):
                    device_id = line.split('=')[1].strip()
                    return device_id
        return "N/A"  # Return N/A if DEVICEID line not found
    except Exception as e:
        print(f"Error reading device ID: {e}")
        return "N/A"

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

# Load logo left images
left_logo = tk.PhotoImage(file="/root/tesis/gps/mqtt/assets/lego.png")  # Using forward slashes

# Increase subsample values to make the logo smaller (e.g., 4,4 or 6,6)
left_logo = left_logo.subsample(14, 14)  # Try different values to get desired size

# Replace text labels with image labels
tk.Label(header_content, image=left_logo, bg="blue").pack(side="left", padx=10)  # Reduced padding
tk.Label(header_content, text="Hello World Header", bg="blue", fg="white", font=("Arial", 24)).pack(side="left", expand=True)

# Important: Keep a reference to prevent garbage collection
root.left_logo = left_logo

# Load logo right images
right_logo = tk.PhotoImage(file="/root/tesis/gps/mqtt/assets/lego.png")  # Using forward slashes

# Increase subsample values to make the logo smaller (e.g., 4,4 or 6,6)
right_logo = right_logo.subsample(14, 14)  # Try different values to get desired size

# Replace text labels with image labels
tk.Label(header_content, image=right_logo, bg="blue").pack(side="right", padx=10)  # Reduced padding

# Important: Keep a reference to prevent garbage collection
root.right_logo = right_logo


# Status GPS dan Waktu
status_frame = tk.Frame(root, bg="lightgray")
status_frame.pack(side="top", fill="x")
gps_status_label = tk.Label(status_frame, text="", bg="lightgray", fg="black", font=("Arial", 16))
gps_status_label.pack(pady=10)

# Body
body_frame = tk.Frame(root, bg="white")
body_frame.pack(expand=True, fill="both", padx=20, pady=10)


tk.Label(body_frame, text="No Body:", bg="white", font=("Arial", 18), anchor="w").pack(anchor="w")
#tk.Label(body_frame, text="Nama Pramudi:", bg="white", font=("Arial", 18), anchor="w").pack(anchor="w")
device_id_label = tk.Label(body_frame, text=f"Device ID: {read_device_id()}", 
                          bg="white", font=("Arial", 18), anchor="w")
device_id_label.pack(anchor="w")
tk.Label(body_frame, text="No GSM:", bg="white", font=("Arial", 18), anchor="w").pack(anchor="w")
tk.Label(body_frame, text="Speed:", bg="white", font=("Arial", 18), anchor="w").pack(anchor="w")
rute_label = tk.Label(body_frame, text="Rute: ", bg="white", font=("Arial", 20), anchor="w")
rute_label.pack(anchor="w")

status_label = tk.Label(body_frame, text="Status: Layanan Aktif", bg="white", font=("Arial", 20), anchor="w")
status_label.pack(anchor="w")

# Label untuk 'Penuh'
penuh_label = tk.Label(body_frame, text="", bg="white", fg="red", font=("Arial", 20), anchor="w")
penuh_label.pack(anchor="w")

# Footer
footer = tk.Frame(root, bg="green", height=50)
footer.pack(side="bottom", fill="x")
footer_rute_label = tk.Label(footer, text="Rute: Jak.001", bg="green", fg="white", font=("Arial", 22))
footer_rute_label.place(x=root.winfo_width(), y=10)

# footer_status_label = tk.Label(footer, text="Layanan Aktif", bg="green", fg="white", font=("Arial", 16))
# footer_status_label.pack(side="right", padx=20)

# Tombol dan Navigasi
button_row = tk.Frame(root)
button_row.pack(side="bottom", fill="x", pady=10)

button_group = tk.Frame(button_row)
button_group.pack(side="left", padx=20)

# Mengatur ukuran tombol
button_width = 15

melayani_button = tk.Button(button_group, text="Melayani", bg="green", fg="white", font=("Arial", 22), width=button_width, command=on_melayani_click)
melayani_button.grid(row=0, column=0, padx=5, pady=2)

not_serving_button = tk.Button(button_group, text="Tidak Melayani", bg="orange", fg="white", font=("Arial", 22), width=button_width, command=on_not_serving_click)
not_serving_button.grid(row=1, column=0, padx=5, pady=2)

red_button = tk.Button(button_group, text="Penuh", bg="red", fg="white", font=("Arial", 22), width=button_width, command=on_red_button_click)
red_button.grid(row=0, column=1, padx=5, pady=2)

isi_bbm_button = tk.Button(button_group, text="Isi BBM", bg="blue", fg="white", font=("Arial", 22), width=button_width, command=on_isi_bbm_click)
isi_bbm_button.grid(row=1, column=1, padx=5, pady=2)

nav_button_frame = tk.Frame(button_row)
nav_button_frame.pack(side="right", padx=20)

prev_button = tk.Button(nav_button_frame, text="Prev", bg="yellow", font=("Arial", 23), command=on_prev)
prev_button.pack(side="left", padx=5)

next_button = tk.Button(nav_button_frame, text="Next", bg="yellow", font=("Arial", 23), command=on_next)
next_button.pack(side="left", padx=5)

# Memulai Animasi dan Pembaruanx``
move_footer_text()
update_status()
update_rute()

# Before root.mainloop(), load the route data
route_data = load_route_data('/root/tesis/gps/mqtt/assets/stopseq.txt')

root.mainloop()