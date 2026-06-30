import sys
import os

# Dynamic import of data_generator from xynera-ai
# The directory structure is:
# honey-main/
#   xynera-honey/
#     fake_filesystem.py
#   xynera-ai/
#     data_generator.py
ai_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "xynera-ai"))
if ai_path not in sys.path:
    sys.path.insert(0, ai_path)

try:
    from data_generator import get_generated_all
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
        "incident_2026_06_01_phishing.md": "/home/ubuntu/documents/incident_reports/incident_2026_06_01_phishing.md"
    }
    for key, path in doc_paths.items():
        if key in gen_data["documents"]:
            file_contents[path] = gen_data["documents"][key]
            
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

# Standard system configuration files and logs
file_contents["/home/ubuntu/notes.txt"] = "Remember to update the server.\nCheck the internal admin scripts under /var/www/internal/dev_tasks.md for migration tasks and access credentials.\n"
file_contents["/home/ubuntu/script.sh"] = "#!/bin/bash\necho Hello World\n"
file_contents["/etc/hosts"] = """127.0.0.1 localhost
127.0.1.1 web-prod-01
10.0.0.10 db-prod-01
10.0.0.11 backup-01
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
for file_path in file_contents.keys():
    parts = file_path.split("/")
    for i in range(1, len(parts)):
        parent = "/" + "/".join(parts[1:i])
        parent = parent.replace("//", "/")
        child = parts[i]
        
        if parent not in filesystem:
            filesystem[parent] = []
        if child not in filesystem[parent]:
            filesystem[parent].append(child)

# Add directories that don't have files directly in them if any
for dir_name in ["/tmp", "/boot", "/dev", "/usr", "/usr/sbin", "/var/backups", "/var/www"]:
    if dir_name not in filesystem:
        filesystem[dir_name] = []
