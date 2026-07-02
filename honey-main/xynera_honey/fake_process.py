def ps():
    return """  PID TTY          TIME CMD
 890 pts/0    00:00:00 bash
 912 pts/0    00:00:00 ps"""


def ps_aux():
    return """USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.2 168340  9612 ?        Ss   Jun15   0:04 /sbin/init
root           2  0.0  0.0      0     0 ?        S    Jun15   0:00 [kthreadd]
root           4  0.0  0.0      0     0 ?        I<   Jun15   0:00 [kworker/0:0H]
root          14  0.0  0.0      0     0 ?        I    Jun15   0:01 [rcu_sched]
root         221  0.0  0.2  72296  6120 ?        Ss   Jun15   0:00 /usr/sbin/sshd -D
root         289  0.0  0.1  31488  2890 ?        Ss   Jun15   0:00 /usr/sbin/cron -f
syslog       301  0.1  0.3 268912  8912 ?        Ssl  Jun15   0:12 /usr/sbin/rsyslogd -n
root         315  0.2  0.6 182100 12890 ?        Ssl  Jun15   0:24 /usr/bin/python3 /usr/bin/fail2ban-server
mysql        334  0.4  3.2 1290312 64200 ?       Ssl  Jun15   0:48 /usr/sbin/mysqld
www-data     567  0.1  0.4 142100  9200 ?        S    Jun15   0:05 nginx: worker process
www-data     568  0.0  0.4 142100  9200 ?        S    Jun15   0:01 nginx: worker process
ubuntu       890  0.0  0.2  22412  5102 pts/0    Ss   12:00   0:00 -bash
ubuntu       912  0.0  0.1  37280  3140 pts/0    R+   12:05   0:00 ps aux"""


def top():
    import datetime
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return f"""top - {current_time} up 2 days, 18 min,  1 user,  load average: 0.00, 0.01, 0.05
Tasks: 104 total,   1 running, 103 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.3 us,  0.1 sy,  0.0 ni, 99.6 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   1984.3 total,   1245.1 free,    312.4 used,    426.8 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   1512.2 avail Mem 

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
    1 root      20   0  168340  11824   8292 S   0.0   0.6   0:02.11 systemd
  221 root      20   0   15820   8204   7210 S   0.0   0.4   0:00.45 sshd
  334 mysql     20   0 1832048 245210  32104 S   0.0  12.1   4:12.33 mysqld
  510 www-data  20   0   56214   8410   6124 S   0.0   0.4   0:01.05 nginx
 1120 ubuntu    20   0   22452   4120   3210 S   0.0   0.2   0:00.15 bash"""

