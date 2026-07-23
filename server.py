import socket
from datetime import datetime

from command_router import route_command
from session_manager import SessionManager
from attack_analyzer import classify, threat_score
from logger import log_command
import fake_network  # Import your dynamic network logic
import fake_process  # Added for dynamic process synchronization
import shlex         # Added for Task 4: advanced parsing
import re            # Added for Task 4: redirection parsing

HOST = "0.0.0.0"
PORT = 2222

USERNAME = "ubuntu"
HOME_DIR = "/home/ubuntu"

def format_prompt(path):
    """Convert the home directory to '~' like a real Linux shell."""
    if path == HOME_DIR:
        return "~"
    if path.startswith(HOME_DIR + "/"):
        return "~" + path[len(HOME_DIR):]
    return path

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[+] Listening on {HOST}:{PORT}")
    print(
        f"\n{'Timestamp':<22}"
        f"{'IP':<18}"
        f"{'Command':<22}"
        f"{'Attack Type':<28}"
        f"{'Score'}"
    )
    print("-" * 105)

    while True:
        conn, addr = server.accept()
        attacker_ip = addr[0]
        print(f"\n[+] Connection from {attacker_ip}")

        session_manager = SessionManager(attacker_ip)
        session = session_manager.get_session()
        conn.send(b"Welcome to XYNERA Honeypot\n")

        try:
            while True:
                # ----------------------------
                # Dynamic Terminal Prompt
                # ----------------------------
                current_dir = session_manager.get_cwd()
                display_dir = format_prompt(current_dir)
                
                # UPDATED: Fetch dynamic hostname directly from fake_network
                hostname = fake_network.get_hostname() 
                prompt = f"{USERNAME}@{hostname}:{display_dir}$ "
                conn.send(prompt.encode())

                data = conn.recv(1024)
                if not data:
                    break

                command = data.decode().strip()
                if not command:
                    conn.send(b"\n")
                    continue
                if command.lower() == "exit":
                    conn.send(b"logout\n")
                    break

                # ----------------------------
                # Task 4: Advanced Shell Parsing (Chained Commands & Redirection)
                # ----------------------------
                # Real bash splits commands by ';' and '&&'. 
                # This naive split prevents "command not found" errors when attackers chain commands.
                # Note: A full bash parser is complex, this handles the most common evasion checks.
                
                # Split commands safely using regex to preserve quoted strings
                raw_commands = re.split(r'\s*(&&|;)\s*(?=(?:[^"\']*["\'][^"\']*["\'])*[^"\']*$)', command)
                
                final_output = []
                abort_chain = False

                for i, cmd_part in enumerate(raw_commands):
                    if abort_chain:
                        break
                        
                    cmd_part = cmd_part.strip()
                    if not cmd_part:
                        continue
                        
                    if cmd_part == '&&':
                        continue # If the previous command succeeded, keep going
                    elif cmd_part == ';':
                        continue # Always keep going

                    # Handle Redirection (e.g., echo "test" > file.txt)
                    redirection_match = re.search(r'([>]{1,2})\s*([^\s]+)$', cmd_part)
                    redirect_target = None
                    is_append = False
                    
                    if redirection_match:
                        redirect_op = redirection_match.group(1)
                        redirect_target = redirection_match.group(2)
                        is_append = redirect_op == '>>'
                        # Strip the redirection part from the command before executing
                        cmd_part = cmd_part[:redirection_match.start()].strip()

                    # ----------------------------
                    # Session Tracking & Scoring
                    # ----------------------------
                    session_manager.add_command(cmd_part)
                    attack_type = classify(cmd_part)
                    session_manager.add_attack_type(attack_type)
                    session_manager.update_threat_score(attack_type)

                    # ----------------------------
                    # Logging
                    # ----------------------------
                    log_command(
                        command=cmd_part,
                        attack_type=attack_type,
                        ip_address=attacker_ip,
                        session_id=session["session_id"],
                    )
                    
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    score = threat_score(attack_type)
                    print(
                        f"{timestamp:<22}"
                        f"{attacker_ip:<18}"
                        f"{cmd_part:<22}"
                        f"{attack_type:<28}"
                        f"{score}"
                    )

                    # ----------------------------
                    # Execute Command
                    # ----------------------------
                    if cmd_part == "ifconfig":
                        response = fake_network.ifconfig()
                    elif cmd_part in ["ip addr", "ip a"]:
                        response = fake_network.ip_addr()
                    elif cmd_part == "hostname":
                        response = fake_network.get_hostname()
                    elif cmd_part == "ps":
                        response = fake_process.ps(session_manager)
                    elif cmd_part in ["ps aux", "ps -aux"]:
                        response = fake_process.ps_aux(session_manager)
                    else:
                        response = route_command(cmd_part, session_manager, attack_type)
                    
                    # Handle output routing based on redirection
                    if redirect_target:
                        # Ensure we don't accidentally write to the actual honeypot filesystem
                        # In a fully fleshed out simulated filesystem, we would call filesystem.touch/write here.
                        # For now, we simulate success by doing nothing and returning empty output.
                        response = "" 
                    
                    # Append output for this command in the chain
                    if response:
                        final_output.append(response)
                        
                    # Basic '&&' failure simulation. If a command returns a common error, 
                    # '&&' should abort the rest of the chain.
                    if "command not found" in response or "Permission denied" in response:
                        if i + 1 < len(raw_commands) and raw_commands[i+1].strip() == '&&':
                           abort_chain = True


                if final_output:
                    conn.send(("\n".join(final_output) + "\n").encode())
                else:
                    conn.send(b"\n") # Send empty newline if command produced no output (e.g., redirection)

        except Exception as e:
            print(f"[ERROR] {attacker_ip}: {e}")
        finally:
            session_manager.close_session()
            print("\n========== SESSION SUMMARY ==========")
            summary = session_manager.summary()
            print(f"Session ID        : {summary['session_id']}")
            print(f"Attacker IP       : {summary['attacker_ip']}")
            print(f"Commands Executed : {summary['commands_executed']}")
            print(f"Attack Types      : {summary['attack_types']}")
            print(f"Threat Score      : {summary['threat_score']}")
            if "current_directory" in summary:
                print(f"Last Directory    : {summary['current_directory']}")
            print("=====================================\n")
            conn.close()
            print(f"[-] {attacker_ip} disconnected")

if __name__ == "__main__":
    start_server()