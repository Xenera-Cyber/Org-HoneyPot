import socket
import time

def read_until_prompt(conn):
    buffer = ""
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        buffer += data
        if buffer.strip().endswith("$") or buffer.strip().endswith("#"):
            break
        if "login:" in buffer or "Password:" in buffer:
            break
    return buffer

def main():
    print("=== Testing Live Honeypot with AI Deception Fallback ===")
    
    # Establish connection
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(("127.0.0.1", 2222))
    except Exception as e:
        print(f"Failed to connect to honeypot: {e}")
        return
        
    # Read welcome banner
    welcome = conn.recv(1024).decode()
    print(f"Received: {welcome.strip()}")
    
    # Read prompt
    prompt = read_until_prompt(conn)
    print(f"Prompt: {prompt.strip()}")
    
    # Run command: top (not locally handled, should go to AI)
    print("\nSending command: 'top'")
    conn.send(b"top\n")
    time.sleep(2.0)
    response_top = conn.recv(4096).decode()
    print(f"Response:\n{response_top}")
    
    # Run command: crontab -e (not locally handled, should go to AI)
    print("\nSending command: 'crontab -e'")
    conn.send(b"crontab -e\n")
    time.sleep(2.0)
    response_crontab = conn.recv(4096).decode()
    print(f"Response:\n{response_crontab}")
    
    # Exit
    conn.send(b"exit\n")
    conn.close()

if __name__ == "__main__":
    main()
