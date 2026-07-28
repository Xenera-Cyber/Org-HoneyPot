# 🐝 Xynera – Honey for Hackers

---

## ⚙️ Run the System (Backend + Frontend)

### 🔹 Step 1: XYNERA-AI (AI Backend)

| Step         | Command                           |
| ------------ | --------------------------------- |
| Go to folder | `cd xynera-ai`                    |
| Create env   | `python -m venv venv`             |
| Activate env | `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac) |
| Install deps | `pip install -r requirements.txt` |
| Run server   | `python api_server.py`            |

---

### 🔹 Step 2: XYNERA-HONEYPOT (Honeypot Service)

| Step         | Command                           |
| ------------ | --------------------------------- |
| Go to folder | `cd xynera-honey`                 |
| Create env   | `python -m venv venv`             |
| Activate env | `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac) |
| Install deps | `pip install -r requirements.txt` |
| Run server   | `python server.py`                |

---

### 🔹 Step 3: XYNERA-UI (React Dashboard)

| Step         | Command                           |
| ------------ | --------------------------------- |
| Go to folder | `cd UIprogress/dashboard-integrated` |
| Install deps | `npm install`                     |
| Run server   | `npm run dev`                     |

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

---

//Updates from AI & UI integration team (Author- Vidit):

1. **RAG Engine (`xynera-ai/rag_engine.py`)**
   - Built the Retrieval-Augmented Generation engine from scratch powering all AI deception responses.
   - Implemented local command simulation layer (pwd, whoami, echo, chmod, etc.) to bypass LLM calls for common commands — reducing latency to near-zero for ~40% of attacker commands.
   - Added async connection pooling (`httpx.AsyncClient`), in-memory response cache keyed on `(command, user, host, cwd)`, and a 6-attempt exponential back-off retry loop with Groq 429 rate-limit parsing.
   - Built `clean_llm_output()` regex post-processor to strip markdown fences, echoed prompts, and trailing shell characters from LLM output.
   - Integrated per-persona filesystem state injection (3 honeypot personas: ubuntu-server, staging-api-01, backup-node-02) into the LLM prompt.

2. **Knowledge Base (`xynera-ai/knowledge_base.py`)**
   - Expanded the static command reference library to ~35 Linux commands with realistic sample outputs.
   - Added 30+ high-value sensitive file documents (SSH keys, `/etc/shadow`, AWS credentials, `.env`, Stripe keys, Kubernetes YAML, database SQL dump, Nginx/Redis/PostgreSQL configs).
   - Added 5 corporate email decoy documents and 21 internal markdown documents (security reports, meeting notes, incident reports, HR docs, contracts) — all dynamically seeded with per-session employee names.

3. **Data Generator (`xynera-ai/data_generator.py`)**
   - Built the complete per-session fake corporate identity generator from scratch.
   - Generates a consistent 25-person employee roster, 6 departments, 5 projects, client/vendor lists, infrastructure YAML, fake credentials (RSA SSH keys, AWS keys, bcrypt shadow hashes, Kubernetes kubeconfig, Stripe secrets), SQL database dumps, corporate emails, and 21 internal markdown documents — all mutually consistent within a session.
   - Uses weekday-based seeding so data rotates daily but stays deterministic within a day.

4. **API Server (`xynera-ai/api_server.py`)**
   - Designed and implemented the 8-step AI processing pipeline exposed at `POST /process`:
     Classifier → Session Data → Attacker Profile → Threat Engine → Personality → RAG Engine → Predictive Engine → Multi-type Logger.
   - Defined `ProcessRequest` and `ProcessResponse` Pydantic models with full field coverage.
   - Wired `predictive_intelligence()` output into both the API response and centralised log for dashboard consumption.

5. **Vector Store (`xynera-ai/vector_store.py`)**
   - Built a custom TF-IDF vectorizer (no sklearn dependency) + FAISS `IndexFlatIP` pipeline for fast knowledge-base retrieval.
   - Implemented disk cache with MD5 hash invalidation so the index rebuilds automatically when the knowledge base changes.
   - Built a custom `TFIDFVectorizer` class from scratch (no sklearn dependency) with stopword removal, IDF weighting, and L2 normalisation, backed by FAISS `IndexFlatIP` (cosine similarity) for fast nearest-neighbour retrieval across the entire knowledge base.
   - Implemented disk cache with MD5 hash invalidation — index rebuilds automatically when the knowledge base changes; loaded instantly from `.cache/` on disk when unchanged.
   - Added a 40-entry `COMMAND_EXPANSIONS` synonym dictionary (e.g. `df` → `"disk free space usage filesystem"`) to boost recall for abbreviated Linux commands, with command names weighted 3× in the index.
   - Added vocabulary coverage ratio guard: queries with less than 50% token coverage in vocabulary skip FAISS entirely, preventing false-positive matches on unknown commands.

6. **Config (`xynera-ai/config.py`)**
   - Replaced hard `python-dotenv` dependency with a pure-Python `.env` file parser (strips comments and quotes), making the backend runnable on any Python 3.9+ environment without extra packages.
   - Implemented `get_dynamic_config()` — deep-merges `dynamic_config.json` over safe defaults on every API call so model, temperature, RAG, and guardrail settings take effect immediately without any service restart.

7. **Classifier (`xynera-ai/classifier.py`)**
   - Implements `classify_command()` — the first step of the API pipeline. Analyses every attacker command via keyword-pattern matching and assigns one of 9 attack categories: `Reconnaissance`, `Malware Download Attempt`, `Permission Manipulation`, `Reverse Shell Attempt`, `SQL Injection Attempt`, `Defense Evasion`, `Persistence Creation`, `Privilege Escalation Attempt`, `Malware Execution Attempt`.
   - Maintains a per-IP `AttackerSession` object that accumulates a cumulative risk score and automatically escalates the threat level through `LOW → MEDIUM → HIGH → CRITICAL` thresholds (12 / 25 / 40) as more commands are executed.
   - Returns a full classification dict (`session_id`, `attack_type`, `risk_score`, `threat_level`, `confidence`, `timestamp`) consumed downstream by the attacker profile, threat engine, and logger.

8. **Attacker Profile (`xynera-ai/attacker_profile.py`)**
   - Maintains a global in-memory `profiles` dict keyed on attacker IP, tracking all commands, directories visited, recon count, persistence attempts, files and services accessed, and success/failure counts per session.
   - `update_profile()` is called before the AI response; `update_profile_response()` is called after to record whether the attacker received a useful or error reply.
   - `get_detailed_profile()` computes three structured scores used by the Predictive Engine and Dashboard:
     - **Curiosity Score** — weighted sum of unique commands, directories visited, recon activity, and persistence attempts (capped at 100).
     - **Engagement Score** — weighted sum of session duration, command volume, successful commands, files and services accessed (capped at 100), with `LOW / MEDIUM / HIGH` engagement level.
     - **Behaviour Profile** — qualitative labels (LOW / MEDIUM / HIGH) for persistence, interaction depth, and session complexity.
   - `get_session_data()` — generates and caches per-session fake corporate data using an MD5-derived seed from the session_id, ensuring all documents, credentials, and employee names are consistent throughout the entire attacker session.

9. **Threat Engine (`xynera-ai/threat_engine.py`)**
   - Implements `ThreatEngine` class with configurable base weights for 12 attack categories (Reverse Shell Attempt = 22, C2 / Backdoor = 25, System Destruction = 30) and a rolling deque of the last 5 attack types per IP.
   - Applies **sequence multipliers** to escalate scores when dangerous combinations are detected in sequence: Reconnaissance → Malware Download (×1.6), Privilege Enumeration → Privilege Escalation (×1.8), Reverse Shell → C2/Backdoor (×2.0).
   - Returns a threat dict with `score`, `risk_level` (LOW / MEDIUM / HIGH / CRITICAL), `multiplier`, and a colour-coded `severity_indicator` emoji surfaced in the dashboard and log.

10. **Personalities (`xynera-ai/personalities.py`)**
    - Defines 11 distinct honeypot personas (`friendly`, `normal`, `suspicious`, `high_security`, `default`, `newbie`, `developer`, `highvalue`, `corporate`, `banking`, `university`, `cloud`) — each with a unique hostname, username, description, and `response_style` string injected directly into the LLM prompt to shape tone, verbosity, and detail level of every AI response.
    - `get_personality()` automatically selects the active persona based on the current threat level: LOW → friendly (welcoming), MEDIUM → normal (standard), HIGH → suspicious (cautious with warnings), CRITICAL → high_security (restrictive, auditing mode). Legacy call signatures (`ip`, `attack_type`, `score`) are also supported for backward compatibility with the honeypot's command router.

11. **Guardrails (`xynera-ai/guardrails.py`)**
    - `apply_guardrails()` is the final safety gate applied to every AI-generated response before it reaches the attacker — called inside `rag_engine.generate_response()`.
    - Blocks dangerous destructive commands (`rm -rf`, `mkfs`, `dd if=`, `shutdown`, `reboot`, `halt`, `init 0`) by returning a guardrail notice in place of the AI output.
    - Blocks malware-related keywords in the command (`ransomware`, `keylogger`, `exploit`, `payload`, `reverse shell`, `meterpreter`) to prevent the AI from inadvertently providing useful attack assistance.
    - Guards against empty AI responses — ensures the attacker always receives a meaningful reply rather than a blank line that would reveal the deception.
    - Dynamically toggleable at runtime via the `guardrailsEnabled` flag in `dynamic_config.json` without restarting the backend.

12. **Logger (`xynera-ai/logger.py`)**
    - Structured logging module writing all events to `ai_backend.log` using Python's `logging.FileHandler` with `%(asctime)s - %(message)s` format.
    - Exposes four specialised log functions called on every API request:
      - `log_personality_integration()` — records session, command, AI response, selected persona, threat score, and full attacker profile as a JSON object.
      - `log_ai_decision()` — records classification result (attack_type, risk_score, threat_level) per command.
      - `log_ai_analysis()` — records AI decision, confidence score, conversation metadata, prediction result, and risk metrics.
      - `log_centralized_event()` — unified log entry (conversation log, system event, security event, warnings, errors, prediction) parsed by `dashboard_api.py` to power the live dashboard event stream.
    - `make_serializable()` helper safely converts Python `set` objects (used in attacker profiles) to JSON-safe lists before serialisation.

13. **Predictive Engine (`xynera-ai/predictive_engine.py`)**
    - `predictive_intelligence()` — called once per command; uses curiosity score, risk score, and engagement level to forecast: next probable attacker action (Reconnaissance / Credential Access / Privilege Escalation), likely high-value target (Public Directories / Sensitive Files / Admin Credentials), deception success probability (51% / 74% / 92%), and overall session outcome (Low / Medium / High Risk Session).
    - `bait_recommendation()` — identifies the most-accessed honeypot asset and total asset access counts for dashboard bait-tuning analytics.
    - `deception_effectiveness_report()` — produces a summary of the most successful trap, highest engagement session, and AI prediction accuracy percentage.
    - `performance_analytics()` — evaluates live system metrics (response time, CPU, RAM, detection accuracy) and returns an optimisation report with status labels and actionable recommendations.

14. **Dynamic Config (`xynera-ai/dynamic_config.json` & `xynera-honey/dynamic_config.json`)**
    - Created both runtime config files allowing live adjustment of the full AI pipeline without restarting any service.
    - `xynera-ai/dynamic_config.json` controls: `personality` (auto), `model` (llama-3.1-8b-instant), `confidenceThreshold` (85), `temperature` (0.1), `maxContext` (4096), `maxResponseLength` (1024), `ragEnabled` (true), `guardrailsEnabled` (true).
    - `xynera-honey/dynamic_config.json` controls: `maxConcurrentSessions` (50), `sessionTimeoutMinutes` (30), `logRetentionDays` (30), `maxCommandsPerSession` (250), and `sshEnabled / httpEnabled / ftpEnabled` service toggles.
    - Settings are live-editable from the dashboard Settings panel via `PUT /api/config`.

15. **AI Dashboard Integration**
    - **`xynera-honey/ai_client.py`** — Built the honeypot-to-AI bridge with persistent HTTP session pooling (`requests.Session`), a background health-monitor daemon thread polling `/health` every 5s (logs only on state transitions), fast-path offline fallback skipping all network I/O when backend is down, 2-retry loop with 0.5s back-off on `ConnectionError`, and a 5s hard timeout aborting immediately to prevent cascading load.
    - **`xynera-honey/dashboard_api.py`** — Built the full FastAPI dashboard backend with CORS middleware, no-cache HTTP headers, compiled regex log parsing (`LOG_PATTERN`), hash-consistent IP geo-mapping, optional `psutil` CPU/RAM metrics, uptime tracking, and all dashboard endpoints: `/api/stats`, `/api/recent-events`, `/api/attackers`, `/api/geo-map`, `/api/service-status`, `GET /api/config`, `PUT /api/config`.
    - **`UIprogress/dashboard-integrated/`** — Integrated the React/TypeScript/Vite dashboard with real-time event logs, session threat scores, geographic attack-origin map, AI prediction panel, and a live settings panel that writes directly to `dynamic_config.json`.

16. **Security & API Testing (Postman)**
    - Validated all endpoints (`GET /health`, `POST /process`, all `dashboard_api.py` routes) using Postman. Full collection saved at `postman_collection.json`.
    - Tested attack scenarios: reconnaissance, credential access, privilege escalation, network recon, reverse shell commands, and multi-session consistency (same `cat /etc/shadow` with same `session_id` → identical hash output confirmed from cache).
    - Verified guardrails blocked all destructive and malware commands, rate-limit back-off prevented API key exhaustion, offline fallback kept the honeypot responsive during simulated AI backend outages, and live `dynamic_config.json` reload applied model and temperature changes without restart.
