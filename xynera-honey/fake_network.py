def netstat():
    return """Active Internet connections (only servers)
Proto Local Address           State
tcp   0.0.0.0:22              LISTEN
tcp   0.0.0.0:80              LISTEN
tcp   127.0.0.1:3306          LISTEN"""


def ss():
    return """Netid State  Local Address:Port
tcp   LISTEN 0.0.0.0:22
tcp   LISTEN 0.0.0.0:80
tcp   LISTEN 127.0.0.1:3306"""
