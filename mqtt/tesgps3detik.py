import serial
import time
import sys

# Menyesuaikan port serial sesuai dengan Raspberry Pi Anda
port = '/dev/ttyAMA0'  # Gantilah dengan port yang sesuai
baudrate = 9600  # Sesuaikan dengan baud rate modem SIMCOM 808
timeout = 2  # Timeout untuk membaca respon

# Membuka koneksi serial
ser = serial.Serial(port, baudrate, timeout=timeout)

# Fungsi untuk mengirim perintah AT dan membaca respon
def send_at_command(command, delay=1):
    try:
        print(f"Kirim perintah: {command}")
        ser.write((command + '\r\n').encode())  # Mengirimkan perintah AT
        time.sleep(delay)  # Menunggu respon
        response = ser.read(ser.in_waiting).decode()  # Membaca respon dari modem
        return response
    except serial.SerialException as e:
        print(f"Error komunikasi serial: {e}")
        return None

# Fungsi untuk memparsing respon GPS
def parse_gps_response(response):
    try:
        parts = response.split(',')
        latitude = parts[2]
        longitude = parts[3]
        return latitude, longitude
    except IndexError:
        return None, None

# Inisialisasi GPS
def initialize_gps():
    commands = [
        'AT',                    # Test komunikasi
        'AT+CGPSPWR=1',         # Nyalakan GPS
        'AT+CGPSRST=0',         # Reset GPS dalam mode hot start
        'AT+CGPSSTATUS?'        # Cek status GPS
    ]
    
    for cmd in commands:
        response = send_at_command(cmd, delay=2)
        print(f"Response: {response}")
        if response and "ERROR" in response:
            print(f"Gagal menginisialisasi GPS pada command: {cmd}")
            return False
    return True

# Loop untuk mendapatkan lokasi GPS setiap 3 detik
try:
    # Verifikasi port terbuka
    if not ser.is_open:
        ser.open()
    
    # Inisialisasi GPS terlebih dahulu
    if not initialize_gps():
        print("Gagal menginisialisasi GPS")
        sys.exit(1)
        
    while True:
        response = send_at_command('AT+CGPSINFO')
        
        if response is None:
            print("Gagal berkomunikasi dengan modem. Mencoba ulang dalam 3 detik...")
            time.sleep(3)
            continue

        latitude, longitude = parse_gps_response(response)

        if latitude and longitude:
            print(f"Latitude: {latitude}, Longitude: {longitude}")
        else:
            print("GPS tidak ditemukan atau tidak valid.")

        # Tunggu 3 detik sebelum mengulangi
        time.sleep(3)

except serial.SerialException as e:
    print(f"Error pada port serial: {e}")
except KeyboardInterrupt:
    print("Pengambilan data dihentikan.")
finally:
    if ser.is_open:
        ser.close()
