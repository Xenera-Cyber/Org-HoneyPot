"""
service_manager.py

Keeps track of which fake services (nginx, mysql, redis, ssh, docker) are
currently running or stopped, PER SESSION. When an attacker changes a
service's state (e.g. `service nginx stop`), that change is remembered
for the rest of their session, and reflected consistently in:
    - systemctl status <service>
    - systemctl (overview)
    - netstat / netstat -tulpn
    - ss

This is what makes the honeypot "dynamic" instead of always returning
the same fixed output no matter what the attacker has done.

Port/PID data is derived from fake_network.SERVICES (the single source
of truth for the simulated host's network topology) so this module can
never drift out of sync with what netstat/ss report.
"""

from fake_network import SERVICES

# Friendly service name -> the actual program name shown in netstat -tulpn
# and used as the lookup key into fake_network.SERVICES.
PROGRAM_NAME = {
    "nginx": "nginx",
    "mysql": "mysqld",
    "redis": "redis-server",
    "ssh": "sshd",
    "docker": "dockerd",
}


def _lookup_default(program):
    """Find the (port, pid) fake_network.SERVICES defines for a program."""
    for _proto, _addr, port, pid, prog in SERVICES:
        if prog == program:
            return port, pid
    return None, None


def _build_default_services():
    defaults = {}
    for name, program in PROGRAM_NAME.items():
        port, pid = _lookup_default(program)
        defaults[name] = {
            "port": port,
            "pid": pid,
            "status": "active (running)",
        }
    return defaults


# Default state of each fake service when a new session starts.
DEFAULT_SERVICES = _build_default_services()


class ServiceManager:
    """
    One ServiceManager belongs to exactly one attacker session.
    It stores the current running/stopped state of every fake service
    for that session, so all commands agree with each other.
    """

    def __init__(self):
        # Deep-copy the defaults so each session gets its own independent state
        self.services = {
            name: dict(info) for name, info in DEFAULT_SERVICES.items()
        }

    def _normalize(self, service):
        return service.strip().lower()

    def is_running(self, service):
        service = self._normalize(service)
        if service not in self.services:
            return None  # unknown service
        return self.services[service]["status"].startswith("active")

    def is_running_by_program(self, program):
        """
        Look up running state by the netstat/ss program name (e.g.
        "mysqld") rather than the friendly service name (e.g. "mysql").
        Returns None if the program isn't tracked by this ServiceManager
        (fake_network still reports it as always-on, e.g. jenkins/prometheus).
        """
        for name, info in self.services.items():
            if PROGRAM_NAME.get(name) == program:
                return info["status"].startswith("active")
        return None

    def start(self, service):
        service = self._normalize(service)
        if service not in self.services:
            return f"Unit {service}.service not found."
        self.services[service]["status"] = "active (running)"
        return f"{service} started."

    def stop(self, service):
        service = self._normalize(service)
        if service not in self.services:
            return f"Unit {service}.service not found."
        self.services[service]["status"] = "inactive (dead)"
        return f"{service} stopped."

    def restart(self, service):
        service = self._normalize(service)
        if service not in self.services:
            return f"Unit {service}.service not found."
        self.services[service]["status"] = "active (running)"
        return f"{service} restarted."

    # ------------------------------------------------------------------
    # Used by the `service <n> <start|stop|restart>` command
    # ------------------------------------------------------------------
    def handle_service_command(self, service, action):
        action = action.strip().lower()
        if action == "start":
            return self.start(service)
        elif action == "stop":
            return self.stop(service)
        elif action == "restart":
            return self.restart(service)
        else:
            return f"Usage: service {service} {{start|stop|restart}}"

    # ------------------------------------------------------------------
    # Used by `systemctl status <service>`
    # ------------------------------------------------------------------
    def systemctl_status(self, service):
        service = self._normalize(service)
        if service not in self.services:
            return f"Unit {service}.service could not be found."
        info = self.services[service]
        return (
            f"\u25cf {service}.service\n"
            f"   Active: {info['status']}\n"
        )

    # ------------------------------------------------------------------
    # Used by bare `systemctl` (overview of every tracked service)
    # ------------------------------------------------------------------
    def systemctl_overview(self):
        lines = []
        for name, info in self.services.items():
            state = "active" if info["status"].startswith("active") else "inactive"
            lines.append(f"{name}.service {state}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Used by `netstat` (basic) — only shows LISTEN lines for running services
    # ------------------------------------------------------------------
    def netstat_lines(self):
        lines = []
        for name, info in self.services.items():
            if info["status"].startswith("active"):
                lines.append(f"tcp 0.0.0.0:{info['port']} LISTEN")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Used by `netstat -tulpn` — shows LISTEN + PID/program, only for
    # currently running services
    # ------------------------------------------------------------------
    def netstat_tulpn_lines(self):
        lines = []
        for name, info in self.services.items():
            if info["status"].startswith("active"):
                program = PROGRAM_NAME.get(name, name)
                lines.append(f"tcp 0.0.0.0:{info['port']} {info['pid']}/{program}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Used by `ss` — same idea as netstat, different format
    # ------------------------------------------------------------------
    def ss_lines(self):
        lines = []
        for name, info in self.services.items():
            if info["status"].startswith("active"):
                lines.append(f"tcp LISTEN 0.0.0.0:{info['port']}")
        return "\n".join(lines)