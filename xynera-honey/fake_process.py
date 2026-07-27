def _service_active(service_manager, program):
    """
    Look up whether a fake service (by its netstat/ps program name, e.g.
    "sshd", "mysqld", "nginx") is currently running for this session.

    Defaults to True (always shown) when no service_manager is supplied
    or when the program isn't tracked by ServiceManager — matching how
    fake_network/service_manager already treat always-on background
    processes (e.g. fail2ban, cron, rsyslogd never get stopped).
    """
    if service_manager is None:
        return True
    result = service_manager.is_running_by_program(program)
    return True if result is None else result


def ps(service_manager=None):
    """
    `ps` process listing. When a ServiceManager is supplied (see
    session_manager.service_manager / server.py), rows for sshd/mysqld/
    nginx are only shown while the backing service is actually running,
    so `service <n> stop` followed by `ps` stays consistent with
    `systemctl`/`netstat`/`ss`. PID consistency is preserved: a stopped
    service's row simply disappears and reappears with the same PID
    when the service is restarted, exactly like the real `ps` would
    behave for a respawned process with a fixed line in this static table.
    """
    lines = [
        "  PID TTY          TIME CMD",
        "    1 ?        00:00:02 systemd",
        "    2 ?        00:00:00 kthreadd",
        "    4 ?        00:00:00 kworker/0:0",
        "   14 ?        00:00:00 rcu_sched",
    ]

    if _service_active(service_manager, "sshd"):
        lines.append("  221 ?        00:00:00 sshd")

    lines.append("  289 ?        00:00:00 cron")
    lines.append("  301 ?        00:00:01 rsyslogd")

    if _service_active(service_manager, "fail2ban-server"):
        lines.append("  315 ?        00:00:02 fail2ban-server")
    if _service_active(service_manager, "mysqld"):
        lines.append("  334 ?        00:00:05 mysqld")
    if _service_active(service_manager, "nginx"):
        lines.append("  567 ?        00:00:01 nginx")
        lines.append("  568 ?        00:00:01 nginx")

    lines.append("  890 pts/0    00:00:00 bash")
    lines.append("  942 pts/0    00:00:00 ps")

    return "\n".join(lines)


def ps_aux(username="ubuntu", service_manager=None):
    """
    `ps aux` listing.

    Bug fix (kept from baseline): the last two process rows (the
    attacker's own shell + this `ps aux` command) previously hardcoded
    "ubuntu" as the owning user, even after the session identity
    changed. They now reflect whatever username is currently active
    for this session.

    Enhancement: rows for sshd/fail2ban/mysqld/nginx now respect the
    session's ServiceManager state (see `ps()` above), so a stopped
    service disappears from `ps aux` just as it does from `ps`,
    `systemctl`, and `netstat`.
    """
    lines = [
        "USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND",
        "root         1  0.0  0.1 169280 11232 ?        Ss   08:10   0:02 /sbin/init",
        "root         2  0.0  0.0      0     0 ?        S    08:10   0:00 [kthreadd]",
        "root         4  0.0  0.0      0     0 ?        I<   08:10   0:00 [kworker/0:0]",
        "root        14  0.0  0.0      0     0 ?        S    08:10   0:00 [rcu_sched]",
    ]

    if _service_active(service_manager, "sshd"):
        lines.append("root       221  0.0  0.2  15432  6236 ?        Ss   08:11   0:00 /usr/sbin/sshd -D")

    lines.append("root       289  0.0  0.1   8948  3228 ?        Ss   08:11   0:00 /usr/sbin/cron -f")
    lines.append("syslog     301  0.1  0.3 222364 12480 ?        Ssl  08:11   0:01 /usr/sbin/rsyslogd -n")

    if _service_active(service_manager, "fail2ban-server"):
        lines.append("root       315  0.2  0.5 284320 20124 ?        Ssl  08:11   0:02 /usr/bin/python3 /usr/bin/fail2ban-server")
    if _service_active(service_manager, "mysqld"):
        lines.append("mysql      334  0.4  1.3 1723456 53212 ?       Ssl  08:11   0:05 /usr/sbin/mysqld")
    if _service_active(service_manager, "nginx"):
        lines.append("www-data   567  0.1  0.4 225480 16784 ?        S    08:11   0:01 nginx: master process /usr/sbin/nginx")
        lines.append("www-data   568  0.0  0.4 225480 16784 ?        S    08:11   0:01 nginx: worker process")

    lines.append(f"{username:<10} 890  0.0  0.1  22040  5408 pts/0    Ss   08:20   0:00 -bash")
    lines.append(f"{username:<10} 942  0.0  0.1  11824  3104 pts/0    R+   08:23   0:00 ps aux")

    return "\n".join(lines)
