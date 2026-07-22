import socket
from datetime import datetime

import ai_client
from command_router import route_command
from session_manager import SessionManager
from attack_analyzer import classify, threat_score
from logger import log_command

HOST = "0.0.0.0"
PORT = 2222


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

    # ----------------------------------------------------------
    # AI Backend Health Check (startup)
    # ----------------------------------------------------------
    if not ai_client.check_ai_backend():
        print("[!] WARNING: AI backend unreachable at startup. Honeypot will run in local-only fallback mode.")

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
                # Terminal Prompt
                # ----------------------------
                # Built live from the session's identity (username/
                # hostname/cwd) — see session_manager.get_prompt(). Never
                # hardcode username/hostname here; that was the source of
                # the stale-identity bug this replaces.
                prompt = session_manager.get_prompt()
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
                # Session Tracking
                # ----------------------------
                session_manager.add_command(command)

                # ----------------------------
                # Attack Classification
                # ----------------------------
                attack_type = classify(command)
                session_manager.add_attack_type(attack_type)
                score = threat_score(attack_type)
                session_manager.update_threat_score(score)

                # ----------------------------
                # Logging
                # ----------------------------
                log_command(
                    command=command,
                    attack_type=attack_type,
                    ip_address=attacker_ip,
                    session_id=session["session_id"],
                )

                # ----------------------------
                # Live Monitoring
                # ----------------------------
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(
                    f"{timestamp:<22}"
                    f"{attacker_ip:<18}"
                    f"{command:<22}"
                    f"{attack_type:<28}"
                    f"{score}"
                )

                # ----------------------------
                # Execute Command
                # ----------------------------
                response = route_command(command, session_manager, attack_type)
                conn.send((response + "\n").encode())

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
            print(f"Identity          : {summary['username']}@{summary['hostname']} ({summary['personality']})")
            print("=====================================\n")
            conn.close()
            print(f"[-] {attacker_ip} disconnected")


if __name__ == "__main__":
    start_server()

