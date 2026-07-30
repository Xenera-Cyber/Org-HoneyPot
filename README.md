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
# 🍯 XYNERA HoneyPot — Core Simulation Engine

> *"A honeypot is only as convincing as its smallest inconsistency."*

This directory holds the beating heart of the XYNERA HoneyPot: four modules that
together simulate a living, breathing Ubuntu 22.04 server — one that talks,
lies, listens, and remembers, all without ever running a single real service.

An attacker who lands here shouldn't be able to find a single seam. Every fake
IP, every fake process, every fake permission error has to agree with every
other fake IP, process, and error — forever, for the whole session. That's
the actual engineering problem these four files solve.

```
┌─────────────────────┐
│   fake_network.py    │  "What does this server look like on the wire?"
│  (Source of Truth)   │  hostname · IP · MAC · open ports · DNS
└──────────┬───────────┘
           │  SERVICES list, DNS cache
           ▼
┌─────────────────────┐        ┌──────────────────────┐
│  service_manager.py  │◄──────►│  fake_processes.py    │
│  (Session Memory)    │        │  (Process Mirror)     │
│  running / stopped   │        │  ps · ps aux           │
└──────────┬───────────┘        └──────────────────────┘
           │  reflected consistently in
           ▼
   netstat / ss / systemctl / ps — all agree, always

┌─────────────────────┐
│  fake_advanced.py     │  "Everything else an attacker types"
│  (Utility Belt)       │  chmod · nc · shared error formatting
└─────────────────────┘
```

---

## 📖 Table of Contents
- [fake_network.py — The Server's Identity Card](#-fake_networkpy--the-servers-identity-card)
- [service_manager.py — The Session's Memory](#-service_managerpy--the-sessions-memory)
- [fake_process.py — The Process Table Mirror](#-fake_processpy--the-process-table-mirror)
- [fake_advanced.py — The Utility Belt](#-fake_advancedpy--the-utility-belt)
- [How It All Fits Together](#-how-it-all-fits-together)

---

## 🌐 `fake_network.py` — The Server's Identity Card

Think of this file as the **honeypot's passport**. It decides, once and for
all, who this fake machine claims to be — and then never contradicts itself.

**Fixed identity constants:**
- Hostname (`web-prod-01`), IP, netmask, broadcast, MAC, IPv6 link-local — all
  hardcoded so every command that reveals network identity tells the *same*
  story.
- `SERVICES`: a single shared list of `(proto, address, port, pid, program)`
  tuples — the **one and only source of truth** for what's "listening" on
  this box. `netstat`, `netstat -tulpn`, `ss`, and `service_manager.py` all
  read from this same list, so nothing can ever drift out of sync.

**The DNS illusion — `_resolve_domain()` / `_DNS_CACHE`:**
Instead of generating a random IP every time an attacker looks up a domain,
this uses a **seeded random generator** (`random.Random(domain_name)`) so a
domain always resolves to the *same* fake IP for the life of the process —
then caches it. Ask for `evil.com` twice, get the same answer twice. Realism
through consistency, not randomness.

**Command simulations included:**

| Category | Commands | What they simulate |
|---|---|---|
| Discovery | `netstat()`, `netstat_tulpn()`, `ss()` | Listening ports + live connections, service-aware |
| Interfaces | `ifconfig()`, `ip_addr()` | eth0/lo interface details, byte/packet counters |
| Lateral movement | `ssh()`, `scp()`, `telnet()`, `ftp()` | Realistic failure modes (refused / timeout / no route / bad auth) with weighted randomness |
| Reachability | `ping()`, `traceroute()` | Randomized latency, packet loss, and hop behavior |
| DNS | `dig()`, `nslookup()`, `host()` | Full DNS tool output, backed by the shared cache |

The clever bit: **every one of these accepts a `service_manager`**, so if an
attacker stops `nginx` mid-session, `netstat` immediately stops showing port
80 — no restart, no reload, just instant, believable consistency.

---

## 🧠 `service_manager.py` — The Session's Memory

If `fake_network.py` is the passport, this is the **short-term memory** of
one specific attacker's visit.

A honeypot that forgets what the attacker just did (e.g., they run
`service nginx stop`, and five commands later `nginx` mysteriously
reappears) breaks the illusion instantly. `ServiceManager` exists to make
sure that never happens.

**How it works:**
- One `ServiceManager` instance = one attacker session, fully isolated from
  every other concurrent session.
- On creation, it deep-copies default service states (`active (running)`)
  built directly from `fake_network.SERVICES` — so port numbers and PIDs
  can *never* disagree between the two files.
- Every service action an attacker can type is covered:
  - `start()`, `stop()`, `restart()` → backing state machine
  - `handle_service_command()` → the actual `service <name> {start|stop|restart}` CLI verb
  - `systemctl_status()` / `systemctl_overview()` → systemd-style status output
  - `netstat_lines()`, `netstat_tulpn_lines()`, `ss_lines()` → alternate rendering paths kept in lockstep with `fake_network.py`

**Why this matters for the honeypot's credibility:** an attacker probing with
`service mysql stop` → `netstat` → `ps aux` → `systemctl status mysql` should
get four *different-looking* commands that all tell the *same* story. That
cross-command consistency is the whole point of this module's existence.

---

## 🧬 `fake_process.py` — The Process Table Mirror

This file answers the question: *"If I stopped a service, would the process
table actually notice?"*

**`ps()` and `ps_aux()`** render Linux-realistic process listings —
`systemd`, `kthreadd`, `cron`, `rsyslogd`, `fail2ban-server`, `mysqld`,
`nginx` (dual worker/master rows, just like real nginx) — but each
service-backed row is **conditionally shown** via `_service_active()`,
which asks the session's `ServiceManager` whether that program is currently
running.

- No `ServiceManager` supplied → everything shows as running (safe default
  for standalone/offline calls).
- `ServiceManager` supplied → a stopped service's row **quietly disappears**,
  and reappears with its *original PID* if restarted — exactly how a real
  respawned daemon would behave with a fixed init entry.

**Bug fix baked in:** `ps_aux()` takes a live `username` parameter instead of
hardcoding `"ubuntu"`, so the attacker's own shell row (`bash`, `ps aux`)
always reflects whoever is *actually* logged in during that session — even
after identity/session changes mid-engagement.

---

## 🧰 `fake_advanced.py` — The Utility Belt

The catch-all for commands that don't need a whole module of their own, but
still need to feel authentically Linux.

- **`chmod(args)`** — Full GNU Coreutils-style parsing:
  - Validates both **numeric** (`chmod 755`) and **symbolic** (`chmod u+x`)
    modes via regex, rejecting malformed input the same way real `chmod`
    does.
  - Returns realistic `Operation not permitted` errors for sensitive paths
    (`/root`, `/etc/shadow`, `/etc/passwd`) — because a honeypot that lets
    attackers "successfully" chmod `/etc/shadow` gives the game away
    instantly.
  - Silent on success, matching real Unix philosophy.

- **`nc(args)`** — Netcat client *and* listener simulation:
  - Detects listener mode (`-l`) vs client mode, parses bundled flags like
    `-lvp 4444`, and returns the right flavor of silence or verbose output
    (`Listening on [0.0.0.0]...`, `Connection ... succeeded!`) depending on
    flags — covering the classic reverse-shell / port-scan patterns
    attackers actually type.

- **`get_common_error(command, target, error_type)`** — A tiny but important
  **shared error dictionary** (`not_found`, `permission_denied`, `no_file`,
  `is_directory`) so that *every* command across the entire honeypot returns
  bash-identical error phrasing instead of each command inventing its own
  slightly-different wording.

---

## 🔗 How It All Fits Together

1. **`fake_network.py`** declares the server's identity and its list of
   "real" services — the immutable ground truth.
2. **`service_manager.py`** layers **session-specific state** on top of that
   truth: who stopped what, and when, for *this* attacker only.
3. **`fake_process.py`** reflects that state into `ps`/`ps aux`, so the
   process table always matches the network table.
4. **`fake_advanced.py`** rounds out the illusion with the everyday
   utility commands (`chmod`, `nc`) and a shared error vocabulary that keeps
   every module speaking the same "bash dialect."

The result: an attacker can run `netstat`, `ss`, `ps aux`, `systemctl
status nginx`, and `chmod 777 nginx.conf` in any order, from any session,
and never once catch the honeypot contradicting itself.

---
