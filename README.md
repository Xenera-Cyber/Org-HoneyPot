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



CONTRIBUTIONS:

🧵 1. The Concurrency Engine (server.py)

Thread-Safe Architecture: Upgraded the core listener into a multi-threaded TCP server. Implemented threading.Lock and daemon threads to handle simultaneous, overlapping attacker connections without blocking or log interleaving.

Background Health Monitoring: Integrated a continuous, background daemon thread to monitor the AI backend's health, allowing the server to seamlessly hot-swap between LLM-driven responses and local fallback emulation without requiring a server restart.

🧠 2. The State Controller (session_manager.py)

Multi-Client State Tracking: Engineered a thread-safe MultiSessionManager to uniquely identify and track sessions by attacker IP, preventing state corruption during concurrent attacks.

Identity Synchronization: Built a rigorous identity management system. If an attacker escalates privileges or changes hostnames, the state propagates instantly across the entire simulation—automatically rewriting simulated system files (like /etc/passwd and /etc/hosts), updating environment variables ($USER, $PWD), and adjusting the live shell prompt.

📁 3. The Virtual Sandbox (fake_filesystem.py)

Isolated Tree-Based Filesystem: Replaced static text outputs with a fully mutable, tree-based virtual filesystem. Every attacker session receives a strictly isolated, sandbox clone of the OS structure.

Dynamic AI Seeding: Tied the filesystem generation to unique session IDs, allowing the AI to dynamically seed realistic documents, .ssh keys, and configuration files into the environment before the attacker even runs ls.

Stateful Metadata: Implemented a Metadata tracking class to realistically simulate file ownership, permissions, and creation/modification timestamps as attackers interact with the environment (touch, mkdir, rm, cp).

🔀 4. The Simulation Router (command_router.py)

Dynamic Telemetry & Timing: Stripped hardcoded system responses, replacing them with a persistent SYSTEM_BOOT_TIME algorithm. Commands like uptime, w, and who now tick realistically and accurately reflect the attacker's true login IP and session duration.

Backend Caching & Optimization: Implemented selective cache invalidation to drastically reduce AI latency. When an attacker modifies a file, the router intelligently flushes only the affected paths from the cache.

Intelligent File Inheritance: Engineered logic within file-creation handlers to ensure any new nodes automatically inherit the simulated UID/GID of the active attacker session, further cementing the illusion of a real Linux box.
