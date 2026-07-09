import httpx
import re
import asyncio
from knowledge_base import knowledge_documents
from config import GROQ_API_KEY, GROQ_MODEL
from guardrails import apply_guardrails
from attacker_profile import get_session_data
import vector_store

# Pre-sort the knowledge documents by command length in reverse order once at module-load time
sorted_docs = sorted(knowledge_documents, key=lambda x: len(x["command"]), reverse=True)


async def call_groq_api(prompt, max_tokens=1024):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0.1
    }
    
    retries = 6
    delay = 2.0
    
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=25.0) as client:
                response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            
            elif response.status_code == 429:
                retry_after = 6.0
                try:
                    err_data = response.json()
                    msg = err_data.get("error", {}).get("message", "")
                    match = re.search(r"try again in ([0-9\.]+)s", msg)
                    if match:
                        retry_after = float(match.group(1)) + 1.0
                    elif "retry-after" in response.headers:
                        retry_after = float(response.headers["retry-after"]) + 1.0
                except:
                    pass
                print(f"[Rate Limit 429] Limit reached. Sleeping for {retry_after:.2f}s before retry (Attempt {attempt+1}/{retries})...")
                await asyncio.sleep(retry_after)
            
            elif response.status_code in [500, 502, 503, 504]:
                print(f"[Groq API Temp Error] Status {response.status_code}. Sleeping for {delay}s before retry...")
                await asyncio.sleep(delay)
                delay *= 2
            
            else:
                print(f"[Groq API Error] Status code: {response.status_code}, Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"[Groq API Exception] {e}. Sleeping for {delay}s...")
            await asyncio.sleep(delay)
            delay *= 2
            
    return None


def clean_llm_output(text, command):
    if not text:
        return ""
    text = text.strip()
    
    # Remove markdown code blocks if present
    if text.startswith("```"):
        nl_idx = text.find("\n")
        if nl_idx != -1:
            text = text[nl_idx+1:]
        else:
            text = text.strip("`")
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    # Split text into lines to process leading/trailing garbage
    lines = text.split("\n")
    if not lines:
        return ""

    command_stripped = command.strip()
    cmd_parts = command_stripped.split()
    base_cmd = cmd_parts[0] if cmd_parts else ""

    # 1. Clean leading echoes
    first_line = lines[0].strip()
    prompt_regex = r'^([a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+:.*?[#$]\s*)?'
    
    match = re.match(prompt_regex + re.escape(command_stripped) + r'\s*$', first_line, re.IGNORECASE)
    if match:
        lines.pop(0)
    else:
        match = re.match(prompt_regex + re.escape(base_cmd) + r'\b.*$', first_line, re.IGNORECASE)
        if match:
            lines.pop(0)
        elif first_line.lower() == command_stripped.lower() or first_line.lower() == base_cmd.lower():
            lines.pop(0)

    while lines and not lines[0].strip():
        lines.pop(0)

    # 2. Clean trailing echoes/prompts
    if lines:
        last_line = lines[-1].strip()
        if re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+:.*?[#$]\s*$', last_line) or last_line.endswith("$") or last_line.endswith("#"):
            if "@" in last_line or last_line.startswith("ubuntu") or last_line.startswith("root"):
                lines.pop()

    while lines and not lines[-1].strip():
        lines.pop()

    return "\n".join(lines).strip()


COMMAND_TO_DATA_KEY = {
    "/home/ubuntu/company_directory/employees.csv": "employees_csv",
    "/home/ubuntu/company_directory/projects.csv": "projects_csv",
    "/home/ubuntu/company_directory/departments.json": "departments_json",
    "/var/www/internal/clients.json": "clients_json",
    "/var/www/internal/vendors.json": "vendors_json",
    "/var/www/internal/infrastructure_assets.yaml": "infrastructure_yaml",
    "/home/ubuntu/.ssh/id_rsa": "ssh_private_key",
    "/etc/shadow": "shadow_file",
    "/etc/passwd": "passwd_file",
    "/home/ubuntu/.aws/credentials": "aws_credentials",
    "/home/ubuntu/.aws/config": "aws_config",
    "/home/ubuntu/.kube/config": "kube_config",
    "/etc/netplan/01-netcfg.yaml": "netplan_config",
    "/etc/hosts": "hosts_file",
    "/home/ubuntu/.pgpass": "pgpass_file",
    "/home/ubuntu/.slack/config.json": "slack_config_json",
    "/home/ubuntu/documents/technical_docs/stripe_config.json": "stripe_config_json",
    "/var/www/internal/db_backup.sql": "db_backup_sql",
    "/home/ubuntu/company_directory/audit_log.csv": "audit_log_csv",
    "/var/log/auth.log": "auth_log",
    "/var/log/syslog": "syslog",
    "/etc/nginx/nginx.conf": "nginx_conf",
    "/home/ubuntu/documents/technical_docs/k8s_deployment.yaml": "kubernetes_yaml",
    "/home/ubuntu/.env": "env_file",
    "/var/www/internal/dev_tasks.md": "dev_tasks_md",
    "/etc/gateway/router.conf": "gateway_router_conf",
    "/home/ubuntu/.ssh/backup_key": "backup_key",
    "/home/dev/backup_status.txt": "backup_status_txt",
    "/etc/ssh/sshd_config": "sshd_config",
    "/etc/redis/redis.conf": "redis_config",
    "/etc/postgresql/14/main/postgresql.conf": "postgresql_config",
    "/home/ubuntu/emails/inbox_summary.txt": ("emails", "inbox_summary.txt"),
    "/home/ubuntu/emails/security_phishing_alert.txt": ("emails", "security_phishing_alert.txt"),
    "/home/ubuntu/emails/staging_db_access.txt": ("emails", "staging_db_access.txt"),
    "/home/ubuntu/emails/performance_review_cycle.txt": ("emails", "performance_review_cycle.txt"),
    "/home/ubuntu/emails/vendor_contract_renewal.txt": ("emails", "vendor_contract_renewal.txt"),
}


def retrieve_context(command, session_id=None):
    if not command:
        return None
    
    cmd_lower = command.lower().strip()
    parts = cmd_lower.split()
    if not parts:
        return None
    
    query_cmd_name = parts[0]
    import os

    # Dynamic session lookup for files and documents
    if session_id:
        try:
            session_data = get_session_data(session_id)
            if query_cmd_name == "cat" and len(parts) > 1:
                file_path = parts[1].strip().strip('"\'')
                file_basename = os.path.basename(file_path)
                
                for path, key in COMMAND_TO_DATA_KEY.items():
                    if file_path == path or file_basename == os.path.basename(path):
                        if isinstance(key, tuple):
                            val = session_data.get(key[0], {}).get(key[1], "")
                        else:
                            val = session_data.get(key, "")
                        return {
                            "command": f"cat {path}",
                            "description": "Dynamic file content",
                            "example_output": val
                        }
                
                if "documents" in session_data:
                    for doc_path, doc_content in session_data["documents"].items():
                        if file_path == doc_path or file_basename == os.path.basename(doc_path):
                            return {
                                "command": f"cat {doc_path}",
                                "description": "Dynamic markdown document",
                                "example_output": doc_content
                            }
        except Exception as e:
            print(f"[Dynamic RAG Intercept Error] {e}")

    # Fallback to static RAG if no session data matched
    if query_cmd_name == "cat":
        if len(parts) > 1:
            query_file = parts[1].strip().strip('"\'')
            query_filename = os.path.basename(query_file)
            for doc in sorted_docs:
                doc_cmd = doc["command"].lower()
                doc_parts = doc_cmd.split()
                if len(doc_parts) > 1 and doc_parts[0] == "cat":
                    doc_file = doc_parts[1].strip()
                    doc_filename = os.path.basename(doc_file)
                    if doc_file == query_file or doc_filename == query_filename:
                        return doc
            return None

    # Try vector store search with a threshold
    context_doc = vector_store.search(command, threshold=0.3)
    if context_doc:
        doc_cmd_parts = context_doc["command"].lower().split()
        if doc_cmd_parts:
            known_commands = {
                "rm", "sqlmap", "stop", "echo", "dirtycow", "pwd", "apt", 
                "systemctl", "nc", "chmod", "wget", "curl", "scp", "ssh", 
                "cd", "cat", "ls", "ps", "netstat", "ip", "df", "free", 
                "uname", "whoami", "who", "top", "ping", "history", "crontab", "mkdir"
            }
            is_shell_cmd = query_cmd_name in known_commands or any(p.startswith("-") for p in parts)
            if is_shell_cmd:
                doc_first = doc_cmd_parts[0]
                if query_cmd_name == "who" and doc_first == "whoami":
                    pass
                elif doc_first != query_cmd_name:
                    context_doc = None
        if context_doc:
            return context_doc

    # Fallback matching with word boundaries
    for doc in sorted_docs:
        doc_cmd = doc["command"].lower()
        doc_parts = doc_cmd.split()
        if doc_parts:
            if doc_parts[0] == query_cmd_name:
                if all(p in parts for p in doc_parts):
                    return doc
            
    return None


async def generate_response(command, personality, attacker_profile, threat_score, history=None, cwd=None, session_id=None):
    if not isinstance(personality, dict):
        personality = {
            "name": "Standard Ubuntu Server",
            "hostname": "ubuntu-server",
            "user": "ubuntu",
            "style": "normal",
            "description": "Clean production server",
            "response_style": "concise, accurate, and professional"
        }

    context_doc = retrieve_context(command, session_id=session_id)

    # Shortcuts
    if context_doc:
        import os
        cmd_stripped = command.strip()
        doc_cmd = context_doc["command"].strip()
        
        if doc_cmd == cmd_stripped:
            return context_doc['example_output'].strip()
            
        if cmd_stripped.startswith("cat "):
            parts = cmd_stripped.split()
            if len(parts) == 2:
                filename_only = os.path.basename(parts[1])
                if doc_cmd.startswith("cat ") and (filename_only in doc_cmd or parts[1] in doc_cmd):
                    return context_doc['example_output'].strip()

        if context_doc['example_output'].strip() == "":
            return ""

    reference_format = context_doc['example_output'].strip() if context_doc else "None. Simulate realistic terminal output based on standard Ubuntu behavior."
    
    history_str = "\n".join(f"- {h}" for h in history) if history else "No command history."

    active_host = personality.get("hostname", "ubuntu-server")
    active_user = personality.get("user", "ubuntu")

    if active_host == "staging-api-01":
        fs_state = """- Directory structure:
      - /
      - /home
      - /home/ubuntu (contains .ssh, api_test_script.py)
      - /home/ubuntu/.ssh (contains backup_key)
      - /etc
      - /etc/gateway (contains router.conf)
    - File contents:
      - /etc/passwd: "root:x:0:0:root:/root:/bin/bash\\nubuntu:x:1000:1000::/home/ubuntu:/bin/bash\\n"
      - /home/ubuntu/api_test_script.py: "#!/usr/bin/env python3\\nprint('Staging API Router service status: ACTIVE')\\n"
      - (Note: Contents for backup_key and router.conf are provided in the REFERENCE FORMAT GUIDE if the command reads or queries them.)"""
    elif active_host == "backup-node-02":
        fs_state = """- Directory structure:
      - /
      - /home
      - /home/dev (contains backup_status.txt, notes.txt)
      - /etc
    - File contents:
      - /etc/passwd: "root:x:0:0:root:/root:/bin/bash\\ndev:x:1001:1001::/home/dev:/bin/bash\\n"
      - /home/dev/notes.txt: "For automated vault synchronization, use aws s3 commands with the credentials configured in the vault cluster."
      - (Note: Contents for backup_status.txt are provided in the REFERENCE FORMAT GUIDE if the command reads or queries them.)"""
    else:
        fs_state = """- Directory structure:
      - /
      - /home
      - /home/ubuntu (contains notes.txt, script.sh, company_directory, documents, .ssh, .aws, .slack, .env)
      - /home/ubuntu/.ssh (contains id_rsa)
      - /home/ubuntu/.aws (contains credentials)
      - /home/ubuntu/.slack (contains config.json)
      - /home/ubuntu/company_directory (contains employees.csv, projects.csv, departments.json, audit_log.csv)
      - /home/ubuntu/documents (contains internal_reports, meeting_notes, technical_docs, incident_reports)
      - /home/ubuntu/documents/internal_reports (contains report_q1_security.md, report_cloud_migration.md)
      - /home/ubuntu/documents/meeting_notes (contains meeting_notes_2026_06_22.md, meeting_notes_2026_06_15.md)
      - /home/ubuntu/documents/technical_docs (contains vpn_access_guidelines.md, api_gateway_setup.md, stripe_config.json, k8s_deployment.yaml)
      - /home/ubuntu/documents/incident_reports (contains incident_2026_05_12_ddos.md, incident_2026_06_01_phishing.md)
      - /var
      - /var/log
      - /var/www (contains internal, html)
      - /var/www/html (contains uploads)
      - /var/www/html/uploads
      - /var/www/internal (contains clients.json, vendors.json, infrastructure_assets.yaml, db_backup.sql, dev_tasks.md)
      - /etc (contains passwd, shadow, nginx)
      - /etc/nginx (contains sites-available)
      - /etc/nginx/sites-available (contains default)
    - File contents:
      - /home/ubuntu/notes.txt: "Remember to update the server.\\nCheck the internal admin scripts under /var/www/internal/dev_tasks.md for migration tasks and access credentials.\\n"
      - /home/ubuntu/script.sh: "#!/bash\\necho Hello World\\n"
      - /etc/passwd: "root:x:0:0:root:/root:/bin/bash\\nubuntu:x:1000:1000::/home/ubuntu:/bin/bash\\n"
      - (Note: Contents for employees.csv, projects.csv, departments.json, audit_log.csv, clients.json, vendors.json, db_backup.sql, dev_tasks.md, /etc/shadow, nginx config default, infrastructure_assets.yaml, all files under .ssh, .aws, .slack, .env, and all markdown/json/yaml reports/documents under /home/ubuntu/documents are provided in the REFERENCE FORMAT GUIDE if the command reads or queries them.)"""

    persona_name = personality.get("name", "Standard Ubuntu Server")
    persona_style = personality.get("response_style", "concise, accurate, and professional")
    persona_desc = personality.get("description", "Clean production server")

    prompt = f"""You are simulating a real Linux terminal on a server matching the following persona:
    Persona Name: {persona_name}
    Description: {persona_desc}
    Required Deception/Response Style: {persona_style}
    
    ENVIRONMENT CONTEXT:
    - Hostname: {active_host}
    - Active User: {active_user} (uid={1000 if active_user == 'ubuntu' else 1001})
    - Shell: /bin/bash
    - Current Working Directory (CWD): {cwd or ('/home/ubuntu' if active_user == 'ubuntu' else '/home/dev')}
    
    MOCK FILESYSTEM STATE:
    {fs_state}
      
    ATTACKER COMMAND HISTORY (last 5 commands):
    {history_str}
    (Note: The history is provided strictly for logical context and continuity. Do NOT print the history commands or their outputs.)

    COMMAND EXECUTED:
    {command}

    REFERENCE FORMAT GUIDE:
    {reference_format}

    STRICT SIMULATION RULES:
    1. Output ONLY the raw stdout and stderr bytes produced by the execution of the current command ('COMMAND EXECUTED').
    2. Do NOT print the prompt (e.g., "ubuntu@server:~$"), do NOT echo the command itself, and do NOT include any trailing prompt or cursor. Start directly with the first line of the current command's output, and end immediately with the last line of stdout/stderr.
    3. Do NOT print the history commands, and do NOT print the outputs of the history commands.
    4. Do NOT write any conversational text, notes, preambles, apologies, or explanations (e.g. do NOT say "Here is the output" or "I am a terminal").
    5. Do NOT wrap the output in markdown code blocks (e.g. do NOT use ```bash or ``` tags).
    6. If the command includes parameters, targets, flags, IPs, domains, or filenames, you MUST dynamically adapt the output to match these inputs. For example:
       - If the command is "ping 8.8.8.8", show packets sent/received for 8.8.8.8.
       - If the command is "nmap -p 80 192.168.1.15", show port 80 open/closed for 192.168.1.15.
       - If the command reads a file (e.g., "cat filename" or "grep pattern filename"), you MUST output ONLY the exact content of that file (or the matching lines) from the REFERENCE FORMAT GUIDE, starting with the very first line of the file's content and ending with the very last line. Do NOT write any preambles, notes, or error messages (such as "Permission denied", "Connection failed", or accessibility warnings) before or after the file contents.
       - If the command queries or lists files (like "ls -la"), base the output on the MOCK FILESYSTEM STATE and current CWD, using real Linux output formatting (e.g. columns, permissions, owners).
    7. If the command has syntax errors, invalid flags, or missing arguments, print the exact command-specific error message a real Linux system would produce.
    8. If the command is completely unrecognized or not a valid Linux command, return "bash: [command_name]: command not found" (substitute the actual command name).
    9. Ensure all formatting, spacing, and column alignment in tables (like ps, netstat, df, systemctl) are perfectly aligned.
    10. Adhere strictly to the persona of a {persona_name}. The output format and content must reflect the response style: {persona_style}.
    
    Generate terminal output:"""

    raw_response = await call_groq_api(prompt, max_tokens=1024)
    if raw_response is None:
        if context_doc:
            response = context_doc['example_output'].strip()
        else:
            parts = command.split()
            cmd_name = parts[0] if parts else command
            response = f"bash: {cmd_name}: command not found"
    else:
        response = clean_llm_output(raw_response, command)

    return apply_guardrails(command, response)


async def generate_deception(command, history=None, cwd=None, attack_type=None, hostname=None, username=None, session_id=None):
    from personalities import get_personality
    score = 0
    if attack_type == "Reconnaissance":
        score = 5
    elif attack_type:
        score = 20
    
    personality = get_personality(ip=None, attack_type=attack_type, score=score)
    if hostname:
        personality["hostname"] = hostname
    if username:
        personality["user"] = username
        
    attacker_profile = {
        "commands": history or [],
        "confidence_score": 0.90
    }
    threat_score = {
        "score": score,
        "risk_level": "LOW" if score < 25 else "HIGH"
    }
    return await generate_response(
        command=command,
        personality=personality,
        attacker_profile=attacker_profile,
        threat_score=threat_score,
        history=history,
        cwd=cwd,
        session_id=session_id
    )
