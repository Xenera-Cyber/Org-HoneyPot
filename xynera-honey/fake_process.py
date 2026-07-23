def _get_active_services(session_manager):
    """
    Helper to fetch active services from the session manager.
    Defaults to all running if the service tracker isn't initialized yet.
    """
    if session_manager and hasattr(session_manager, 'get_active_services'):
        return session_manager.get_active_services()
    # Default active services if state is unknown
    return ["sshd", "fail2ban", "mysql", "nginx", "ssh", "mysqld"]

def ps(session_manager=None):
    active = _get_active_services(session_manager)
    
    lines = [
        "  PID TTY          TIME CMD",
        "    1 ?        00:00:02 systemd",
        "    2 ?        00:00:00 kthreadd",
        "    4 ?        00:00:00 kworker/0:0",
        "   14 ?        00:00:00 rcu_sched"
    ]
    
    if "sshd" in active or "ssh" in active:
        lines.append("  221 ?        00:00:00 sshd")
        
    lines.append("  289 ?        00:00:00 cron")
    lines.append("  301 ?        00:00:01 rsyslogd")
    
    if "fail2ban" in active:
        lines.append("  315 ?        00:00:02 fail2ban-server")
    if "mysql" in active or "mysqld" in active:
        lines.append("  334 ?        00:00:05 mysqld")
    if "nginx" in active:
        lines.append("  567 ?        00:00:01 nginx")
        lines.append("  568 ?        00:00:01 nginx")
        
    lines.append("  890 pts/0    00:00:00 bash")
    lines.append("  942 pts/0    00:00:00 ps")
    
    return "\n".join(lines)

def ps_aux(session_manager=None):
    """
    Bug fix: the last two process rows (the attacker's own shell + this
    `ps aux` command) previously hardcoded "ubuntu" as the owning user,
    even after the session identity changed. They now reflect whatever
    username is currently active for this session.
    """
    active = _get_active_services(session_manager)
    
    # Extract dynamic username if session_manager is provided
    username = "ubuntu"
    if session_manager and hasattr(session_manager, 'get_username'):
        username = session_manager.get_username()
        
    lines = [
        "USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND",
        "root         1  0.0  0.1 169280 11232 ?        Ss   08:10   0:02 /sbin/init",
        "root         2  0.0  0.0      0     0 ?        S    08:10   0:00 [kthreadd]",
        "root         4  0.0  0.0      0     0 ?        I<   08:10   0:00 [kworker/0:0]",
        "root        14  0.0  0.0      0     0 ?        S    08:10   0:00 [rcu_sched]"
    ]
    
    if "sshd" in active or "ssh" in active:
        lines.append("root       221  0.0  0.2  15432  6236 ?        Ss   08:11   0:00 /usr/sbin/sshd -D")
        
    lines.append("root       289  0.0  0.1   8948  3228 ?        Ss   08:11   0:00 /usr/sbin/cron -f")
    lines.append("syslog     301  0.1  0.3 222364 12480 ?        Ssl  08:11   0:01 /usr/sbin/rsyslogd -n")
    
    if "fail2ban" in active:
        lines.append("root       315  0.2  0.5 284320 20124 ?        Ssl  08:11   0:02 /usr/bin/python3 /usr/bin/fail2ban-server")
    if "mysql" in active or "mysqld" in active:
        lines.append("mysql      334  0.4  1.3 1723456 53212 ?       Ssl  08:11   0:05 /usr/sbin/mysqld")
    if "nginx" in active:
        lines.append("www-data   567  0.1  0.4 225480 16784 ?        S    08:11   0:01 nginx: master process /usr/sbin/nginx")
        lines.append("www-data   568  0.0  0.4 225480 16784 ?        S    08:11   0:01 nginx: worker process")
        
    lines.append(f"{username:<10} 890  0.0  0.1  22040  5408 pts/0    Ss   08:20   0:00 -bash")
    lines.append(f"{username:<10} 942  0.0  0.1  11824  3104 pts/0    R+   08:23   0:00 ps aux")
    
    return "\n".join(lines)