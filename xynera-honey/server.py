import socket

from command_router import route_command

from session_manager import SessionManager

from attack_analyzer import (
    classify,
    threat_score
)

from logger import log_command
import malware_detector

HOST = "0.0.0.0"
PORT = 2222


def start_server():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(
        (HOST, PORT)
    )

    server.listen(5)

    print(
        f"[+] Listening on {HOST}:{PORT}"
    )

    while True:

        conn, addr = server.accept()

        attacker_ip = addr[0]

        print(
            f"[+] Connection from "
            f"{attacker_ip}"
        )

        session_manager = SessionManager(
            attacker_ip
        )

        session = (
            session_manager
            .get_session()
        )

        conn.send(
            b"Welcome to XYNERA Honeypot\n"
        )

        try:

            while True:

                current_dir = (
                    session_manager
                    .get_cwd()
                )

                prompt = (
                    f"ubuntu@web-prod-01:"
                    f"{current_dir}$ "
                )

                conn.send(
                    prompt.encode()
                )

                data = conn.recv(
                    1024
                )

                if not data:
                    break

                command = (
                    data.decode()
                    .strip()
                )

                if command.lower() == "exit":

                    conn.send(
                        b"logout\n"
                    )

                    break

                # ---------------------
                # Session Tracking
                # ---------------------

                session_manager.add_command(
                    command
                )

                # ---------------------
                # Attack Analysis
                # ---------------------

                attack_type = classify(
                    command
                )

                session_manager.add_attack_type(
                    attack_type
                )

                score = threat_score(
                    attack_type
                )

                session_manager.update_threat_score(
                    score
                )

                # ---------------------
                # Logging
                # ---------------------

                log_command(
                    command=command,
                    attack_type=attack_type,
                    ip_address=attacker_ip,
                    session_id=session[
                        "session_id"
                    ]
                )

                # ---------------------
                # Console Monitoring
                # ---------------------

                print(
                    f"[COMMAND] "
                    f"{command}"
                )

                print(
                    f"[ATTACK] "
                    f"{attack_type}"
                )

                print(
                    f"[THREAT SCORE] "
                    f"{session['threat_score']}"
                )

                # ---------------------
                # Route Command
                # ---------------------

                response = route_command(
                    command,
                    session_manager
                )

                conn.send(
                    (
                        response + "\n"
                    ).encode()
                )

        except Exception as e:

            print(
                f"[ERROR] {e}"
            )

        finally:

            session_manager.close_session()

            print(
                "\n========== "
                "SESSION SUMMARY "
                "=========="
            )

            print(
                session_manager.summary()
            )

            print(
                "=============================\n"
            )

            conn.close()

            print(
                f"[-] "
                f"{attacker_ip} "
                f"disconnected"
            )


if __name__ == "__main__":

    start_server()
