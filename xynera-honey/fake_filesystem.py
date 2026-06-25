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
        "Documents",
        "Downloads",
        "projects",
        ".bash_history"
    ],

    "/home/ubuntu/Documents": [
        "employee_directory.csv",
        "meeting_notes.txt",
        "server_inventory.csv"
    ],

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

    "/etc/passwd": """
root:x:0:0:root:/root:/bin/bash
ubuntu:x:1000:1000::/home/ubuntu:/bin/bash
dev:x:1001:1001::/home/dev:/bin/bash
backup:x:1002:1002::/home/backup:/bin/bash
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
mysql:x:111:115:MySQL Server:/nonexistent:/bin/false
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
