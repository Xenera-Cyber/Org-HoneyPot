import httpx
import re
from knowledge_base import knowledge_documents
from config import GROQ_API_KEY, GROQ_MODEL
import vector_store

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
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            print(f"[Groq API Error] Status code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"[Groq API Exception] {e}")
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
    # Check if the first line is the prompt + command, or just the command
    first_line = lines[0].strip()
    prompt_regex = r'^([a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+:.*?[#$]\s*)?'
    
    # Try matching prompt + exact command
    match = re.match(prompt_regex + re.escape(command_stripped) + r'\s*$', first_line, re.IGNORECASE)
    if match:
        lines.pop(0)
    else:
        # Try matching prompt + command name (e.g. "ubuntu@server:~$ whoami")
        match = re.match(prompt_regex + re.escape(base_cmd) + r'\b.*$', first_line, re.IGNORECASE)
        if match:
            lines.pop(0)
        elif first_line.lower() == command_stripped.lower() or first_line.lower() == base_cmd.lower():
            lines.pop(0)

    # Clean any resulting empty lines at the top
    while lines and not lines[0].strip():
        lines.pop(0)

    # 2. Clean trailing echoes/prompts
    # Check if the last line is a terminal prompt
    if lines:
        last_line = lines[-1].strip()
        # Regex to match just a prompt at the end
        if re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+:.*?[#$]\s*$', last_line) or last_line.endswith("$") or last_line.endswith("#"):
            if "@" in last_line or last_line.startswith("ubuntu") or last_line.startswith("root"):
                lines.pop()

    # Clean any resulting empty lines at the bottom
    while lines and not lines[-1].strip():
        lines.pop()

    return "\n".join(lines).strip()

def retrieve_context(command):
    if not command:
        return None
    
    cmd_lower = command.lower().strip()
    parts = cmd_lower.split()
    if not parts:
        return None
    
    query_cmd_name = parts[0]
    import os
    sorted_docs = sorted(knowledge_documents, key=lambda x: len(x["command"]), reverse=True)

    # 1. Strict cat file matching first to prevent incorrect document leaks
    if query_cmd_name == "cat":
        if len(parts) > 1:
            query_file = parts[1].strip()
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

    # 2. Try vector store search with a threshold
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

    # 3. Fallback matching with word boundaries
    for doc in sorted_docs:
        doc_cmd = doc["command"].lower()
        doc_parts = doc_cmd.split()
        if doc_parts:
            if doc_parts[0] == query_cmd_name:
                if all(p in parts for p in doc_parts):
                    return doc
            
    return None


async def generate_deception(command, history=None, cwd=None, attack_type=None, hostname=None, username=None):
    context_doc = retrieve_context(command)

    # Shortcut routing for exact command matches or static file reads to bypass LLM latency and safety blocks
    if context_doc:
        import os
        cmd_stripped = command.strip()
        doc_cmd = context_doc["command"].strip()
        
        # 1. Exact match
        if doc_cmd == cmd_stripped:
            return context_doc['example_output'].strip()
            
        # 2. Cat/file read shortcut
        if cmd_stripped.startswith("cat "):
            parts = cmd_stripped.split()
            if len(parts) == 2:
                filename_only = os.path.basename(parts[1])
                if doc_cmd.startswith("cat ") and (filename_only in doc_cmd or parts[1] in doc_cmd):
                    return context_doc['example_output'].strip()

    reference_format = context_doc['example_output'].strip() if context_doc else "None. Simulate realistic terminal output based on standard Ubuntu behavior."
    
    # Format command history for context
    history_str = "\n".join(f"- {h}" for h in history) if history else "No command history."

    active_host = hostname or "ubuntu-server"
    active_user = username or "ubuntu"

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
      - /var/www (contains internal)
      - /var/www/internal (contains clients.json, vendors.json, infrastructure_assets.yaml, db_backup.sql, dev_tasks.md)
      - /etc (contains passwd, shadow, nginx)
      - /etc/nginx (contains sites-available)
      - /etc/nginx/sites-available (contains default)
    - File contents:
      - /home/ubuntu/notes.txt: "Remember to update the server.\\nCheck the internal admin scripts under /var/www/internal/dev_tasks.md for migration tasks and access credentials.\\n"
      - /home/ubuntu/script.sh: "#!/bash\\necho Hello World\\n"
      - /etc/passwd: "root:x:0:0:root:/root:/bin/bash\\nubuntu:x:1000:1000::/home/ubuntu:/bin/bash\\n"
      - (Note: Contents for employees.csv, projects.csv, departments.json, audit_log.csv, clients.json, vendors.json, db_backup.sql, dev_tasks.md, /etc/shadow, nginx config default, infrastructure_assets.yaml, all files under .ssh, .aws, .slack, .env, and all markdown/json/yaml reports/documents under /home/ubuntu/documents are provided in the REFERENCE FORMAT GUIDE if the command reads or queries them.)"""

    prompt = f"""You are simulating a real Linux terminal on an Ubuntu 22.04 LTS server.
    
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
    
    Generate terminal output:"""

    raw_response = await call_groq_api(prompt, max_tokens=1024)
    if raw_response is None:
        # Fallback to example output directly if API call failed
        if context_doc:
            return context_doc['example_output'].strip()
        else:
            parts = command.split()
            cmd_name = parts[0] if parts else command
            return f"bash: {cmd_name}: command not found"

    return clean_llm_output(raw_response, command)
