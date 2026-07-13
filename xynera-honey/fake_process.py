def ps():
    return """  PID TTY          TIME CMD
    1 ?        00:00:02 systemd
    2 ?        00:00:00 kthreadd
    4 ?        00:00:00 kworker/0:0
   14 ?        00:00:00 rcu_sched
  221 ?        00:00:00 sshd
  289 ?        00:00:00 cron
  301 ?        00:00:01 rsyslogd
  315 ?        00:00:02 fail2ban-server
  334 ?        00:00:05 mysqld
  567 ?        00:00:01 nginx
  568 ?        00:00:01 nginx
  890 pts/0    00:00:00 bash
  942 pts/0    00:00:00 ps"""


def ps_aux():
    return """USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 169280 11232 ?        Ss   08:10   0:02 /sbin/init
root         2  0.0  0.0      0     0 ?        S    08:10   0:00 [kthreadd]
root         4  0.0  0.0      0     0 ?        I<   08:10   0:00 [kworker/0:0]
root        14  0.0  0.0      0     0 ?        S    08:10   0:00 [rcu_sched]
root       221  0.0  0.2  15432  6236 ?        Ss   08:11   0:00 /usr/sbin/sshd -D
root       289  0.0  0.1   8948  3228 ?        Ss   08:11   0:00 /usr/sbin/cron -f
syslog     301  0.1  0.3 222364 12480 ?        Ssl  08:11   0:01 /usr/sbin/rsyslogd -n
root       315  0.2  0.5 284320 20124 ?        Ssl  08:11   0:02 /usr/bin/python3 /usr/bin/fail2ban-server
mysql      334  0.4  1.3 1723456 53212 ?       Ssl  08:11   0:05 /usr/sbin/mysqld
www-data   567  0.1  0.4 225480 16784 ?        S    08:11   0:01 nginx: master process /usr/sbin/nginx
www-data   568  0.0  0.4 225480 16784 ?        S    08:11   0:01 nginx: worker process
ubuntu     890  0.0  0.1  22040  5408 pts/0    Ss   08:20   0:00 -bash
ubuntu     942  0.0  0.1  11824  3104 pts/0    R+   08:23   0:00 ps aux"""