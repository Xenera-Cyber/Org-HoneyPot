import random
import socket

# ==========================================================
# Consistent Server Identity
# ==========================================================
# These values are dynamically resolved to match the actual honeypot host.

def get_server_ip():
    """Resolve the actual IP of the honeypot listener dynamically."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.1.25"

def get_server_hostname():
    """Dynamically fetch the current hostname of the OS."""
    return socket.gethostname()

def get_server_broadcast():
    """Dynamically generate broadcast address based on the actual IP."""
    _ip_parts = get_server_ip().split(".")
    return f"{_ip_parts[0]}.{_ip_parts[1]}.{_ip_parts[2]}.255" if len(_ip_parts) == 4 else "192.168.1.255"

SERVER_NETMASK = "255.255.255.0"
SERVER_MAC = "08:00:27:4e:9a:2c"
SERVER_IPV6_LINK = "fe80::a00:27ff:fe4e:9a2c"

# Single source of truth for every listening service, shared by
# netstat(), netstat_tulpn(), ss() and service_manager.py so their
# output can never drift out of sync with each other.
# (proto, bind_address, port, pid, program)
SERVICES = [
    ("tcp", "0.0.0.0", 22, 221, "sshd"),
    ("tcp", "0.0.0.0", 80, 567, "nginx"),
    ("tcp", "0.0.0.0", 443, 567, "nginx"),
    ("tcp", "127.0.0.1", 3306, 334, "mysqld"),
    ("tcp", "127.0.0.1", 5432, 412, "postgres"),
    ("tcp", "127.0.0.1", 6379, 501, "redis-server"),
    ("tcp", "0.0.0.0", 2375, 812, "dockerd"),
    ("tcp", "0.0.0.0", 8080, 701, "jenkins"),
    ("tcp", "0.0.0.0", 9090, 801, "prometheus"),
]

# ==========================================================
# In-memory DNS Cache
# ==========================================================
# Guarantees that dig(), nslookup(), host(), and every command that
# accepts a hostname (ping, traceroute, ssh, scp, telnet, ftp) all
# agree on the same fake IP for the same domain for the life of the
# process, instead of re-randomizing it on every call.
_DNS_CACHE = {}


def _is_ipv4(value):
    """Return True if value already looks like a literal IPv4 address."""
    parts = value.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True


def _resolve_domain(domain):
    """Deterministically resolve (and cache) a fake IP for a domain name."""
    key = domain.lower().strip()
    
    # Sync hostname lookup with actual honeypot listener dynamically
    if key == get_server_hostname().lower():
        return get_server_ip()
    if key == "localhost":
        return "127.0.0.1"

    if key not in _DNS_CACHE:
        seeded = random.Random(key)
        _DNS_CACHE[key] = (
            f"10.{seeded.randint(0, 255)}."
            f"{seeded.randint(0, 255)}."
            f"{seeded.randint(2, 254)}"
        )
    return _DNS_CACHE[key]


def _resolve_target(host):
    """
    Return (display_name, ip_address) for any host argument passed to a
    network command. Literal IPs pass through unchanged; hostnames are
    resolved through the shared DNS cache so the same name always maps
    to the same address.
    """
    host = host.strip()
    if _is_ipv4(host):
        return host, host
    return host, _resolve_domain(host)


def _human_bytes(n):
    """Format a byte count the way ifconfig does, e.g. '184.2 MB'."""
    return f"{n / (1024 * 1024):.1f} MB"


def _active_services(service_manager=None):
    """
    Return the SERVICES entries that should currently appear as
    listening. When a session's ServiceManager is supplied, services the
    attacker has stopped are excluded so netstat/ss/netstat -tulpn always
    agree with `service <n> stop` / `systemctl stop <n>`. With no
    ServiceManager (e.g. calls made outside of a live session) every
    service is treated as running, matching the original static output.
    """
    if service_manager is None:
        return SERVICES
    return [
        entry for entry in SERVICES
        if service_manager.is_running_by_program(entry[4]) is not False
    ]

# ==========================================================
# Local Discovery Commands
# ==========================================================

def get_hostname(hostname=None):
    """Return the dynamically generated hostname for the session."""
    return get_server_hostname()

def netstat(service_manager=None):
    server_ip = get_server_ip()
    server_hostname = get_server_hostname()
    
    header = (
        "Active Internet connections (only servers)\n"
        f"{'Proto':<6}{'Recv-Q':>7} {'Send-Q':>7} "
        f"{'Local Address':<24}{'Foreign Address':<24}{'State'}"
    )
    lines = [header]

    for proto, addr, port, _pid, _prog in _active_services(service_manager):
        # Service information updated to reflect actual host binding
        display_addr = server_hostname if addr == "0.0.0.0" else addr
        local = f"{display_addr}:{port}"
        lines.append(
            f"{proto:<6}{'0':>7} {'0':>7} {local:<24}{'0.0.0.0:*':<24}LISTEN"
        )

    # A couple of realistic active connections so the table doesn't
    # look like a server nobody has ever connected to.
    peer_established = f"203.0.113.{random.randint(2, 254)}:{random.randint(1024, 65535)}"
    peer_time_wait = f"198.51.100.{random.randint(2, 254)}:{random.randint(1024, 65535)}"
    lines.append(
        f"{'tcp':<6}{'0':>7} {'0':>7} {server_hostname + ':22':<24}{peer_established:<24}ESTABLISHED"
    )
    lines.append(
        f"{'tcp':<6}{'0':>7} {'0':>7} {server_hostname + ':80':<24}{peer_time_wait:<24}TIME_WAIT"
    )

    return "\n".join(lines) + "\n"


def netstat_tulpn(service_manager=None):
    server_hostname = get_server_hostname()
    header = (
        "Active Internet connections (only servers)\n"
        f"{'Proto':<6}{'Recv-Q':>7} {'Send-Q':>7} "
        f"{'Local Address':<24}{'Foreign Address':<24}{'State':<12}{'PID/Program name'}"
    )
    lines = [header]

    for proto, addr, port, pid, prog in _active_services(service_manager):
        display_addr = server_hostname if addr == "0.0.0.0" else addr
        local = f"{display_addr}:{port}"
        lines.append(
            f"{proto:<6}{'0':>7} {'0':>7} {local:<24}{'0.0.0.0:*':<24}"
            f"{'LISTEN':<12}{pid}/{prog}"
        )

    return "\n".join(lines) + "\n"


def ss(service_manager=None):
    server_hostname = get_server_hostname()
    header = (
        f"{'Netid':<6}{'State':<12}{'Recv-Q':>7} {'Send-Q':>7}   "
        f"{'Local Address:Port':<26}{'Peer Address:Port'}"
    )
    lines = [header]

    for proto, addr, port, _pid, _prog in _active_services(service_manager):
        display_addr = server_hostname if addr == "0.0.0.0" else addr
        local = f"{display_addr}:{port}"
        lines.append(
            f"{proto:<6}{'LISTEN':<12}{'0':>7} {'128':>7}   {local:<26}{'0.0.0.0:*'}"
        )

    peer = f"203.0.113.{random.randint(2, 254)}:{random.randint(1024, 65535)}"
    lines.append(
        f"{'tcp':<6}{'ESTAB':<12}{'0':>7} {'0':>7}   "
        f"{server_hostname + ':22':<26}{peer}"
    )

    return "\n".join(lines) + "\n"

def ifconfig(ip=None):
    """Ubuntu 22.04 (net-tools) style interface listing for eth0 and lo."""
    server_ip = get_server_ip()
    server_broadcast = get_server_broadcast()
    
    rx_packets = random.randint(80000, 200000)
    tx_packets = random.randint(60000, 150000)
    rx_bytes = rx_packets * random.randint(120, 900)
    tx_bytes = tx_packets * random.randint(100, 800)

    return f"""eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet {server_ip}  netmask {SERVER_NETMASK}  broadcast {server_broadcast}
        inet6 {SERVER_IPV6_LINK}  prefixlen 64  scopeid 0x20<link>
        ether {SERVER_MAC}  txqueuelen 1000  (Ethernet)
        RX packets {rx_packets}  bytes {rx_bytes} ({_human_bytes(rx_bytes)})
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets {tx_packets}  bytes {tx_bytes} ({_human_bytes(tx_bytes)})
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 1284  bytes 103482 (103.4 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1284  bytes 103482 (103.4 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
"""


def ip_addr(ip=None):
    """Ubuntu `ip addr` style listing for lo and eth0, matching ifconfig()."""
    server_ip = get_server_ip()
    server_broadcast = get_server_broadcast()
    
    return f"""1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether {SERVER_MAC} brd ff:ff:ff:ff:ff:ff
    inet {server_ip}/24 brd {server_broadcast} scope global dynamic eth0
       valid_lft 86058sec preferred_lft 86058sec
    inet6 {SERVER_IPV6_LINK}/64 scope link
       valid_lft forever preferred_lft forever
"""

# ==========================================================
# Outbound / Lateral-Movement Commands
# ==========================================================
def ssh(host="192.168.1.10", user="root", port=22):
    """Simulate a failed SSH lateral-movement attempt."""
    display, ip = _resolve_target(host)

    # A minority of attempts fail at the transport level, before any
    # banner is ever seen.
    outcome = random.random()
    if outcome < 0.10:
        return f"ssh: connect to host {ip} port {port}: Connection refused\n"
    if outcome < 0.18:
        return f"ssh: connect to host {ip} port {port}: Connection timed out\n"
    if outcome < 0.24:
        return f"ssh: connect to host {ip} port {port}: No route to host\n"

    lines = [
        "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6",
        f"Warning: Permanently added '{display}' (ED25519) to the list of known hosts.",
        f"{user}@{display}'s password:",
        "Permission denied, please try again.",
        f"{user}@{display}'s password:",
        "Permission denied, please try again.",
        f"{user}@{display}'s password:",
        f"{user}@{display}: Permission denied (publickey,password).",
    ]
    return "\n".join(lines) + "\n"


def scp(host="192.168.1.10", user="root", filename="file.txt"):
    """Simulate a failed outbound SCP transfer over the same broken SSH path."""
    display, ip = _resolve_target(host)
    responses = [
        f"ssh: connect to host {ip} port 22: Connection refused\nlost connection",
        f"ssh: connect to host {ip} port 22: Connection timed out\nlost connection",
        f"ssh: connect to host {ip} port 22: No route to host\nlost connection",
        f"{user}@{display}: Permission denied (publickey,password).\nlost connection",
    ]
    return random.choice(responses)


def ping(host="192.168.1.10", count=3):
    """Simulate a ping sweep with randomized latency/loss."""
    if not host or " " in host:
        return f"ping: {host}: Name or service not known\n"

    count = max(1, count)
    display, ip = _resolve_target(host)

    # Weighted towards success, occasional partial/total loss.
    loss = random.choice([0, 0, 0, 25, 50, 100])
    received = round(count * (100 - loss) / 100)

    lines = [f"PING {display} ({ip}) 56(84) bytes of data."]
    for seq in range(1, received + 1):
        latency = round(random.uniform(0.3, 4.5), 3)
        lines.append(f"64 bytes from {ip}: icmp_seq={seq} ttl=64 time={latency} ms")

    lines.append(f"--- {display} ping statistics ---")
    lines.append(
        f"{count} packets transmitted, {received} received, {loss}% packet loss, "
        f"time {random.randint(2000, 2100)}ms"
    )
    return "\n".join(lines) + "\n"


def traceroute(host="192.168.1.10"):
    """Simulate a traceroute with realistic hop progression and jitter."""
    display, ip = _resolve_target(host)

    total_hops = random.randint(4, 8)
    reaches_destination = random.random() < 0.6

    lines = [f"traceroute to {display} ({ip}), 30 hops max, 60 byte packets"]
    for hop in range(1, total_hops + 1):
        if random.random() < 0.15:
            lines.append(f" {hop}  * * *")
            continue

        is_final_hop = hop == total_hops and reaches_destination
        hop_ip = ip if is_final_hop else f"10.0.{random.randint(0, 254)}.{random.randint(1, 254)}"
        t1 = round(random.uniform(0.3, 40.0), 3)
        t2 = round(random.uniform(0.3, 40.0), 3)
        t3 = round(random.uniform(0.3, 40.0), 3)
        lines.append(f" {hop}  {hop_ip}  {t1} ms  {t2} ms  {t3} ms")

    if not reaches_destination:
        lines.append(f" {total_hops + 1}  * * *")

    return "\n".join(lines) + "\n"


def telnet(host="192.168.1.10", port=23):
    """Simulate a telnet session that varies between refusal and a login banner."""
    display, ip = _resolve_target(host)
    server_hostname = get_server_hostname()

    outcome = random.random()
    if outcome < 0.4:
        return f"Trying {ip}...\ntelnet: connect to address {ip}: Connection refused"
    if outcome < 0.7:
        return f"Trying {ip}...\ntelnet: connect to address {ip}: Connection timed out"

    return (
        f"Trying {ip}...\n"
        f"Connected to {display}.\n"
        "Escape character is '^]'.\n"
        "\n"
        f"Ubuntu 22.04.3 LTS\n"
        f"{server_hostname} login: "
    )


def ftp(host="192.168.1.10"):
    """Simulate an FTP connection attempt, occasionally reaching a login prompt."""
    display, ip = _resolve_target(host)
    server_hostname = get_server_hostname()

    outcome = random.random()
    if outcome < 0.45:
        return "ftp: connect: Connection refused"
    if outcome < 0.70:
        return "ftp: connect: Connection timed out"
    if outcome < 0.85:
        return "421 Service not available, closing control connection."

    return (
        f"Connected to {display}.\n"
        f"220 {server_hostname} FTP server (vsFTPd 3.0.5) ready.\n"
        "Name (root): root\n"
        "331 Please specify the password.\n"
        "Password:\n"
        "530 Login incorrect.\n"
        "Login failed."
    )

# ==========================================================
# DNS Commands
# ==========================================================
def dig(domain="example.com"):
    """Simulate a dig DNS lookup, always resolving a domain to the same IP."""
    ip = _resolve_domain(domain)
    return f""";<<>> DiG 9.18.1-1ubuntu1.2-Ubuntu <<>> {domain}
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: {random.randint(1000, 65000)}
;; QUESTION SECTION:
;{domain}.            IN    A

;; ANSWER SECTION:
{domain}.        300    IN    A    {ip}

;; Query time: {random.randint(10, 80)} msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
"""


def nslookup(domain="example.com"):
    """Simulate an nslookup DNS query, occasionally returning NXDOMAIN."""
    if random.choice([True, False]):
        ip = _resolve_domain(domain)
        return f"""Server:  127.0.0.53
Address: 127.0.0.53#53

Non-authoritative answer:
Name:    {domain}
Address: {ip}
"""
    return f"""Server:  127.0.0.53
Address: 127.0.0.53#53

** server can't find {domain}: NXDOMAIN
"""


def host(domain="example.com"):
    """Simulate the `host` DNS lookup utility, occasionally failing."""
    if random.choice([True, False]):
        ip = _resolve_domain(domain)
        return f"{domain} has address {ip}"
    return f"Host {domain} not found: 3(NXDOMAIN)"