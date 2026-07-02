import sys
import os

# Dynamic import of data_generator from xynera_ai
# The directory structure is:
# honey-main/
#   xynera_honey/
#     fake_filesystem.py
#   xynera_ai/
#     data_generator.py
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_path not in sys.path:
    sys.path.append(parent_path)

try:
    from xynera_ai.data_generator import get_generated_all
    gen_data = get_generated_all()
except Exception as e:
    print(f"Error loading dynamic dataset generator: {e}", file=sys.stderr)
    gen_data = {}

file_contents = {}

# Map dynamic files to filesystem paths
if gen_data:
    file_contents["/home/ubuntu/company_directory/employees.csv"] = gen_data.get("employees_csv", "")
    file_contents["/home/ubuntu/company_directory/projects.csv"] = gen_data.get("projects_csv", "")
    file_contents["/home/ubuntu/company_directory/departments.json"] = gen_data.get("departments_json", "")
    file_contents["/var/www/internal/clients.json"] = gen_data.get("clients_json", "")
    file_contents["/var/www/internal/vendors.json"] = gen_data.get("vendors_json", "")
    file_contents["/var/www/internal/infrastructure_assets.yaml"] = gen_data.get("infrastructure_yaml", "")
    
    # Wednesday markdown documents
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
    docs_data = gen_data.get("documents", {})
    if isinstance(docs_data, str):
        try:
            import json
            docs_data = json.loads(docs_data)
        except Exception:
            pass
    if isinstance(docs_data, dict):
        for key, path in doc_paths.items():
            if key in docs_data:
                file_contents[path] = docs_data[key]
            
    # Credentials & secrets
    file_contents["/home/ubuntu/.ssh/id_rsa"] = gen_data.get("ssh_private_key", "")
    file_contents["/etc/shadow"] = gen_data.get("shadow_file", "")
    file_contents["/etc/passwd"] = gen_data.get("passwd_file", "")
    file_contents["/home/ubuntu/.aws/credentials"] = gen_data.get("aws_credentials", "")
    file_contents["/home/ubuntu/.slack/config.json"] = gen_data.get("slack_config_json", "")
    file_contents["/home/ubuntu/.env"] = gen_data.get("env_file", "")
    file_contents["/home/ubuntu/company_directory/audit_log.csv"] = gen_data.get("audit_log_csv", "")
    file_contents["/home/ubuntu/documents/technical_docs/stripe_config.json"] = gen_data.get("stripe_config_json", "")
    file_contents["/home/ubuntu/documents/technical_docs/k8s_deployment.yaml"] = gen_data.get("kubernetes_yaml", "")
    file_contents["/var/www/internal/db_backup.sql"] = gen_data.get("db_backup_sql", "")
    file_contents["/etc/nginx/sites-available/default"] = gen_data.get("nginx_conf", "")
    file_contents["/var/www/internal/dev_tasks.md"] = gen_data.get("dev_tasks_md", "")
    file_contents["/etc/gateway/router.conf"] = gen_data.get("gateway_router_conf", "")
    file_contents["/home/ubuntu/.ssh/backup_key"] = gen_data.get("backup_key", "")
    file_contents["/home/dev/backup_status.txt"] = gen_data.get("backup_status_txt", "")

    # Config files
    file_contents["/etc/ssh/sshd_config"] = gen_data.get("sshd_config", "")
    file_contents["/etc/redis/redis.conf"] = gen_data.get("redis_config", "")
    file_contents["/etc/postgresql/14/main/postgresql.conf"] = gen_data.get("postgresql_config", "")
    file_contents["/home/ubuntu/.aws/config"] = gen_data.get("aws_config", "")
    file_contents["/home/ubuntu/.kube/config"] = gen_data.get("kube_config", "")
    file_contents["/home/ubuntu/.pgpass"] = gen_data.get("pgpass_file", "")
    file_contents["/etc/netplan/01-netcfg.yaml"] = gen_data.get("netplan_config", "")
    file_contents["/etc/hosts"] = gen_data.get("hosts_file", "")

    # Emails
    if "emails" in gen_data:
        emails_data = gen_data["emails"]
        if isinstance(emails_data, str):
            try:
                import json
                emails_data = json.loads(emails_data)
            except Exception:
                pass
        if isinstance(emails_data, dict):
            file_contents["/home/ubuntu/emails/inbox_summary.txt"] = emails_data.get("inbox_summary.txt", "")
            file_contents["/home/ubuntu/emails/security_phishing_alert.txt"] = emails_data.get("security_phishing_alert.txt", "")
            file_contents["/home/ubuntu/emails/staging_db_access.txt"] = emails_data.get("staging_db_access.txt", "")
            file_contents["/home/ubuntu/emails/performance_review_cycle.txt"] = emails_data.get("performance_review_cycle.txt", "")
            file_contents["/home/ubuntu/emails/vendor_contract_renewal.txt"] = emails_data.get("vendor_contract_renewal.txt", "")

# Standard system configuration files and logs
file_contents["/home/ubuntu/notes.txt"] = "Remember to update the server.\nCheck the internal admin scripts under /var/www/internal/dev_tasks.md for migration tasks and access credentials.\n"
file_contents["/home/ubuntu/script.sh"] = "#!/bin/bash\necho Hello World\n"
if "/etc/hosts" not in file_contents:
    file_contents["/etc/hosts"] = """127.0.0.1 localhost
127.0.1.1 web-prod-01
10.200.100.15 prod-db-01.xynera.local prod-db-01
10.200.100.40 backup-node-02
"""
file_contents["/etc/hostname"] = "web-prod-01\n"
file_contents["/var/log/auth.log"] = """Jun 15 08:01:22 sshd[2211]: Accepted password for ubuntu
Jun 15 08:15:13 sshd[2214]: Accepted password for dev
Jun 15 09:01:55 CRON[1001]: Job Started
"""
file_contents["/var/log/syslog"] = """Jun 15 nginx restarted
Jun 15 mysql service started
Jun 15 backup completed successfully
"""

# Reconstruct filesystem hierarchy dynamically
filesystem = {}
empty_dirs = ["/tmp", "/boot", "/dev", "/usr", "/usr/sbin", "/var/backups", "/var/www", "/root", "/sys", "/proc", "/opt"]
all_paths = list(file_contents.keys()) + empty_dirs

for path in all_paths:
    parts = path.split("/")
    for i in range(1, len(parts)):
        parent = "/" + "/".join(parts[1:i])
        parent = parent.replace("//", "/")
        child = parts[i]
        
        if parent not in filesystem:
            filesystem[parent] = []
        if child not in filesystem[parent]:
            filesystem[parent].append(child)

    if path in empty_dirs:
        if path not in filesystem:
            filesystem[path] = []

def resolve_path(cwd, path):
    if path.startswith("/"):
        full_path = path
    else:
        full_path = f"{cwd}/{path}" if cwd != "/" else f"/{path}"
    
    parts = []
    for segment in full_path.split("/"):
        if not segment or segment == ".":
            continue
        if segment == "..":
            if parts:
                parts.pop()
        else:
            parts.append(segment)
            
    return "/" + "/".join(parts)

def ls(session):
    cwd = session.get("cwd", "/")
    return "\n".join(filesystem.get(cwd, []))

def cd(session, path):
    cwd = session.get("cwd", "/")
    new_path = resolve_path(cwd, path)
    if new_path in filesystem:
        session["cwd"] = new_path
        return ""
    else:
        return f"cd: no such file or directory: {path}"

def cat(session, path):
    cwd = session.get("cwd", "/")
    full_path = resolve_path(cwd, path)
    if full_path in file_contents:
        return file_contents[full_path]
    return f"cat: {path}: No such file"


