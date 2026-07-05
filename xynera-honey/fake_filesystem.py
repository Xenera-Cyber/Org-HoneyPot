filesystem = {
    "/": [
        "bin",
        "boot",
        "dev",
        "etc",
        "home",
        "opt",
        "tmp",
        "usr",
        "var"
    ],
    "/home": [
        "ubuntu",
        "dev",
        "backup"
    ],
    "/home/ubuntu": [
        "Desktop",
        "Documents",
        "Downloads",
        "Music",
        "Pictures",
        "Videos",
        "projects",
        ".ssh",
        ".config",
        ".cache",
        ".bash_history",
        ".bashrc",
        ".profile"
    ],
    "/home/ubuntu/Desktop": [
        "todo.txt"
    ],
    "/home/ubuntu/Documents": [
        "employee_directory.csv",
        "meeting_notes.txt",
        "server_inventory.csv"
    ],
    "/home/ubuntu/Downloads": [
        "ubuntu_server_notes.pdf",
        "backup.zip"
    ],
    "/home/ubuntu/Music": [],
    "/home/ubuntu/Pictures": [
        "office.jpg"
    ],
    "/home/ubuntu/Videos": [],
    "/home/ubuntu/.ssh": [
        "authorized_keys",
        "id_rsa.pub"
    ],
    "/home/ubuntu/.config": [
        "user-dirs.dirs"
    ],
    "/home/ubuntu/.cache": [],
    "/etc": [
        "passwd",
        "hosts",
        "hostname"
    ],
    "/var": [
        "log",
        "www"
    ],
    "/var/log": [
        "auth.log",
        "syslog"
    ],
    "/opt": [
        "backups"
    ],
    "/opt/backups": [
        "db_backup.sql",
        "weekly_backup.tar.gz"
    ]
}

file_contents = {
    "/home/ubuntu/Desktop/todo.txt": """
- Patch nginx
- Review firewall rules
- Rotate SSH keys
""",

    "/home/ubuntu/Documents/employee_directory.csv": """
ID,Name,Department,Email
1001,Alice Johnson,Finance,alice.johnson@xynera.local
1002,John Smith,IT,john.smith@xynera.local
1003,Sarah Davis,Operations,sarah.davis@xynera.local
1004,Michael Brown,HR,michael.brown@xynera.local
1005,Emma Wilson,Engineering,emma.wilson@xynera.local
""",

    "/home/ubuntu/Documents/meeting_notes.txt": """
Infrastructure Weekly Review
- nginx upgrade planned next month
- verify backup integrity
- review SSL renewal process
- monitor database replication
""",

    "/home/ubuntu/Documents/server_inventory.csv": """
Hostname,Role,Location
web-prod-01,Web Server,Delhi
db-prod-01,Database Server,Delhi
backup-01,Backup Node,Mumbai
""",

    "/home/ubuntu/.bash_history": """
apt update
apt upgrade -y
systemctl restart nginx
nano /etc/nginx/nginx.conf
tail -f /var/log/auth.log
mysql -u root
""",

    "/home/ubuntu/.bashrc": """
# ~/.bashrc
export PATH=$PATH:/usr/local/bin
alias ll='ls -la'
alias grep='grep --color=auto'
""",

    "/home/ubuntu/.profile": """
# ~/.profile
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi
""",

    "/home/ubuntu/.ssh/authorized_keys": """
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxxxxxxxxxxxxxxxxxxxxxxxx ubuntu@web-prod-01
""",

    "/home/ubuntu/.ssh/id_rsa.pub": """
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCyyyyyyyyyyyyyyyyyyyyyyyy ubuntu@web-prod-01
""",

    "/home/ubuntu/.config/user-dirs.dirs": """
XDG_DESKTOP_DIR="$HOME/Desktop"
XDG_DOWNLOAD_DIR="$HOME/Downloads"
XDG_DOCUMENTS_DIR="$HOME/Documents"
""",

    "/etc/passwd": """
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug Reporting:/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:Systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:101:103:Systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:102:106:D-Bus Message Bus:/nonexistent:/usr/sbin/nologin
syslog:x:103:110:Syslog:/home/syslog:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
uuidd:x:105:111:UUID Daemon:/run/uuidd:/usr/sbin/nologin
tcpdump:x:106:112::/nonexistent:/usr/sbin/nologin
tss:x:107:113:TPM Software Stack:/var/lib/tpm:/bin/false
landscape:x:108:114:Landscape Client:/var/lib/landscape:/usr/sbin/nologin
pollinate:x:109:1:Pollinate:/var/cache/pollinate:/bin/false
mysql:x:110:115:MySQL Server:/nonexistent:/bin/false
postgres:x:111:116:PostgreSQL Administrator:/var/lib/postgresql:/bin/bash
redis:x:112:117:Redis Server:/var/lib/redis:/usr/sbin/nologin
docker:x:113:118:Docker Engine:/var/lib/docker:/usr/sbin/nologin
nginx:x:114:119:Nginx Service:/var/cache/nginx:/usr/sbin/nologin
ubuntu:x:1000:1000:Ubuntu User:/home/ubuntu:/bin/bash
dev:x:1001:1001:Developer:/home/dev:/bin/bash
admin:x:1002:1002:System Administrator:/home/admin:/bin/bash
support:x:1003:1003:Support Engineer:/home/support:/bin/bash
backupuser:x:1004:1004:Backup Operator:/home/backupuser:/bin/bash
""",

    "/etc/hosts": """
127.0.0.1 localhost
127.0.1.1 web-prod-01
10.0.0.10 db-prod-01
10.0.0.11 backup-01
""",

    "/etc/hostname": """
web-prod-01
""",

    "/var/log/auth.log": """
Jun 15 08:01:22 sshd[2211]: Accepted password for ubuntu
Jun 15 08:15:13 sshd[2214]: Accepted password for dev
Jun 15 09:01:55 CRON[1001]: Job Started
""",

    "/var/log/syslog": """
Jun 15 nginx restarted
Jun 15 mysql service started
Jun 15 backup completed successfully
""",

    "/opt/backups/db_backup.sql": """
CREATE DATABASE customers;
USE customers;
CREATE TABLE users(
 id INT PRIMARY KEY,
 name VARCHAR(100),
 email VARCHAR(100)
);
"""
}