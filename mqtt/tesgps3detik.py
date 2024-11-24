import serial
import time

def setup_serial(port="/dev/ttyAMA0", baudrate=9600):
    """Mengatur koneksi serial ke modul SIM808."""
    ser = serial.Serial(
        port=port,
        baudrate=baudrate,
        timeout=1,  # Timeout untuk membaca data
    )
    if ser.isOpen():
        print(f"Koneksi serial dibuka pada {port} dengan baud rate {baudrate}")
    return ser

def send_at_command(ser, command, delay=1):
    """Mengirim perintah AT dan membaca respons."""
    ser.write((command + "\r\n").encode())  # Kirim perintah dengan terminasi \r\n
    time.sleep(delay)  # Tunggu respons
    response = ser.readlines()
    return [line.decode().strip() for line in response]

def get_location(ser):
    """Mengambil data lokasi menggunakan AT+CGNSINF."""
    try:
        # Pastikan GNSS diaktifkan
        print("Mengaktifkan GNSS...")
        response = send_at_command(ser, "AT+CGNSPWR=1")
        if "OK" not in response:
            print("Gagal mengaktifkan GNSS")
            return None

        time.sleep(2)  # Tunggu GNSS untuk mulai mendapatkan data

        # Ambil informasi lokasi
        print("Mengambil data lokasi...")
        response = send_at_command(ser, "AT+CGNSINF", delay=2)
        for line in response:
            if "+CGNSINF" in line:
                data = line.split(",")
                if data[1] == "1":  # Pastikan GNSS aktif
                    latitude = data[3]
                    longitude = data[4]
                    print(f"Lokasi ditemukan: Latitude={latitude}, Longitude={longitude}")
                    return latitude, longitude
                else:
                    print("GNSS tidak aktif atau belum mendapatkan lokasi.")
        return None
    except Exception as e:
        print(f"Error saat mendapatkan lokasi: {e}")
        return None

def main():
    # Port serial tergantung perangkat Anda
    port = "/dev/ttyAMA0"
    baudrate = 9600

    while True:  # Loop utama
        try:
            ser = setup_serial(port, baudrate)
            
            # Tes komunikasi
            print("Mengirimkan perintah AT untuk tes koneksi...")
            response = send_at_command(ser, "AT")
            if "OK" not in response:
                print("Tidak ada respons dari modul. Memulai ulang...")
                time.sleep(3)
                continue

            # Perulangan untuk menampilkan lokasi
            while True:
                location = get_location(ser)
                if location:
                    print(f"Lokasi: Latitude={location[0]}, Longitude={location[1]}")
                else:
                    print("Gagal mendapatkan lokasi. Mencoba lagi...")
                time.sleep(3)  # Tunggu 3 detik sebelum mendapatkan lokasi lagi
        
        except Exception as e:
            print(f"Error: {e}. Mengulang kembali...")
            time.sleep(3)  # Tunggu sebelum mencoba ulang
        finally:
            if 'ser' in locals() and ser.isOpen():
                ser.close()
                print("Koneksi serial ditutup. Memulai ulang...")

if __name__ == "__main__":
    main()
