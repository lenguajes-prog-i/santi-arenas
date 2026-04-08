import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Escuchando telemetría en {UDP_IP}:{UDP_PORT}...")

try:
    while True:
        # Paquetes recibidos
        data, addr = sock.recvfrom(1024)
        print(f"[MÉTRICA RECIBIDA de {addr}]: {data.decode('utf-8')}")
except KeyboardInterrupt:
    print("\nDeteniendo monitor...")
finally:
    sock.close()