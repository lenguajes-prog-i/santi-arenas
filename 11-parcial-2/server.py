import socket
import threading
import pickle

class ChatServer:
    def __init__(self, host='192.168.1.226', port=5555):
        # Creación del socket TCP
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Enlace del servidor
        self.server.bind((host, port))
        self.server.listen()
        
        # Estructuras de datos
        self.clients = {}      # {socket: nickname}
        self.nicknames = {}    # {nickname: socket}
        self.client_room = {}
        self.rooms = {}
        
        # Lock para sincronización
        self.lock = threading.Lock()
        
        print(f"=== SERVIDOR ===\n[INFO] Servidor iniciado en {host}:{port}")

    def send_pickle(self, client, data):
        # Envía datos serializados
        try:
            client.send(pickle.dumps(data))
        except:
            self.remove_client(client)

    def broadcast(self, message, room, sender_socket=None):
        # Envía mensaje a todos en la sala excepto el emisor
        if room in self.rooms:
            for client in self.rooms[room]:
                if client != sender_socket:
                    self.send_pickle(client, message)

    def remove_client(self, client):
        # Elimina cliente de todas las estructuras
        with self.lock:
            nickname = self.clients.get(client, "Usuario desconocido")

            if client in self.client_room:
                room = self.client_room[client]
                if client in self.rooms.get(room, []):
                    self.rooms[room].remove(client)
                del self.client_room[client]

            if client in self.clients:
                nick = self.clients[client]
                del self.clients[client]
                if nick in self.nicknames:
                    del self.nicknames[nick]
        
        client.close()
        print(f"[-] {nickname} desconectado")

    def handle_client(self, client):
        # Manejo de cada cliente en un hilo
        try:
            # Solicita nickname
            client.send(pickle.dumps("NICKNAME_REQUEST"))
            nickname = pickle.loads(client.recv(1024)).strip()

            if not nickname:
                nickname = f"User_{client.getpeername()[1]}"

            # Guarda cliente
            with self.lock:
                self.clients[client] = nickname
                self.nicknames[nickname] = client

            print(f"[NUEVO] {nickname} se ha conectado.")

            while True:
                try:
                    msg = pickle.loads(client.recv(1024)).strip()
                except:
                    break

                if not msg:
                    break

                # ===== MENSAJE PRIVADO =====
                if msg.startswith("/pm"):
                    parts = msg.split(" ", 2)

                    if len(parts) < 3:
                        self.send_pickle(client, "Error: Uso /pm <nickname> <mensaje>")
                        continue

                    target_nick = parts[1]
                    message = parts[2]

                    with self.lock:
                        if target_nick not in self.nicknames:
                            self.send_pickle(client, "Error: Usuario no existe")
                            continue
                        target_client = self.nicknames[target_nick]

                    try:
                        self.send_pickle(target_client, f"[PM de {nickname}]: {message}")
                    except:
                        self.send_pickle(client, "Error: Cliente desconectado")

                # ===== SALAS =====
                elif msg.startswith("/join"):
                    parts = msg.split()

                    if len(parts) < 2:
                        self.send_pickle(client, "Error: Uso /join <sala>")

                    elif client in self.client_room:
                        self.send_pickle(client, "Error: Ya estás en una sala. Usa /leave.")

                    else:
                        room = parts[1]
                        
                        with self.lock:
                            self.client_room[client] = room
                            self.rooms.setdefault(room, []).append(client)

                        self.send_pickle(client, f"[INFO] Te has unido a '{room}'")
                        print(f"[+] {nickname} -> sala '{room}'")

                elif msg == "/leave":
                    if client in self.client_room:
                        with self.lock:
                            room = self.client_room.pop(client)
                            self.rooms[room].remove(client)

                        self.send_pickle(client, f"[INFO] Saliste de '{room}'")
                    else:
                        self.send_pickle(client, "Error: No estás en ninguna sala.")

                elif msg == "/rooms":
                    lista = ", ".join(self.rooms.keys()) if self.rooms else "Ninguna"
                    self.send_pickle(client, f"Salas: {lista}")

                elif msg.startswith("/msg"):
                    if client not in self.client_room:
                        self.send_pickle(client, "Error: Únete a una sala primero.")
                    else:
                        parts = msg.split(" ", 1)
                        if len(parts) > 1:
                            room = self.client_room[client]
                            self.broadcast(f"{nickname}: {parts[1]}", room, client)

                elif msg == "/quit":
                    break

                else:
                    self.send_pickle(client, "Error: Comando no válido.")

        except:
            pass
        finally:
            self.remove_client(client)

    def run(self):
        # Acepta clientes continuamente
        while True:
            client, addr = self.server.accept()
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

# Inicio del servidor
if __name__ == "__main__":
    ChatServer().run()