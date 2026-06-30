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
