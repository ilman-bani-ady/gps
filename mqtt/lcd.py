import tkinter as tk
import time
import csv
from math import radians, sin, cos, sqrt, atan2
from tkinter import messagebox
from gmqtt import Client as MQTTClient
import asyncio
import uuid
import serial

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

# Tambahkan variabel password
EXIT_PASSWORD = "666"  # Ganti dengan password yang diinginkan

# Add these constants near the top of the file with other global variables
MQTT_BROKER = "103.245.39.79"  # Replace with your MQTT broker
MQTT_PORT = 1883
MQTT_TOPIC = "bus/location"  # Topic for publishing location data
MQTT_CLIENT_ID = f'lcd-{uuid.uuid4().hex}'  # Generate unique client ID

# Add MQTT client setup
mqtt_client = None

# Add this global variable near the top with other globals
current_latitude = -6.179767
current_longitude = 106.934196

# Konfigurasi Serial untuk GPRS Modem
ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=9600,
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# Add near the top with other global variables
gsm_connection_status = False

def initialize_gsm_connection():
    global gsm_connection_status
    try:
        print("Starting GSM initialization...", flush=True)  # Debug start
        
        # Clear any existing data in the buffer
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Send AT Command to check TCP connection
        command = b'AT+CIPSTART="TCP","103.245.39.79","80"\r\n'
        ser.write(command)
        print(f"Sending AT Command: {command.decode()}", flush=True)
        
        # Give more time for modem to respond
        time.sleep(2)
        
        # Read response
        response = ""
        while ser.in_waiting:
            response += ser.read().decode('utf-8', errors='ignore')
        
        print(f"AT Command Response: {response}", flush=True)  # Print the full response
        
        # Check response (case insensitive)
        if any(success.lower() in response.lower() for success in ["CONNECT OK", "ALREADY CONNECT"]):
            print("GSM Status: Connection successful!", flush=True)
            gsm_connection_status = True
            time.sleep(2)
        else:
            print("GSM Status: Connection failed!", flush=True)
            gsm_connection_status = False
            
    except Exception as e:
        print(f"GPRS Connection Error: {e}", flush=True)
        gsm_connection_status = False
    
    print(f"Final GSM status: {gsm_connection_status}", flush=True)  # Final status debug

async def setup_mqtt():
    global mqtt_client
    
    mqtt_client = MQTTClient(MQTT_CLIENT_ID)
    
    # Connect to the broker
    await mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    print(f"Connected to MQTT broker at {MQTT_BROKER}")

def publish_location():
    global current_latitude, current_longitude
    
    if mqtt_client and mqtt_client.is_connected:
        # For testing, using dummy location
        dummy_location = {
            "device_id": read_device_id(),
            "latitude": current_latitude,
            "longitude": current_longitude,
            "timestamp": time.time()
        }
        
        # Publish to MQTT topic
        mqtt_client.publish(MQTT_TOPIC, str(dummy_location))
        
        # Update the GPS status label with current coordinates
        update_gps_display()
    
    # Schedule next publication
    root.after(5000, publish_location)  # Publish every 5 seconds

def update_gps_display():
    current_time = time.strftime("%H:%M:%S")
    
    # Update main status text
    main_text = f"Jam: {current_time} | Lat: {current_latitude:.6f} | Lon: {current_longitude:.6f} | Status: Connected | GSM: "
    main_status_label.config(text=main_text)
    
    print(f"Current GSM status: {gsm_connection_status}")  # Debug print
    
    # Update GSM status with color based on stored status
    if gsm_connection_status:
        print("Setting status to Connected (Green)")  # Debug print
        gsm_status_label.config(
            text="Connected",
            fg="green"
        )
    else:
        print("Setting status to Not Connected (Red)")  # Debug print
        gsm_status_label.config(
            text="Not Connected",
            fg="red"
        )

# Buat class NumericKeypad
class NumericKeypad(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.result = ""
        
        # Konfigurasi window popup
        self.title("Enter Password")
        self.geometry("300x400")
        self.configure(bg='gray')
        
        # Entry widget untuk menampilkan input
        self.display = tk.Entry(self, show="*", font=('Arial', 20), justify='center')
        self.display.pack(pady=10, padx=10, fill='x')
        
        # Frame untuk tombol
        button_frame = tk.Frame(self, bg='gray')
        button_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Buat grid 3x4 untuk tombol
        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            'C', '0', '⏎'
        ]
        
        row = 0
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            btn = tk.Button(button_frame, text=button, font=('Arial', 18),
                          width=4, height=2, command=cmd)
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def click(self, key):
        if key == 'C':
            self.result = ""
            self.display.delete(0, tk.END)
        elif key == '⏎':
            if self.result == EXIT_PASSWORD:
                self.parent.quit()
            else:
                messagebox.showerror("Error", "Wrong Password!")
                self.result = ""
                self.display.delete(0, tk.END)
        else:
            self.result += key
            self.display.delete(0, tk.END)
            self.display.insert(0, self.result)

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
        with open('/home/pi/gps/mqtt/assets/current_location.txt', 'r') as file:
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
    main_status_label.config(
        text=f"Jam: {current_time} | GPS Lat: {gps_latitude} | GPS Lon: {gps_longitude} | Status: {connection_status} | GSM: "
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
        with open('/home/pi/gps/mqtt/assets/bustrack.txt', 'r') as file:
            for line in file:
                if line.startswith('DEVICEID='):
                    device_id = line.split('=')[1].strip()
                    return device_id
        return "N/A"  # Return N/A if DEVICEID line not found
    except Exception as e:
        print(f"Error reading device ID: {e}")
        return "N/A"

def check_gprs_connection():
    try:
        # Clear any existing data in the buffer
        ser.reset_input_buffer()
        
        # Send AT Command to check TCP connection
        ser.write(b'AT+CIPSTART="TCP","103.245.39.79","80"\r\n')
        
        # Wait for response with timeout
        start_time = time.time()
        response = ""
        
        while (time.time() - start_time) < 7:  # 7 second timeout
            if ser.in_waiting:
                response += ser.read_all().decode('utf-8', errors='ignore')
                # Check for both successful connection responses
                if any(success in response for success in ["CONNECT OK", "ALREADY CONNECT"]):
                    return True
                elif any(error in response for error in ["ERROR", "FAIL", "CLOSED"]):
                    return False
            time.sleep(0.1)
        
        # If we reach here, it means we timed out
        return False
        
    except Exception as e:
        print(f"GPRS Connection Error: {e}")
        return False

# Window Utama
root = tk.Tk()
root.title("Hello World GUI")
root.attributes('-fullscreen', True)
root.resizable(False, False)

# Variabel untuk menghitung klik
click_count = 0
last_click_time = 0

# Fungsi untuk menangani klik di pojok kiri atas
def handle_click(event):
    global click_count, last_click_time
    current_time = time.time()
    
    # Cek apakah klik berada di area pojok kiri atas (50x50 pixel)
    if event.x <= 50 and event.y <= 50:
        # Reset counter jika waktu antara klik terlalu lama (lebih dari 1 detik)
        if current_time - last_click_time > 1:
            click_count = 1
        else:
            click_count += 1
        
        # Tampilkan keypad jika sudah 3 klik
        if click_count >= 3:
            NumericKeypad(root)
            click_count = 0  # Reset click count
            
        last_click_time = current_time

# Bind event klik ke seluruh window
root.bind('<Button-1>', handle_click)

# Optional: Tambahkan handler untuk tombol Escape jika ingin keluar dari fullscreen
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

def end_fullscreen(event=None):
    root.attributes("-fullscreen", False)

# Bind tombol Escape untuk keluar dari fullscreen
root.bind('<Escape>', end_fullscreen)

# Header dan Logo
header = tk.Frame(root, bg="blue", height=50)
header.pack(side="top", fill="x")
header_content = tk.Frame(header, bg="blue")
header_content.pack(side="top", fill="x", pady=10)

# Load logo left images
##left_logo = tk.PhotoImage(file=" /home/pi/gps/mqtt/assets/lego.png")  # Using forward slashes

# Increase subsample values to make the logo smaller (e.g., 4,4 or 6,6)
##left_logo = left_logo.subsample(14, 14)  # Try different values to get desired size

# Replace text labels with image labels
##tk.Label(header_content, image=left_logo, bg="blue").pack(side="left", padx=10)  # Reduced padding
tk.Label(header_content, text="Hello World Header", bg="blue", fg="white", font=("Arial", 24)).pack(side="left", expand=True)

# Important: Keep a reference to prevent garbage collection
##root.left_logo = left_logo

# Load logo right images
##right_logo = tk.PhotoImage(file="/home/pi/gps/mqtt/assets/lego.png")  # Using forward slashes

# Increase subsample values to make the logo smaller (e.g., 4,4 or 6,6)
##right_logo = right_logo.subsample(14, 14)  # Try different values to get desired size

# Replace text labels with image labels
##tk.Label(header_content, image=right_logo, bg="blue").pack(side="right", padx=10)  # Reduced padding

# Important: Keep a reference to prevent garbage collection
##root.right_logo = right_logo


# Status GPS dan Waktu
status_frame = tk.Frame(root, bg="lightgray")
status_frame.pack(side="top", fill="x")

main_status_label = tk.Label(status_frame, text="", bg="lightgray", font=("Arial", 16))
main_status_label.pack(side="left")

gsm_status_label = tk.Label(status_frame, text="Not Connected", bg="lightgray", fg="red", font=("Arial", 16))
gsm_status_label.pack(side="left")

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
route_data = load_route_data('/home/pi/gps/mqtt/assets/stopseq.txt')

# Setup MQTT connection
asyncio.get_event_loop().run_until_complete(setup_mqtt())

# Start publishing location
publish_location()

# Before root.mainloop()
print("Initializing GSM connection...", flush=True)
initialize_gsm_connection()
print("GSM initialization complete", flush=True)

root.mainloop()
