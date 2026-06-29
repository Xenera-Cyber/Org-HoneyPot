def netstat():
    return """Active Internet connections (only servers)

Proto Local Address         State
tcp   0.0.0.0:22            LISTEN
tcp   0.0.0.0:80            LISTEN
tcp   0.0.0.0:443           LISTEN
tcp   127.0.0.1:3306        LISTEN
tcp   127.0.0.1:5432        LISTEN
tcp   127.0.0.1:6379        LISTEN
tcp   0.0.0.0:8080          LISTEN
tcp   0.0.0.0:9090          LISTEN
"""


def netstat_tulpn():
    return """Proto Local Address      PID/Program name
tcp   0.0.0.0:22           221/sshd
tcp   0.0.0.0:80           567/nginx
tcp   0.0.0.0:443          567/nginx
tcp   127.0.0.1:3306       334/mysqld
tcp   127.0.0.1:5432       412/postgres
tcp   127.0.0.1:6379       501/redis-server
tcp   0.0.0.0:8080         701/jenkins
tcp   0.0.0.0:9090         801/prometheus
"""


def ss():
    return """Netid State  Local Address:Port

tcp   LISTEN 0.0.0.0:22
tcp   LISTEN 0.0.0.0:80
tcp   LISTEN 0.0.0.0:443
tcp   LISTEN 127.0.0.1:3306
tcp   LISTEN 127.0.0.1:5432
tcp   LISTEN 127.0.0.1:6379
tcp   LISTEN 0.0.0.0:8080
tcp   LISTEN 0.0.0.0:9090
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
    return f"""SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6
Warning: Permanently added '{host}' (ED25519) to the list of known hosts.
{user}@{host}'s password: 
Permission denied, please try again.
{user}@{host}'s password: 
Permission denied, please try again.
{user}@{host}'s password: 
{user}@{host}: Permission denied (publickey,password).
"""
