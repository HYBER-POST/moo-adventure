import socket
from threading import Thread
import json
HOST, PORT = 'localhost', 8080
MAX_PLAYERS = 2

class Server:
    def __init__(self, addr, max_conn):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr)
        self.max_players = max_conn
        self.players = []
        self.sock.listen(self.max_players)
        self.listen()

    def listen(self):
        while True:
            if not len(self.players) >= self.max_players:
                conn, addr = self.sock.accept()
                print("Новое подключение:", addr)
                Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):
        self.player = {
            "id": len(self.players),
            "x": 400,
            "y": 300
        }
        self.players.append(self.player)

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("Отключен")
                    break
                data = json.loads(data.decode('utf-8'))
                if data["request"] == "get_players":
                    conn.sendall(bytes(json.dumps({
                        "response": self.players
                    }), 'UTF-8'))
                if data["request"] == "move":
                    if data["move"] == "left":
                        self.player["x"] -= 5
                    if data["move"] == "right":
                        self.player["x"] += 5
                    if data["move"] == "up":
                        self.player["y"] -= 5
                    if data["move"] == "down":
                        self.player["y"] += 5
            except Exception as e:
                print(e)
                break
        self.players.remove(self.player)

if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)