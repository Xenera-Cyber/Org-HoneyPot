# 🐝 Xynera – Honey for Hackers

---

## ⚙️ Run Both Servers

### 🔹 Step 1: XYNERA-AI

> ⚠️ Remember to change the API

| Step         | Command                           |
| ------------ | --------------------------------- |
| Go to folder | `cd <xynera-ai-folder>`           |
| Create env   | `python3 -m venv venv`            |
| Activate env | `source venv/bin/activate`        |
| Install deps | `pip install -r requirements.txt` |
| Run server   | `python3 api_server.py`           |

---

### 🔹 Step 2: XYNERA-HONEYPOT

| Step         | Command                           |
| ------------ | --------------------------------- |
| Go to folder | `cd <xynera-honeypot-folder>`     |
| Create env   | `python3 -m venv venv`            |
| Activate env | `source venv/bin/activate`        |
| Install deps | `pip install -r requirements.txt` |
| Run server   | `python3 server.py`               |

---

## ✅ System Status

All systems should now be running.

---

## 🧪 Testing the Servers

### 🔹 Option 1: Curl Test

```bash
curl -X POST http://10.200.200.30:5000/process \
-H "Content-Type: application/json" \
-d '{"ip":"10.200.200.10","command":"nmap test"}'
```

---

### 🔹 Option 2: Attacker Machine

```bash
nc 10.200.200.20 2222
```

Then execute commands.

---

# 📌 Current Condition of the System

---

## 📁 Honeypot Server Structure

```
Honeypot Server
│
├── server.py
├── session_manager.py
├── command_router.py
├── fake_filesystem.py
├── fake_process.py
├── fake_network.py
└── ai_client.py
```

---

## 🎯 Purpose of Deception Layer

The honeypot is the **fake system attackers interact with**.

---

## 🧱 Architecture Overview

```
Attacker (Kali)
        │
        ▼
Honeypot Server (Deception Layer)
        │
        ▼
AI Backend (Intelligence Layer)
```

---

## 🔄 Data Flow

```
Attacker Command
        │
        ▼
server.py
        │
        ▼
command_router.py
        │
 ┌──────┴───────────────┐
 ▼                      ▼
Local Simulation        AI Backend
(fake modules)          (via ai_client)
        │                      │
        ▼                      ▼
Response               AI-generated response
        │                      │
        └──────────────┬───────┘
                       ▼
               Sent back to attacker
```

---

# 📂 File Responsibilities

---

## 🔹 server.py

**Handles:**

```
socket connection
input/output loop
session creation
command handling
```

---

## 🔹 session_manager.py

**Stores per-attacker data:**

| Field    | Description       |
| -------- | ----------------- |
| IP       | Attacker IP       |
| cwd      | Current directory |
| commands | Command history   |

**Example:**

```python
sessions = {
  "session_id": {
     "ip": "10.200.200.10",
     "cwd": "/",
     "commands": []
  }
}
```

---

## 🔹 command_router.py

**Decides routing:**

| Command Type    | Execution |
| --------------- | --------- |
| ls, ps, netstat | Local     |
| nmap, wget      | Backend   |

---

## 🔹 fake_filesystem.py

**Simulates:**

```
ls
cd
pwd
cat
```

**Example Structure:**

```
/
├── home
│   └── ubuntu
│       └── notes.txt
├── etc
│   └── passwd
```

---

## 🔹 fake_process.py

**Simulates:**

```
ps
top
```

**Example Output:**

```
USER       PID %CPU %MEM COMMAND
root         1  0.0  0.1 /sbin/init
root       221  0.0  0.2 sshd
mysql      334  0.4  1.3 mysqld
```

---

## 🔹 fake_network.py

**Simulates:**

```
netstat
ss
```

**Example:**

```
tcp   0.0.0.0:22        LISTEN
tcp   0.0.0.0:80        LISTEN
tcp   127.0.0.1:3306    LISTEN
```

---

## 🔹 ai_client.py

**Connects to backend:**

```
POST /process
```

**Request:**

```json
{
 "ip": "10.200.200.10",
 "command": "nmap target"
}
```

**Response:**

```json
{
 "reply": "...",
 "attack_type": "...",
 "score": ...,
 "threat_level": "..."
}
```

---

# ⚠️ Important Design Rules

---

## ❗ Rule 1 — Never Execute Real Commands

```
No os.system()
No subprocess
```

---

## ❗ Rule 2 — Always Return Something

```
fallback → "command not found"
```

---

## ❗ Rule 3 — No Visible Crashes

Never expose:

```
traceback
error
timeout
```

---

## ❗ Rule 4 — Keep It Believable

```
realistic outputs
consistent filesystem
(optional later: slow responses)
```

---

# 💻 Example Interaction

```
$ whoami
ubuntu

$ ls
home
var
etc

$ ps
USER PID ...

$ netstat
tcp 0.0.0.0:22 LISTEN

$ nmap target
Starting Nmap...

$ wget malware.sh
--2026-- Downloading...
```

---

# 🔗 Final System (Combined)

```
Kali Attacker
        │
        ▼
Honeypot Server
        │
        ▼
AI Backend
        │
        ▼
RAG Engine
        │
        ▼
Deception Output
```

---

# 🤖 AI Backend

---

## 📁 Structure

```
AI Backend
│
├── API Layer
│     api_server.py
│
├── Detection Layer
│     classifier.py
│
├── Behavior Layer
│     attacker_profile.py
│
├── Threat Analysis Layer
│     threat_engine.py
│
├── Logging Layer
│     logger.py
│
└── Config Layer
      config.py


rag_engine.py
│
├── embedding step      → bge-m3
├── vector search       → FAISS
├── reasoning           → deepseek-r1
└── deception response  → tinyllama
```
<img width="1262" height="941" alt="Screenshot from 2026-03-18 19-21-16" src="https://github.com/user-attachments/assets/84650c4f-0b1d-4346-9029-c1c3fedaf02b" />
<img width="1267" height="906" alt="Screenshot from 2026-03-18 19-20-46" src="https://github.com/user-attachments/assets/e249d548-84f9-4920-a94b-9e9da52a9093" />
<img width="1261" height="940" alt="Screenshot from 2026-03-18 10-50-25" src="https://github.com/user-attachments/assets/3c3128af-a32a-4b53-8287-a1b2c1a877a6" />



//Updates from cyber team(Author- Hriday):
1. fake_filesystem.py
Expanded the fake Linux filesystem to resemble a realistic enterprise server.
Added multiple directories such as /bin, /boot, /opt, /usr, /var/log, and backup locations.
Introduced realistic files including employee records, meeting notes, server inventory, authentication logs, database backups, and bash history.
Improved file contents to provide more believable information during attacker interaction.

2. fake_process.py
Increased the number of simulated running processes to better mimic a production Linux environment.
Added common system services such as cron, rsyslog, fail2ban, PostgreSQL, Redis, and multiple Nginx worker processes.
Implemented support for the ps aux command in addition to the existing ps command.

3. fake_network.py
Enhanced simulated network services by adding HTTPS, PostgreSQL, Redis, Jenkins, and Prometheus ports.
Added support for additional networking commands including netstat -tulpn, ifconfig, and ip addr.
Improved network responses with realistic interface configurations and service information.

4. session_manager.py
Redesigned session handling using an object-oriented SessionManager class.
Added session metadata including session ID, attacker IP, timestamps, threat score, attack history, and session status.
Implemented dedicated methods for command tracking, directory management, attack recording, session summary generation, and session closure.

5. logger.py
Introduced a dedicated logging module for structured attack logging.
Implemented rotating log files with automatic log directory creation.
Added timestamped logging of attacker IP, session ID, attack type, and executed command for improved monitoring and forensic analysis.

6. attack_analyzer.py
Expanded attack classification by adding Privilege Escalation and Reverse Shell Activity detection.
Introduced a threat scoring mechanism to assign severity levels to different attack categories.
Improved the foundation for future threat monitoring and reporting.

7. command_router.py
Reorganized command handling into logical categories for better readability and maintainability.
Added support for several new Linux commands including users, ls -la, ps aux, netstat -tulpn, hostname, uname -a, uptime, systemctl, ifconfig, and ip addr.
Improved path handling for cd and enhanced file access logic for cat.
Extended support for common attacker commands such as wget, curl, chmod, and nc.

8. server.py
Improved overall server workflow by integrating session tracking, attack classification, threat scoring, and centralized logging.
Added real-time console monitoring of attacker commands and detected attack types.
Implemented automatic session summary generation upon client disconnection.
Improved modular interaction between the server and supporting components.

Overall Project Enhancements
Improved code modularity and separation of responsibilities across all components.
Increased realism of the honeypot environment to provide a more convincing attacker experience.
Enhanced scalability by preparing the architecture for future integration with SQLite, AI-based deception, dashboards, and advanced threat analysis.
Maintained compatibility with the existing project structure while providing a stronger and more extensible baseline for future development.
