import socket
import time
import random # Datos aleatorios

DEST_IP = "127.0.0.1"
DEST_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Enviando métricas cada 1 segundo...")

try:
    while True:
        # Simulamos obtener datos del sistema
        cpu_usage = random.randint(10, 90)
        ram_usage = random.randint(30, 70)
        
        # Formateamos el mensaje: "CPU:XX%|RAM:XX%"
        mensaje = f"CPU:{cpu_usage}%|RAM:{ram_usage}%"
        
        # Enviamos sin esperar confirmación (Fuego y olvido)
        sock.sendto(mensaje.encode('utf-8'), (DEST_IP, DEST_PORT))
        
        print(f"Enviado: {mensaje}")
        time.sleep(1) # Esperamos un segundo para la siguiente lectura
        
except KeyboardInterrupt:
    print("\nSensor detenido.")
finally:
    sock.close()