import socket
import threading

from session_manager import create_session, get_session, add_command
from command_router import route_command

HOST = "0.0.0.0"
PORT = 2222


def handle_client(conn, addr):
    ip = addr[0]
    print(f"[+] Connection from {ip}")

    session_id = create_session(ip)
    session = get_session(session_id)

    try:
        # banner
        conn.send(b"Welcome to Ubuntu 22.04.3 LTS\n")
        conn.send(b"Last login: Tue Mar 17 10:22:11 2026\n")

        while True:
            prompt = f"ubuntu@server:{session['cwd']}$ "
            conn.send(prompt.encode())

            data = conn.recv(1024)
            if not data:
                break

            command = data.decode().strip()
            print(f"[{ip}] {command}")

            # exit
            if command.lower() in ["exit", "quit"]:
                conn.send(b"logout\n")
                break

            # store command
            add_command(session_id, command)

            # history log (ASCII only)
            history = session["commands"][-5:]
            print(f"[HISTORY] {ip} -> {history}")

            # 🔥 route command (correct way)
            response, attack_type = route_command(command, session)

            # log attack
            print(f"[ATTACK] {ip} -> {attack_type}")

            # send response safely
            if response:
                formatted = response.replace("\n", "\r\n")
                conn.send((formatted + "\r\n").encode())
            else:
                conn.send(b"\r\n")

    except Exception as e:
        print(f"[!] Error: {e}")

    finally:
        conn.close()
        print(f"[-] Disconnected {ip}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[+] Honeypot running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    start_server()
