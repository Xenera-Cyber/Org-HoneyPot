import random


def netstat():
    return """Active Internet connections (only servers)
Proto Local Address State
tcp 0.0.0.0:22 LISTEN
tcp 0.0.0.0:80 LISTEN
tcp 0.0.0.0:443 LISTEN
tcp 127.0.0.1:3306 LISTEN
tcp 127.0.0.1:5432 LISTEN
tcp 127.0.0.1:6379 LISTEN
tcp 0.0.0.0:8080 LISTEN
tcp 0.0.0.0:9090 LISTEN
"""


def netstat_tulpn():
    return """Proto Local Address PID/Program name
tcp 0.0.0.0:22 221/sshd
tcp 0.0.0.0:80 567/nginx
tcp 0.0.0.0:443 567/nginx
tcp 127.0.0.1:3306 334/mysqld
tcp 127.0.0.1:5432 412/postgres
tcp 127.0.0.1:6379 501/redis-server
tcp 0.0.0.0:8080 701/jenkins
tcp 0.0.0.0:9090 801/prometheus
"""


def ss():
    return """Netid State Local Address:Port
tcp LISTEN 0.0.0.0:22
tcp LISTEN 0.0.0.0:80
tcp LISTEN 0.0.0.0:443
tcp LISTEN 127.0.0.1:3306
tcp LISTEN 127.0.0.1:5432
tcp LISTEN 127.0.0.1:6379
tcp LISTEN 0.0.0.0:8080
tcp LISTEN 0.0.0.0:9090
"""


def ifconfig():
    return """eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>
inet 192.168.1.25
netmask 255.255.255.0
broadcast 192.168.1.255
"""


def ip_addr():
    return """2: eth0:
 inet 192.168.1.25/24
 brd 192.168.1.255
"""


def ssh(host="192.168.1.10", user="root"):
    """Simulate a failed SSH lateral-movement attempt."""
    responses = [
        "Permission denied, please try again.",
        "Authentication failed.",
        "Connection refused.",
        "Host unreachable.",
    ]
    msg = random.choice(responses)
    return f"""SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6
Warning: Permanently added '{host}' (ED25519) to the list of known hosts.
{user}@{host}'s password:
{msg}
{user}@{host}'s password:
{msg}
{user}@{host}'s password:
{user}@{host}: Permission denied (publickey,password).
"""


def ping(host="192.168.1.10"):
    """Simulate a ping sweep with randomized latency/loss."""
    t1 = round(random.uniform(0.5, 9.9), 3)
    t2 = round(random.uniform(0.5, 9.9), 3)
    t3 = round(random.uniform(0.5, 9.9), 3)
    loss = random.choice([0, 33, 66, 100])
    received = 3 - loss // 33
    return f"""PING {host} ({host}) 56(84) bytes of data.
64 bytes from {host}: icmp_seq=1 ttl=64 time={t1} ms
64 bytes from {host}: icmp_seq=2 ttl=64 time={t2} ms
64 bytes from {host}: icmp_seq=3 ttl=64 time={t3} ms
--- {host} ping statistics ---
3 packets transmitted, {received} received, {loss}% packet loss
"""


def traceroute(host="192.168.1.10"):
    """Simulate a traceroute that dead-ends before reaching the target."""
    hops = random.randint(3, 6)
    route = ""
    for i in range(1, hops):
        t = round(random.uniform(1.0, 50.0), 3)
        route += f"{i}  192.168.1.{random.randint(1, 254)}  {t} ms\n"
    return f"""traceroute to {host} ({host}), 30 hops max
{route}{hops}  {host}  No route to host
"""


def telnet(host="192.168.1.10", port=23):
    """Simulate a refused/timed-out telnet connection."""
    responses = [
        f"Trying {host}...\ntelnet: connect to address {host}: Connection refused",
        f"Trying {host}...\ntelnet: connect to address {host}: Connection timed out",
        f"Trying {host}...\ntelnet: connect to address {host}: No route to host",
    ]
    return random.choice(responses)


def ftp(host="192.168.1.10"):
    """Simulate a refused/unavailable FTP connection."""
    responses = [
        "ftp: connect: Connection refused",
        "ftp: connect: Connection timed out",
        "421 Service not available, closing control connection.",
    ]
    return random.choice(responses)


def dig(domain="example.com"):
    """Simulate a dig DNS lookup response."""
    ip = f"192.168.1.{random.randint(2, 254)}"
    return f""";<<>> DiG 9.18.1 <<>> {domain}
;; ANSWER SECTION:
{domain}.        300    IN    A    {ip}
;; Query time: {random.randint(10, 80)} msec
"""


def nslookup(domain="example.com"):
    """Simulate an nslookup DNS query, occasionally returning NXDOMAIN."""
    if random.choice([True, False]):
        ip = f"192.168.1.{random.randint(2, 254)}"
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
        ip = f"192.168.1.{random.randint(2, 254)}"
        return f"{domain} has address {ip}"
    return f"Host {domain} not found: 3(NXDOMAIN)"