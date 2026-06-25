def ps():
    return """USER       PID   %CPU %MEM COMMAND
root         1    0.0  0.1 /sbin/init
root         2    0.0  0.0 [kthreadd]
root         4    0.0  0.0 [kworker/0:0]
root        14    0.0  0.0 [rcu_sched]
root       221    0.0  0.2 /usr/sbin/sshd -D
root       289    0.0  0.1 /usr/sbin/cron -f
syslog     301    0.1  0.3 /usr/sbin/rsyslogd -n
root       315    0.2  0.5 /usr/bin/python3 /usr/bin/fail2ban-server
mysql      334    0.4  1.3 /usr/sbin/mysqld
www-data   567    0.1  0.4 nginx: worker process
www-data   568    0.0  0.4 nginx: worker process
ubuntu     890    0.0  0.1 -bash"""


def ps_aux():
    return """USER       PID  COMMAND
root       221  sshd
root       289  cron
syslog     301  rsyslogd
root       315  fail2ban-server
mysql      334  mysqld
www-data   567  nginx
ubuntu     890  bash"""
