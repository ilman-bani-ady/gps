import socket

def send_coordinates(lat, lon):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))
    client.send(f"{lat}, {lon}".encode())
    client.close()

# Example usage
#send_coordinates("106.817306", "-6.207741")

send_coordinates("106.832099", "-6.299146")