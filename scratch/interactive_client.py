import socket
import sys
import threading
import time

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            sys.stdout.write(data.decode())
            sys.stdout.flush()
        except Exception:
            break

def main():
    host = "127.0.0.10"
    port = 2222
    print(f"[*] Connecting to XYNERA Honeypot at {host}:{port}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        # Start receiver thread
        t = threading.Thread(target=receive_messages, args=(s,), daemon=True)
        t.start()
        
        time.sleep(0.1) # Wait for initial welcome message
        
        while True:
            cmd = input()
            s.sendall(f"{cmd}\n".encode())
            if cmd.strip().lower() == "exit":
                time.sleep(0.2)
                break
    except KeyboardInterrupt:
        print("\n[*] Disconnecting...")
    except Exception as e:
        print(f"[-] Connection Error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    main()
