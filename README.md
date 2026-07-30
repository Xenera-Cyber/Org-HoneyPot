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
1. **Integrated React Dashboard (`UIprogress/dashboard-integrated`)**
   - Designed a comprehensive modern frontend using React, TypeScript, and Vite.
   - Features real-time event logs, active sessions list, geographic severity visualization map, and detailed command execution timelines.
   - Includes a settings control panel to modify threat engine levels, AI model options, temperatures, and toggle deception pipeline layers dynamically.

2. **Dynamic Configuration System (`xynera-ai/dynamic_config.json`)**
   - Implemented runtime configuration reload for the AI Backend.
   - Allows dynamically setting models (e.g. `llama-3.1-8b-instant`), temperatures, max response limits, and toggling RAG / Guardrails systems globally on-the-fly without service restarts.

3. **Session-Level Threat Engine & Scoring**
   - Integrated command-by-command real-time threat analysis scoring within the `xynera-ai` API backend.
   - Returns cumulative threat scores and intent classification parameters to the honeypot (`xynera-honey`) to profile attacker interest levels (reconnaissance, privilege escalation, malware deployment) dynamically and save session details for visual frontend analytics.

AYUSH CONTRIBUTION
# 🔹 Attack Analyzer (attack_analyzer.py)

## 📖 Overview

The **Attack Analyzer** is the first security analysis layer of the AI-Powered SSH Honeypot. It examines every command executed by an attacker, identifies the type of activity being performed, and assigns an appropriate threat score. The generated information helps other modules understand attacker behavior and respond accordingly.

Rather than relying on complex machine learning models, the module uses lightweight rule-based detection, making it fast, reliable, and easy to maintain while supporting future expansion with additional attack patterns.

---

## 🎯 Objectives

| Objective | Description |
|-----------|-------------|
| Command Analysis | Inspect every command executed by the attacker. |
| Attack Classification | Categorize commands into predefined attack types. |
| Threat Scoring | Assign a severity score for each detected attack. |
| Module Integration | Provide analysis results to other honeypot modules. |
| Scalability | Easily extend detection rules for new attack techniques. |

---

## ⚙️ Workflow

```text
                 Attacker Command
                        │
                        ▼
              Normalize Command
                        │
                        ▼
          Compare with Detection Rules
                        │
                        ▼
           Identify Attack Category
                        │
                        ▼
             Calculate Threat Score
                        │
                        ▼
      Forward Result to Other Modules
```

---

## 📂 Attack Categories

| Category | Purpose | Example Commands |
|----------|---------|------------------|
| 🔍 Reconnaissance | Collect system information | `ls`, `pwd`, `whoami`, `uname` |
| 📁 Directory Navigation | Explore directories | `cd` |
| 🔑 Credential Enumeration | Access sensitive files | `cat /etc/passwd` |
| 📥 Malware Download | Download payloads | `wget`, `curl` |
| 📤 File Transfer | Copy files between systems | `scp` |
| 🔓 Privilege Escalation | Gain elevated permissions | `sudo`, `su`, `chmod` |
| 🌐 Lateral Movement | Connect to remote systems | `ssh` |
| 💻 Reverse Shell | Create remote shell access | `nc`, `bash -i` |
| ❓ Unknown | Unrecognized activity | Any unmatched command |

---

## 📊 Threat Score Matrix

| Threat Level | Score |
|-------------|------:|
| Low | 5–20 |
| Medium | 60–80 |
| High | 90–95 |
| Critical | 100 |

---

## 🧩 Core Functions

| Function | Description |
|----------|-------------|
| `classify(command)` | Identifies the attack category based on command patterns. |
| `threat_score(attack_type)` | Returns the predefined severity score for the detected attack. |

---

## 🔗 Module Integration

```text
                     server.py
                         │
                         ▼
             attack_analyzer.py
              │       │        │
              ▼       ▼        ▼
         logger.py session_manager.py
                         │
                         ▼
                deception_engine.py
```

---

## ⭐ Key Features

| Feature | Benefit |
|---------|---------|
| Rule-Based Detection | Fast and efficient attack classification. |
| Threat Scoring | Measures attack severity consistently. |
| Lightweight Design | Minimal processing overhead. |
| Modular Architecture | Easy to extend with new detection rules. |
| Centralized Analysis | Provides standardized output to all modules. |
| Easy Maintenance | Detection rules can be updated independently. |

---

## 📌 Summary

The **Attack Analyzer** acts as the intelligence core of the honeypot's detection layer. By converting attacker commands into meaningful attack categories and threat scores, it enables accurate logging, session tracking, and adaptive deception while maintaining a lightweight and extensible architecture.

# 🔹 Malware Detector (malware_detector.py)

## 📖 Overview

The **Malware Detector** module is responsible for safely simulating malware-related activities inside the SSH Honeypot. Instead of performing actual downloads or file transfers, it generates realistic terminal outputs for commonly used commands such as `wget`, `curl`, and `scp`. This allows attackers to believe their actions were successful while ensuring the host system remains completely isolated and secure.

The module validates attacker-supplied targets using lightweight syntax checks without making DNS lookups, HTTP requests, or outbound network connections. By producing convincing command outputs, it strengthens the deception capabilities of the honeypot while preventing any real malware execution. :contentReference[oaicite:0]{index=0}

---

## 🎯 Objectives

| Objective | Description |
|-----------|-------------|
| Malware Simulation | Emulate malware download commands without real execution. |
| Safe Environment | Prevent outbound network communication from the honeypot. |
| Realistic Responses | Generate believable Linux terminal outputs. |
| Target Validation | Verify URLs and hostnames using syntax checks. |
| Deception Support | Keep attackers engaged with convincing responses. |

---

## ⚙️ Workflow

```text
                Attacker Command
                       │
                       ▼
               Extract Target
                       │
                       ▼
              Validate Target
                 │          │
          Valid  │          │ Invalid
                 ▼          ▼
     Generate Simulation   Return Error
                 │
                 ▼
      Return Simulated Output
```

---

## 📂 Supported Commands

| Command | Purpose | Simulated Response |
|---------|---------|--------------------|
| `wget` | Download remote files | Download progress, speed, completion message |
| `curl` | Retrieve remote content | Transfer statistics and progress output |
| `scp` | Secure file transfer | File transfer summary with completion details |

---

## 🧩 Core Functions

| Function | Description |
|----------|-------------|
| `extract_target(command)` | Extracts the target URL or filename from the attacker command. |
| `is_valid_target(target)` | Validates the syntax of URLs and hostnames. |
| `handle_wget(command)` | Simulates Linux `wget` output. |
| `handle_curl(command)` | Simulates Linux `curl` transfer output. |
| `handle_scp(command)` | Simulates secure file transfer without copying files. |

---

## 🔗 Module Integration

```text
               attack_analyzer.py
                        │
                        ▼
              deception_engine.py
                        │
                        ▼
             malware_detector.py
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
     command_router.py       Simulated Output
```

---

## ⭐ Key Features

| Feature | Benefit |
|---------|---------|
| Safe Malware Simulation | Prevents real malware execution. |
| No Outbound Traffic | Blocks external network communication. |
| Dynamic Output | Uses randomized values for realistic responses. |
| URL Validation | Accepts only syntactically valid targets. |
| Lightweight Design | Fast execution with minimal overhead. |
| Modular Architecture | Easy to extend with additional download utilities. |

---

## 💡 Highlights

- Simulates **`wget`**, **`curl`**, and **`scp`** commands without contacting external systems.
- Produces realistic Linux terminal outputs using randomized values.
- Performs only syntax validation to maintain complete isolation.
- Integrates seamlessly with the **Deception Engine** to enhance attacker engagement.
- Prevents attackers from using the honeypot as a relay for malicious activities.

---

## 📌 Summary

The **Malware Detector** enhances the realism of the AI-Powered SSH Honeypot by safely emulating malware download and file transfer activities. Through realistic terminal simulations, secure validation, and seamless integration with the deception engine, it keeps attackers engaged while ensuring the underlying system remains fully protected and isolated. :contentReference[oaicite:1]{index=1}

---

# 🔹 Deception Engine (deception_engine.py)

## 📖 Overview

The **Deception Engine** is responsible for generating intelligent and realistic responses based on the attacker's actions. After an attack is classified, this module determines whether a custom deceptive response should be returned or if the command should continue through the normal execution flow.

It also maintains a lightweight attacker profile for each active session, ensuring interactions remain consistent and realistic throughout the attack. This modular design allows the honeypot to support future AI-driven deception while keeping the current implementation flexible and easy to extend. :contentReference[oaicite:0]{index=0}

---

## 🎯 Objectives

| Objective | Description |
|-----------|-------------|
| Adaptive Deception | Generate attack-specific responses. |
| Session Profiling | Maintain attacker intent throughout a session. |
| Dynamic Responses | Improve realism using customized outputs. |
| Modular Design | Separate deception logic from command execution. |
| AI Ready | Support future AI and RAG-based enhancements. |

---

## ⚙️ Workflow

```text
              Attacker Command
                     │
                     ▼
         Receive Attack Category
                     │
                     ▼
        Update Attacker Profile
                     │
                     ▼
       Select Deception Handler
             │             │
        Available      Not Available
             │             │
             ▼             ▼
 Generate Response   Continue Normal Flow
             │
             ▼
      Return Final Output
```

---

## 📂 Supported Deception Types

| Attack Type | Response |
|-------------|----------|
| 🔍 Reconnaissance | Simulates realistic system information. |
| 🔑 Credential Enumeration | Generates fake `/etc/passwd` and `/etc/shadow` data. |
| 📥 Malware Download | Delegates to `malware_detector.py`. |
| 🌐 Lateral Movement | Allows network simulation modules to respond. |
| 🖥 Reverse Shell | Placeholder for future implementation. |
| 🔓 Privilege Escalation | Reserved for future adaptive simulation. |

---

## 🧩 Core Functions

| Function | Description |
|----------|-------------|
| `update_profile()` | Stores attacker intent within the active session. |
| `get_dynamic_uptime()` | Generates randomized Linux uptime information. |
| `credential_enumeration_deception()` | Returns simulated credential files. |
| `malware_download_deception()` | Routes download commands to the malware detector. |
| `adapt_response()` | Selects and executes the appropriate deception handler. |

---

## 👤 Attacker Profiling

| Intent | Trigger |
|--------|---------|
| Reconnaissance | Information gathering commands |
| Credential | Access to `/etc/passwd` or `/etc/shadow` |
| Malware | Commands like `wget`, `curl`, or `nc` |

Maintaining these profiles allows the honeypot to produce more consistent and believable responses during an attack session. :contentReference[oaicite:1]{index=1}

---

## 🔗 Module Integration

```text
                attack_analyzer.py
                        │
                        ▼
              deception_engine.py
             │          │           │
             ▼          ▼           ▼
 malware_detector  command_router  session_manager
```

---

## ⭐ Key Features
| Feature | Benefit |
|---------|---------|
| Adaptive Responses | Generates context-aware deception. |
| Session Profiling | Tracks attacker intent during a session. |
| Dynamic System Data | Produces realistic and non-repetitive outputs. |
| Modular Handlers | Easy to add new deception strategies. |
| AI-Ready Design | Supports future intelligent deception. |
| Lightweight Architecture | Maintains performance with minimal overhead. |

---

## 💡 Why This Module Matters
The **Deception Engine** is the heart of the honeypot's realism. Instead of returning static outputs, it adapts responses based on attacker behavior, creating a more convincing environment while safely collecting valuable attack intelligence.

---

## 📌 Summary
The **Deception Engine** bridges attack analysis and response generation by delivering adaptive, attack-aware interactions. Through session profiling, dynamic content generation, and seamless integration with supporting modules, it significantly improves the effectiveness and realism of the AI-Powered SSH Honeypot. :contentReference[oaicite:2]{index=2}


# 🔹 AI Client (`ai_client.py`)

## 📖 Overview

The **AI Client** serves as the communication bridge between the SSH Honeypot and the AI backend. It forwards attacker commands along with session context to the backend, receives AI-generated responses, and returns them to the honeypot. This enables intelligent and context-aware interactions without tightly coupling the honeypot to the AI service.

To ensure reliability, the module continuously monitors backend availability. If the AI service becomes unavailable, it automatically switches to an offline fallback mode and seamlessly restores AI communication once the backend recovers. :contentReference[oaicite:0]{index=0}

---

## 🎯 Objectives

| Objective | Description |
|-----------|-------------|
| AI Communication | Exchange requests and responses with the AI backend. |
| Context Sharing | Send attacker commands and session information for analysis. |
| Health Monitoring | Continuously monitor backend availability. |
| Automatic Recovery | Restore AI communication after backend recovery. |
| Reliable Operation | Ensure uninterrupted honeypot functionality using fallback responses. |

---

## ⚙️ Communication Workflow

```text
            Attacker Command
                    │
                    ▼
            Prepare AI Request
                    │
                    ▼
       Check Backend Availability
             │              │
       Available      Unavailable
             │              │
             ▼              ▼
     Send Request     Return Fallback
             │
             ▼
      Receive AI Response
             │
             ▼
      Validate & Clean Data
             │
             ▼
      Return Final Response
```

---

## 📂 Core Components

| Component | Purpose |
|-----------|---------|
| `send_to_ai()` | Sends attacker requests to the AI backend. |
| `check_ai_backend()` | Verifies backend availability using the health endpoint. |
| `start_health_monitor()` | Starts the background health monitoring thread. |
| `_health_monitor_loop()` | Continuously monitors backend status. |
| `get_offline_fallback()` | Generates fallback responses when the backend is unavailable. |
| `clean_response()` | Removes unnecessary formatting before returning the response. |

---

## ❤️ Backend Health Monitoring

```text
        AI Backend
             │
             ▼
     Health Check (/health)
             │
      ┌──────┴──────┐
      ▼             ▼
   Online        Offline
      │             │
      ▼             ▼
 Use AI        Return Fallback
      │             │
      └──────┬──────┘
             ▼
     Continue Monitoring
```

---

## 🔗 Module Integration

```text
          command_router.py
                  │
                  ▼
             ai_client.py
          │             │
          ▼             ▼
   AI Backend      session_manager.py
          │
          ▼
 attack_analyzer.py
```

---

## ⭐ Key Features

| Feature | Benefit |
|---------|---------|
| AI Backend Integration | Enables intelligent response generation. |
| Health Monitoring | Continuously checks backend availability. |
| Automatic Recovery | Restores AI routing without restarting the server. |
| Offline Fallback | Keeps the honeypot operational during backend failures. |
| Persistent HTTP Session | Reduces communication overhead and improves efficiency. |
| Thread-Safe Design | Supports multiple concurrent attacker sessions safely. |

---

## 🔄 Response Lifecycle

| Stage | Action |
|-------|--------|
| Request | Collect attacker command and session context. |
| Processing | Forward request to the AI backend. |
| Validation | Verify the received response. |
| Cleanup | Remove unnecessary formatting. |
| Delivery | Return the final response to the attacker. |

---

## 💡 Why This Module Matters

The **AI Client** enables intelligent and adaptive interactions by connecting the honeypot with an external AI backend. Its built-in health monitoring, automatic recovery, and offline fallback mechanisms ensure reliable operation even during temporary backend failures, making the system resilient and scalable.

---

## 📌 Summary

The **AI Client** provides secure and reliable communication between the honeypot and the AI backend. Through continuous health monitoring, thread-safe request handling, automatic failover, and seamless recovery, it ensures uninterrupted AI-assisted deception while maintaining a modular architecture. :contentReference[oaicite:1]{index=1}

# 🔄 Overall System Workflow

The AI-Powered SSH Honeypot follows a modular workflow where each component performs a dedicated task while collaborating to provide a realistic and secure deception environment.

```text
                    Attacker
                        │
                        ▼
               SSH Connection
                        │
                        ▼
                  server.py
                        │
                        ▼
            attack_analyzer.py
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
 logger.py      session_manager.py  deception_engine.py
                                        │
                        ┌───────────────┴───────────────┐
                        ▼                               ▼
            malware_detector.py                command_router.py
                                                        │
                                                        ▼
                                                   ai_client.py
                                                        │
                                                        ▼
                                                   AI Backend
                                                        │
                                                        ▼
                                              Intelligent Response
```

---

# ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔍 Rule-Based Attack Detection | Classifies attacker commands into predefined attack categories. |
| 📊 Threat Scoring | Assigns severity scores based on attacker behaviour. |
| 🎭 Adaptive Deception | Generates realistic responses to mislead attackers. |
| 📥 Malware Simulation | Safely emulates malware download and transfer commands. |
| 🤖 AI Integration | Uses an external AI backend for intelligent response generation. |
| ❤️ Health Monitoring | Continuously checks AI backend availability. |
| 🔄 Automatic Recovery | Restores AI communication without restarting the server. |
| 📜 Session Management | Maintains attacker history and behavioural profiles. |
| 📝 Comprehensive Logging | Records attacker commands, sessions, and threat information. |
| ⚡ Multi-Client Support | Handles multiple attacker sessions concurrently. |

---

# 📂 Module Overview

| Module | Responsibility |
|--------|----------------|
| `attack_analyzer.py` | Detects attack type and assigns threat scores. |
| `malware_detector.py` | Simulates malware downloads and secure file transfers. |
| `deception_engine.py` | Generates adaptive and attack-aware deceptive responses. |
| `ai_client.py` | Communicates with the AI backend and manages failover. |

---

# 🚀 Future Enhancements

- 🧠 AI-driven adaptive deception using attacker history.
- 🌐 Enhanced network simulation for lateral movement attacks.
- 🔐 Interactive privilege escalation scenarios.
- 📈 Real-time attack visualization dashboard.
- ☁️ Cloud-based threat intelligence integration.
- 📊 Advanced analytics and reporting.
- 🤖 Support for multiple AI models and personalities.

---

# 📌 Conclusion

The **AI-Powered SSH Honeypot** combines rule-based attack detection, adaptive deception, malware simulation, and AI-assisted decision making to create a realistic yet secure environment for studying attacker behaviour. Its modular architecture ensures each component remains independent, scalable, and easy to maintain while collectively providing an effective platform for threat analysis and cybersecurity research.

---

## 👨‍💻 Technologies Used

| Category | Technologies |
|----------|--------------|
| Language | Python 3 |
| Networking | Socket Programming |
| AI Backend | FastAPI |
| Communication | REST API |
| Concurrency | Threading |
| Logging | Python Logging |
| Security | SSH Honeypot |
| AI Concepts | RAG, LLM Integration |
| Platform | Linux / Windows |