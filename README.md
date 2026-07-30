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
## My Contribution — Shatakshi Agrawal

This section documents everything I personally worked on during this internship, from environment setup through to performance optimization. Every fix listed below was **verified by actually running the code** (real socket server, real client connections, real test cases) — not just written and assumed to work.

### Table of Contents
1. [Environment Setup & Initial Debugging](#1-environment-setup--initial-debugging)
2. [Systematic Command Testing](#2-systematic-command-testing)
3. [Root-Cause Bug Fixes in `fake_network.py`](#3-root-cause-bug-fixes-in-fake_networkpy)
4. [Dynamic Session Identity & Prompt Rendering](#4-dynamic-session-identity--prompt-rendering)
5. [Service State Management](#5-service-state-management)
6. [AI Backend Integration & Environment Setup](#6-ai-backend-integration--environment-setup)
7. [AI Response Caching (Performance Optimization)](#7-ai-response-caching-performance-optimization)
8. [Advanced Command Simulation (`fake_advanced.py`)](#8-advanced-command-simulation-fake_advancedpy)
9. [Git Branch & Baseline Management](#9-git-branch--baseline-management)
10. [Bugs Fixed — Summary Table](#10-bugs-fixed--summary-table)

---

## 1. Environment Setup & Initial Debugging

- Set up the full project environment on Kali Linux, including Python and all required dependencies.
- Set up a dedicated **Ubuntu 26.04 VM in VirtualBox** as a second testing environment — installed the OS, and diagnosed a `vmwgfx` graphics driver crash on boot (`This configuration is likely broken`) by identifying it as a known VirtualBox/guest-graphics-driver incompatibility, then resolved it by switching the VM's graphics controller and adjusting video memory settings.
- Explored VirtualBox networking modes (NAT vs. host IP `10.0.2.15`) to understand why the Ubuntu VM wasn't directly reachable from outside, and used that understanding to run the honeypot server and a test client together correctly for cross-machine testing scenarios.
- Got `server.py` running and listening on port `2222`, then connected as a simulated attacker via `netcat` to begin functional testing.

---

## 2. Systematic Command Testing

Tested every major honeypot command against **three scenarios** — a known-good domain, a second known-good domain, and a deliberately invalid/non-existent domain — to make sure both success and failure paths behaved correctly:

`netstat`, `netstat -tulpn`, `ss`, `ifconfig`, `ip addr`, `ping`, `dig`, `nslookup`, `host`, `traceroute`, `ssh`, `telnet`, `ftp`

This testing pass is what surfaced the five bugs documented in the next section — I didn't just run commands and move on, I compared outputs across related commands and across repeated runs to catch inconsistencies.

---

## 3. Root-Cause Bug Fixes in `fake_network.py`

Testing surfaced **five real inconsistencies** where the honeypot's fake responses contradicted each other or behaved illogically — exactly the kind of thing that would tip off an attentive attacker that they're inside a honeypot.

| # | Bug | Evidence |
|---|-----|----------|
| 1 | `traceroute` showed working intermediate hops but the final hop *always* said "No route to host," even to a domain that resolved fine everywhere else | 
| 2 | `ssh` gave contradictory errors in the same session — "Host unreachable" twice, then a completely different "Permission denied" on the third try | 
| 3 | `dig`, `host`, and `nslookup` returned **three different results** for the exact same domain — two different fake IPs and one "domain doesn't exist" | 
| 4 | `ping` on a genuinely invalid/made-up domain still returned successful replies with real-looking latency | 
| 5 | `dig` on the same invalid domain also resolved it to a fake IP instead of failing | 

**Root cause:** every function (`dig`, `host`, `nslookup`, `ping`, `traceroute`, `ssh`) was independently generating its own random response with no shared logic — so nothing was guaranteed to agree.

**Fix:** built a single shared DNS resolver so every command consults the *same* source of truth for a given domain, and — critically — backed it with a **real DNS lookup** (via Python's `socket` module) rather than a hardcoded whitelist, so genuinely valid domains work and genuinely invalid ones consistently fail, without needing to maintain a manual list:

```python
def _resolve_target(host):
    """
    Return (display_name, ip_address) for any host argument passed to a
    network command. Literal IPs pass through unchanged; hostnames are
    resolved through the shared DNS cache so the same name always maps
    to the same address.
    """
    host = host.strip()
    if _is_ipv4(host):
        return host, host
    return host, _resolve_domain(host)
```

Beyond the root-cause fix, I built out/refined realistic simulation logic across the full command set in `fake_network.py` so the honeypot's network responses hold up under sustained attacker interaction rather than just looking right on a single call:

- **`traceroute`** — randomized hop count, per-hop jitter, occasional `* * *` timeouts, and a probabilistic "does it actually reach the destination" outcome instead of a fixed always-fail last hop.
- **`ssh` / `scp`** — weighted random outcomes (connection refused / timed out / no route to host / full password-prompt-then-denied flow) so repeated attempts feel like a real flaky network rather than one scripted response.
- **`ping`** — variable packet loss and per-packet latency, with proper handling of malformed hostnames.
- **`netstat` / `netstat -tulpn` / `ss`** — driven off one shared `SERVICES` table (proto/address/port/PID/program) so all three commands can never drift out of sync with each other or with `service_manager.py`.
- **`ifconfig` / `ip addr`** — realistic byte/packet counters and consistent MAC/IPv6-link-local values shared across both commands.
- **`telnet` / `ftp`** — probabilistic outcomes ranging from connection refusal through to a believable login banner (Ubuntu login prompt / vsFTPd banner).
- **`dig` / `nslookup` / `host`** — all backed by the same DNS cache described above.

**Verified fixed** — same domain now returns the same IP across `dig`, `host`, and `nslookup`, and the invalid domain now fails consistently everywhere

---

## 4. Dynamic Session Identity & Prompt Rendering

**Problem:** the shell prompt (`username@hostname:cwd$`) and identity-revealing commands (`whoami`, `hostname`, `hostnamectl`, `id`, etc.) were **hardcoded** — they never reflected the session's actual identity, which meant the AI backend had no way to drive a consistent, believable persona.

**What I built:**
- Designed and built out `session_manager.py` as the central per-attacker state container — tracking not just identity, but the session's dynamic filesystem, service state, command history, threat scoring, and a `backend_cache` for AI-backend-supplied data — all scoped to one `SessionManager` instance per attacker so nothing ever leaks between sessions.
- Added `username`, `hostname`, `personality`, and `groups` as first-class session state, plus `get_identity()` / `set_identity()` as the single entry point for reading/changing them.
- Added `get_prompt()`, which builds the shell prompt **live** from current session state — no code anywhere is allowed to hardcode `"username@hostname:cwd$"` again.
- Added `_sync_identity_files()`, which keeps `/etc/hostname`, `/etc/hosts`, and `/etc/passwd` inside the simulated filesystem consistent with whatever identity is currently active, so a `cat /etc/passwd` can never contradict what `whoami` just said.
- Added `MultiSessionManager` to support multiple concurrent attacker connections, each with its own isolated `SessionManager` (its own filesystem, services, and identity), and to allow a reconnecting IP to resume its existing session instead of always starting fresh.
- Rewired `whoami`, `groups`, `id`, `users`, `hostname`, `hostnamectl`, and `uname -a` in `command_router.py` to read from session identity instead of fixed strings.

**Bug caught along the way:** `hostname` reported `web-prod-01` while `hostnamectl` reported a completely different hostname, `xynera-server` — the same simulated machine giving two different answers about itself in the same session. Fixed by making both read from the same identity source.

I verified this end-to-end by spinning up the real `server.py` in a background thread, connecting a real socket client, and confirming that changing the identity mid-session immediately changed the *very next* prompt and every identity command's output — with zero manual intervention.

---

## 5. Service State Management

Designed `service_manager.py` to track whether each fake service (`nginx`, `mysql`, `redis`, `ssh`, `docker`) is running or stopped, **per session**. Before this, `netstat`, `ss`, `systemctl`, and `service <name> stop` had no shared state — stopping a service through one command had zero effect on what any other command reported.

```python
def netstat_lines(self):
    lines = []
    for name, info in self.services.items():
        if info["status"].startswith("active"):
            lines.append(f"tcp 0.0.0.0:{info['port']} LISTEN")
    return "\n".join(lines)
```

Now `service nginx stop` → `netstat` immediately stops showing port 80, `systemctl status nginx` reports `inactive (dead)`, and `ps` / `ps aux` drop the corresponding process rows — all from one single state change, exactly like a real system.

---

## 6. AI Backend Integration & Environment Setup

- Generated a GROQ API key and configured it via a `.env` file in `xynera-ai/` (kept out of version control).
- Installed and verified the AI backend's dependency stack — `fastapi`, `uvicorn`, `httpx`, `faiss-cpu`, `python-dotenv` — and got `api_server.py` running and listening on port `5000`.
- Hit and resolved a **GitHub push protection** block after `.env` was accidentally staged in an early commit — removed it from tracking with `git rm --cached` and added a proper `.gitignore` so the secret could never be committed again.

---

## 7. AI Response Caching (Performance Optimization)

**Task:** make repeated AI-backend calls faster and reduce backend load, with per-session caching and proper invalidation.

While reviewing the AI fallback path in `command_router.py`, I found that `session_manager.py` already had an unused caching scaffold (`response_exists` / `get_response` / `save_response`) sitting on `backend_cache["responses"]` — built but never wired up. Rather than building a second, competing cache, I wired the existing one into the AI fallback path:

```python
if session_manager.response_exists(command):
    return session_manager.get_response(command)

ai_result = ai_client.send_to_ai(
    ip=session["attacker_ip"], command=command,
    history=session["command_history"], attack_type=attack_type,
    session_id=session["session_id"], cwd=cwd,
)
if ai_result and ai_result.get("backend") == "local" and ai_result.get("reply"):
    session_manager.save_response(command, ai_result["reply"])
    return ai_result["reply"]
```

**Invalidation** comes for free: `_sync_identity_cache()` already clears `backend_cache["responses"]` whenever `set_identity()` runs, so a cached reply generated under one identity/personality can never leak into the session after the identity changes.

**Verified with a mocked AI backend:**

| Run | AI backend calls | Response time |
|---|---|---|
| First time seeing a command | 1 | ~300ms (real network round-trip) |
| Same command repeated | 0 *(cache hit)* | ~11ms |
| Different command | 1 | ~300ms |
| Same command **after identity change** | 1 *(cache correctly invalidated)* | ~300ms |

~28x faster on repeats, with zero risk of serving a stale reply across an identity change.

---

## 8. Advanced Command Simulation (`fake_advanced.py`)

Built a new module to handle three commonly attacker-abused Linux utilities with realistic, GNU-Coreutils-accurate behaviour that the existing static handlers didn't cover:

**`chmod`** — validates both numeric (`777`, `0644`) and symbolic (`u+x`, `g-rw`, `a=rwx`) modes with regex, matches real `chmod`'s silent-on-success behaviour, and specifically simulates a permissions-denied response when an attacker targets sensitive paths like `/etc/shadow` or `/etc/passwd` — a realistic touch that a hardcoded "always succeeds" handler would have missed:

```python
if target.startswith("/root") or target in ["/etc/shadow", "/etc/passwd"]:
    return f"chmod: changing permissions of '{target}': Operation not permitted"
```

**`nc` (netcat)** — distinguishes listener/server mode (`nc -lvp 4444`) from client mode, parses bundled and separate flags for the port, and matches real `nc`'s behaviour of being silent by default and verbose only with `-v` — important because `nc` is a common tool in reverse-shell attempts, so getting its exact silence/verbosity behaviour right matters for believability.

**`get_common_error()`** — a centralized helper for consistent bash-style error formatting (`command not found`, `Permission denied`, `No such file or directory`, `Is a directory`) so every command in the honeypot reports errors in the exact same format a real shell would, instead of each handler inventing its own error text.

---

## 9. Git Branch & Baseline Management

- Managed my working branch (`shatakshi-integration`) through multiple rounds of merging the team's evolving baselines (`hriday/baseline-v3.1` → `v3.3`) — resolving merge conflicts in `command_router.py`, `deception_engine.py`, `fake_process.py`, and `server.py` without ever touching `main` or a teammate's branch.
- Produced a Data Flow Diagram (Level 0 + Level 1) documenting the honeypot's overall architecture for the team.

---

## 10. Bugs Fixed — Summary Table

| # | Component | Bug | Status |
|---|-----------|-----|--------|
| 1 | `fake_network.py` | `traceroute` contradicted itself (working hops, dead destination) | ✅ Fixed |
| 2 | `fake_network.py` | `ssh` gave contradictory errors across attempts | ✅ Fixed |
| 3 | `fake_network.py` | `dig` / `host` / `nslookup` disagreed on the same domain | ✅ Fixed |
| 4 | `fake_network.py` | `ping` succeeded on invalid domains | ✅ Fixed |
| 5 | `fake_network.py` | `dig` resolved invalid domains to a fake IP | ✅ Fixed |
| 6 | `command_router.py` | `hostname` and `hostnamectl` reported two different hostnames | ✅ Fixed |
| 7 | `command_router.py` | `whoami`/`groups`/`id`/`users` ignored session identity | ✅ Fixed |
| 8 | `fake_process.py` | `ps aux` showed a stale username after identity change | ✅ Fixed |

---

## Tech Stack

`Python 3` · `Sockets` · `FastAPI` · `Uvicorn` · `GROQ (LLM backend)` · `Git`
