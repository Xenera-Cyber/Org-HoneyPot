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

CONTRIBUTION Ayush
🔹 attack_analyzer.py
Overview

The attack_analyzer.py module is responsible for identifying the type of activity an attacker is performing after executing a command inside the honeypot. Every command received from an attacker is analyzed using predefined rule-based logic. Based on the detected behaviour, the module classifies the command into an attack category and assigns a threat score representing its severity.

This module acts as the first layer of threat analysis within the honeypot and provides information that is later used for session tracking, logging, threat monitoring, and deception.

Objectives

The main objectives of this module are:

Analyze every command executed by the attacker.
Identify the attack category based on command patterns.
Assign a numerical threat score according to the severity of the detected activity.
Provide standardized attack information to other components of the honeypot.
Support future expansion by allowing new attack categories and detection rules to be added easily.
Attack Classification

The module classifies commands into different categories based on predefined detection rules.

Reconnaissance

Reconnaissance represents the initial information-gathering stage of an attack. During this phase, attackers attempt to learn about the operating system, users, running services, network interfaces, and available files.

Commands detected include:

ls
pwd
whoami
id
groups
hostname
users
uname
ifconfig
ip
netstat
ss
ps
nmap
traceroute
whois
dig
nslookup

These commands are classified as Reconnaissance because they primarily collect information rather than modify the system.

Directory Navigation

Commands beginning with cd are classified as Directory Navigation.

Although directory changes are not inherently dangerous, they indicate that an attacker is exploring the file system to locate valuable files or sensitive directories.

Credential Enumeration

The module detects attempts to access Linux credential files such as:

/etc/passwd
/etc/shadow

Accessing these files is a common technique used to identify user accounts or obtain password hashes.

Such commands are classified as Credential Enumeration.

Malware Download

Commands containing:

wget
curl

are classified as Malware Download because these tools are commonly used to download malicious scripts, executables, or payloads from remote servers.

File Transfer

Commands beginning with scp are classified as File Transfer.

These commands indicate that files may be copied between systems, which could be used for malware deployment or data exfiltration.

Privilege Escalation

Commands containing:

sudo
chmod
su

are classified as Privilege Escalation.

These commands suggest that an attacker is attempting to gain elevated permissions or modify access controls.

Reverse Shell Activity

Commands such as:

nc
bash -i
socket

are classified as Reverse Shell Activity.

These commands are commonly associated with establishing remote command execution channels back to the attacker's machine.

Lateral Movement

Commands containing:

ssh

are classified as Lateral Movement.

These commands indicate that an attacker may be attempting to move from one compromised machine to another within a network.

Unknown Activity

If a command does not match any predefined detection rule, it is classified as Unknown.

This ensures that every command receives a valid classification even if it is not explicitly recognized.

Threat Scoring

After determining the attack category, the module assigns a threat score using the shared threat score table.

Attack Type	Threat Score	Description
Reconnaissance	20	Basic information gathering.
Directory Navigation	10	Low-risk exploration of directories.
Credential Enumeration	60	Attempts to access sensitive user information.
Malware Download	90	Possible malware retrieval from external sources.
Malware Preparation	95	High-risk preparation before malware execution.
Malware Execution	100	Critical malware execution activity.
File Transfer	80	Potential malware movement or data transfer.
Privilege Escalation	95	Attempt to gain administrative privileges.
Lateral Movement	80	Attempt to access additional systems.
Destructive Attack	100	Commands capable of severe system damage.
Reverse Shell Activity	100	Remote shell establishment attempt.
Unknown	5	Command not recognized by existing rules.

The threat score allows other components to estimate how dangerous the attacker’s behaviour is and helps prioritize monitoring and reporting.

Workflow
Attacker Command
        │
        ▼
Convert Command to Lowercase
        │
        ▼
Compare Against Detection Rules
        │
        ▼
Identify Attack Category
        │
        ▼
Retrieve Threat Score
        │
        ▼
Return Classification Result
Functions
classify(command)

This function analyzes the attacker’s command after converting it to lowercase. It compares the command against predefined detection rules and returns the corresponding attack category.

Input

Command entered by the attacker.

Output

Attack category as a string.
threat_score(attack_type)

This function retrieves the predefined threat score associated with the detected attack category.

If the attack type is not found in the shared dictionary, the function returns the default score of 5.

Integration with Other Modules

The attack_analyzer.py module is closely integrated with several components of the honeypot:

server.py – Calls the module immediately after receiving an attacker command.
session_manager.py – Stores detected attack types and cumulative threat scores for each session.
logger.py – Records the classified attack type and score in the attack logs.
deception_engine.py – Uses the detected attack category to generate appropriate deceptive responses.
Advantages
Fast rule-based analysis with minimal overhead.
Consistent classification of attacker behaviour.
Centralized threat scoring for all modules.
Easy to maintain and extend with new attack categories.
Provides valuable context for logging, session management, and adaptive deception.


🔹 malware_detector.py
Overview

The malware_detector.py module is responsible for simulating malware download and file transfer activities inside the honeypot. Instead of allowing real network communication, it generates realistic terminal outputs that imitate the behaviour of common Linux utilities such as wget, curl, and scp. This allows attackers to believe their commands have executed successfully while ensuring that no actual files are downloaded or transferred.

Unlike a real malware detection engine that scans files for malicious content, this module focuses on safely emulating malware delivery commands to maintain the realism of the honeypot.

Objectives

The primary objectives of this module are:

Simulate malware download commands without making real network connections.
Generate believable Linux terminal outputs for download and transfer utilities.
Validate attacker-supplied URLs and hostnames using safe syntactic checks.
Prevent attackers from triggering outbound network requests from the honeypot.
Support the deception engine by providing realistic malware download responses.
Command Processing

Whenever an attacker executes a download or transfer command, the module performs the following sequence of operations:

Extract the target URL or file path from the command.
Validate the target using syntactic checks.
Generate a realistic command output.
Return the simulated response to the deception engine.

At no point does the module establish an actual network connection.

Target Extraction

The function extract_target() retrieves the last argument from the attacker’s command, assuming it represents the download target.

Examples:

wget http://example.com/payload.sh

Extracted Target:

http://example.com/payload.sh

Another example:

curl https://example.com/test.bin

Extracted Target:

https://example.com/test.bin

If no target is provided, the module returns:

unknown_payload

This ensures that every command produces a valid processing result.

Target Validation

Before generating a simulated response, the module verifies whether the supplied target appears to be a valid URL or hostname.

The validation supports:

HTTP URLs
HTTPS URLs
Bare hostnames

Examples of accepted targets:

http://example.com/file.sh
https://example.com/file.sh
malware.sh

The validation intentionally does not perform DNS resolution, ping operations, or HTTP requests.

This design prevents attackers from abusing the honeypot to communicate with external systems.

Wget Simulation

The handle_wget() function generates a realistic Linux wget download transcript.

The simulated output includes:

Current timestamp
Host resolution
Simulated IP address
Successful TCP connection
HTTP 200 OK response
File size
Download speed
Progress bar
Download completion message

Several values are randomized, including:

Remote IP address
File size
Download speed
Download duration

Randomization ensures that repeated downloads do not produce identical outputs, making the deception more convincing.

If an invalid target is supplied, the function returns an error similar to:

wget: unable to resolve host address

This behaviour closely resembles a real Linux system.

Curl Simulation

The handle_curl() function generates a simulated transfer progress display similar to the Linux curl command.

The response includes:

Total bytes
Download progress
Transfer speed
Completion statistics

If the supplied target is invalid, the function returns:

curl: Could not resolve host

No network communication is performed.

SCP Simulation

The handle_scp() function simulates secure file transfer operations.

Instead of copying files, it returns a realistic transfer summary showing:

Filename
Transfer percentage
File size
Transfer speed
Completion time

This provides attackers with believable feedback while ensuring that the honeypot remains completely isolated.

Workflow
Attacker Command
        │
        ▼
Extract Target
        │
        ▼
Validate URL / Hostname
        │
   ┌────┴────┐
   │         │
Valid      Invalid
   │         │
   ▼         ▼
Generate   Return
Simulation Error Message
   │
   ▼
Return Simulated Output
Function Description
extract_target(command)

This function extracts the final argument from the attacker's command and treats it as the intended download target.

Input

Complete attacker command

Output

Target URL or filename
is_valid_target(target)

Checks whether the supplied target follows the expected syntax for a valid URL or hostname.

The validation is intentionally limited to syntax only.

No real DNS lookup or network request is performed.

handle_wget(command)

Simulates the Linux wget command.

The function produces realistic download messages with randomized file sizes, timestamps, and transfer speeds.

Returns

Simulated terminal output
Target URL
handle_curl(command)

Simulates the Linux curl command.

Produces a transfer progress display without contacting any remote server.

Returns

Simulated terminal output
Target URL
handle_scp(command)

Simulates a successful secure copy operation.

No file transfer occurs.

Returns

Simulated transfer summary
Target path
Integration with Other Modules

The malware_detector.py module works together with several components of the honeypot:

deception_engine.py – Delegates wget and curl commands to this module for realistic malware download simulation.
command_router.py – May use the generated responses when handling attacker commands.
attack_analyzer.py – Identifies malware download commands before they are passed to the deception engine.

Together, these modules create a safe yet convincing simulation of malware delivery.

Advantages
Prevents real malware downloads.
Prevents outbound network communication.
Generates realistic Linux command outputs.
Uses randomized values to improve deception.
Provides consistent behaviour for multiple download utilities.
Keeps the honeypot isolated while maintaining attacker engagement.
Easy to extend with additional download utilities in future versions.


🔹 deception_engine.py
Overview

The deception_engine.py module is responsible for generating intelligent and believable responses based on the attacker's behaviour. It acts as an intermediate layer between the attacker and the normal command execution process. Before a command is processed by the standard command router, the deception engine determines whether a customized deceptive response should be generated.

Unlike static command simulation, this module adapts its responses according to the detected attack type and maintains a lightweight profile of the attacker's intent throughout the session. This makes the honeypot appear more realistic while preparing the architecture for future AI-powered deception.

Objectives

The primary objectives of this module are:

Generate attack-specific deceptive responses.
Maintain a session-specific attacker behaviour profile.
Improve the realism of the honeypot by returning dynamic responses.
Keep attacker interactions consistent throughout a session.
Allow seamless fallback to the standard command router whenever deception is not required.
Provide a modular architecture that can easily support AI and RAG integration in future versions.
Module Architecture

The deception engine operates between the attack analysis layer and the command router.

Attacker Command
        │
        ▼
attack_analyzer.py
        │
        ▼
deception_engine.py
        │
   ┌────┴────┐
   │         │
Deception   No Deception
Generated
   │         │
   ▼         ▼
Return      command_router.py
Response

The attack type detected by attack_analyzer.py determines which deception handler is selected.

Session-Based Attacker Profiling

One of the important features of this module is maintaining an attacker profile for every active session.

The function update_profile() stores attacker behaviour directly inside the session dictionary.

Each session maintains its own independent profile, preventing information from one attacker affecting another.

The current intent categories are:

Reconnaissance
Credential
Malware

For example:

Accessing /etc/passwd or /etc/shadow changes the intent to Credential.
Executing wget, curl, or nc changes the intent to Malware.
All other supported commands are treated as Reconnaissance.

This information can later be used for analytics, reporting, or future AI-based adaptive deception.

Dynamic Uptime Generation

Instead of returning the same output every time an attacker executes the uptime command, the module generates randomized values.

The generated response includes:

Current uptime
Number of active users
System load averages

Each execution produces slightly different values.

Example:

14:23:48 up 37 days, 18:42, 3 users, load average: 0.21, 0.17, 0.08

This prevents attackers from identifying the honeypot through repeated identical outputs.

Reconnaissance Deception

Reconnaissance commands are generally handled by dedicated simulation modules such as:

fake_filesystem.py
fake_process.py
fake_network.py

Therefore, the deception engine only provides special handling for the uptime command.

If the command is not uptime, the function returns None, allowing the command router to continue normal processing.

This approach avoids duplicating functionality already implemented elsewhere.

Credential Enumeration Deception

When attackers attempt to read Linux credential files, the module intercepts these requests before they reach the filesystem.

/etc/shadow

The simulated filesystem does not contain a real shadow file.

Instead of returning an error such as:

No such file or directory

the module generates a believable fake shadow file.

Example:

root:*:19000:0:99999:7:::
ubuntu:*:19000:0:99999:7:::
dev:*:19000:0:99999:7:::

No password hashes are exposed.

/etc/passwd

Unlike /etc/shadow, the simulated filesystem already contains a passwd file.

However, that file is static.

The deception engine dynamically rebuilds /etc/passwd using the current session username.

For example:

root:x:0:0:root:/root:/bin/bash
john:x:1000:1000::/home/john:/bin/bash
dev:x:1001:1001::/home/dev:/bin/bash

This ensures consistency between:

Shell prompt
Current username
Home directory
whoami
/etc/passwd

Such consistency makes the honeypot much more convincing.

Malware Download Deception

Instead of generating download responses directly, the deception engine delegates malware-related commands to malware_detector.py.

Supported commands include:

wget
curl

This separation of responsibilities keeps malware simulation centralized within a single module.

The deception engine simply routes the request and returns the simulated output generated by the malware detector.

Lateral Movement Handling

Commands classified as Lateral Movement currently do not receive custom deception.

The handler returns None.

This allows other components, such as the network simulation module, to generate richer responses.

This design avoids replacing detailed simulations with simpler outputs.

Reverse Shell Handling

A placeholder handler is included for future development.

Planned improvements include:

AI-generated reverse shell responses.
Long-running interactive shell simulation.
Adaptive responses based on attacker behaviour.

Currently, no custom response is generated.

Privilege Escalation Handling

A dedicated placeholder function exists for future privilege escalation simulation.

Potential future capabilities include:

Simulated sudo execution.
Fake permission changes.
AI-generated administrative command responses.
Adaptive privilege escalation behaviour.

At present, the function returns None, allowing normal routing.

Attack Type Dispatcher

The module maintains a centralized dispatcher called DECEPTION_HANDLERS.

This dictionary maps each attack type to its corresponding deception function.

Current mappings include:

Attack Type	Handler
Reconnaissance	reconnaissance_deception()
Credential Enumeration	credential_enumeration_deception()
Malware Download	malware_download_deception()
Lateral Movement	lateral_movement_deception()
Reverse Shell Activity	reverse_shell_deception()
Privilege Escalation	privilege_escalation_deception()

This architecture makes it easy to introduce additional attack categories without modifying the main routing logic.

Main Response Adaptation

The function adapt_response() serves as the entry point of the deception engine.

Its responsibilities include:

Updating the attacker profile.
Checking for special cases such as uptime.
Selecting the correct deception handler.
Returning the generated response.
Returning None when no deception is applicable.

Returning None signals the command router to process the command normally.

Workflow
Attacker Command
        │
        ▼
Receive Attack Type
        │
        ▼
Update Attacker Profile
        │
        ▼
Select Deception Handler
        │
   ┌────┴────┐
   │         │
Handler     No Handler
Returns     Available
Response
   │         │
   ▼         ▼
Return      command_router.py
Response
Function Description
update_profile(command, session)

Maintains a lightweight attacker intent profile within the current session.

Possible intents:

Reconnaissance
Credential
Malware
get_dynamic_uptime()

Generates randomized Linux uptime information to improve realism.

reconnaissance_deception()

Provides deception for reconnaissance commands, currently handling only uptime.

credential_enumeration_deception()

Generates simulated /etc/passwd and /etc/shadow content while keeping responses consistent with the active session.

malware_download_deception()

Delegates malware download simulation to malware_detector.py.

lateral_movement_deception()

Allows normal network simulation modules to handle lateral movement commands.

reverse_shell_deception()

Placeholder for future reverse shell simulation.

privilege_escalation_deception()

Placeholder for future privilege escalation simulation.

adapt_response()

The main controller responsible for selecting and executing the appropriate deception handler based on the detected attack type.

Integration with Other Modules

The deception engine interacts closely with several components:

attack_analyzer.py – Supplies the detected attack category.
command_router.py – Calls adapt_response() before normal command execution.
session_manager.py – Stores attacker intent inside each session.
malware_detector.py – Generates simulated download responses for malware-related commands.
fake_filesystem.py, fake_process.py, and fake_network.py – Handle commands when no specialized deception is required.

This modular integration ensures each component has a clear responsibility while working together to create a believable honeypot environment.

Advantages
Generates attack-aware deceptive responses.
Maintains independent attacker profiles for each session.
Produces dynamic system information to avoid repetitive outputs.
Ensures consistency across simulated system files and user identities.
Separates deception logic from command execution.
Easily extensible through centralized handler mapping.
Ready for future AI, RAG, and adaptive deception integration without major architectural changes.


🔹 ai_client.py
Overview

The ai_client.py module serves as the communication bridge between the honeypot server and the AI backend. Whenever the honeypot receives a command that requires AI-assisted analysis or deception, this module sends the request to the AI backend, processes the response, and returns it to the honeypot.

In addition to communication, the module continuously monitors the health of the AI backend. If the backend becomes unavailable, it automatically switches to a local fallback mode. Once the backend recovers, AI communication is restored automatically without requiring a server restart. This ensures that attacker sessions continue uninterrupted even during backend failures.

Objectives

The primary objectives of this module are:

Establish communication with the AI backend.
Send attacker commands and session information for AI processing.
Receive AI-generated deception responses.
Continuously monitor backend availability.
Automatically recover from backend failures.
Provide a reliable offline fallback mechanism.
Ensure thread-safe communication in a multi-client environment.
Maintain compatibility with the existing honeypot architecture.
Module Architecture

The AI client acts as an intermediary between the honeypot and the AI backend.

Attacker
    │
    ▼
server.py
    │
    ▼
command_router.py
    │
    ▼
ai_client.py
    │
    ▼
AI Backend (/process)
    │
    ▼
AI Response
    │
    ▼
Honeypot

This separation ensures that the honeypot remains independent of the backend implementation while still benefiting from AI-generated responses.

AI Backend Configuration

The module reads backend information from environment variables.

These include:

AI Backend Host
AI Backend Port

Using environment variables allows the backend server to be changed without modifying the source code.

The module automatically constructs the required endpoints:

/process – Handles AI request processing.
/health – Used for backend health monitoring.

This approach improves deployment flexibility across different environments.

Persistent HTTP Session

Instead of creating a new HTTP connection for every request, the module maintains a persistent requests.Session.

This provides several advantages:

Reduces connection overhead.
Improves communication efficiency.
Reuses existing TCP connections.
Supports multiple attacker sessions more efficiently.

Persistent sessions are especially useful when multiple attackers are connected simultaneously.

AI Request Processing

Whenever the honeypot requires AI assistance, the function send_to_ai() prepares a structured request.

The request contains information such as:

Attacker IP address.
Executed command.
Command history.
Attack type.
Additional session data.

This contextual information enables the AI backend to generate more relevant and consistent responses.

Response Processing

After receiving a response from the AI backend, the module validates the returned data before passing it to the honeypot.

The returned information may include:

AI-generated reply.
Detected attack type.
Personality name.
Prediction.
Backend status.
Response time.

The module also cleans the AI response to remove unnecessary Markdown formatting before returning it.

This ensures that the attacker receives clean terminal output.

Backend Health Monitoring

One of the major features of this module is continuous backend health monitoring.

A dedicated background daemon thread periodically checks whether the AI backend is available by sending requests to the /health endpoint.

The monitoring process runs independently of attacker sessions.

This means health checks continue even while multiple clients are interacting with the honeypot.

The monitoring interval is configurable through the HEALTH_CHECK_INTERVAL constant.

Automatic Backend Recovery

The module automatically manages backend availability.

When the Backend is Online
The health monitor marks the backend as available.
Attacker commands are forwarded to the AI backend.
AI-generated responses are returned normally.
When the Backend is Offline
The health monitor detects the failure.
Backend availability is marked as unavailable.
AI requests are skipped.
The honeypot immediately switches to the offline fallback response.

No unnecessary network requests are made while the backend remains unavailable.

When the Backend Recovers

The background health monitor continues checking the backend.

As soon as the backend responds successfully:

Backend availability is restored.
AI routing resumes automatically.
Existing attacker sessions continue normally.
No server restart is required.

This provides seamless recovery from temporary backend failures.

Offline Fallback Mechanism

The module includes a built-in fallback mechanism to ensure uninterrupted operation.

Whenever the backend is unavailable, a standardized fallback response is returned.

The fallback contains:

Backend status
Attack type
Empty AI reply
Personality information
Prediction field
Response time

This guarantees that the honeypot continues responding even when AI services are temporarily unavailable.

Retry Mechanism

Temporary network failures do not immediately terminate AI communication.

The module includes configurable retry logic.

If a connection attempt fails:

Wait for a short delay.
Retry the request.
Repeat until the maximum retry count is reached.

This improves resilience against temporary network instability.

Timeout Handling

Each backend request is protected by a configurable timeout.

If the AI backend takes too long to respond:

The request is terminated.
The timeout is logged.
A fallback response is returned.

This prevents attacker sessions from becoming unresponsive due to slow backend processing.

Response Validation

Before processing the AI response, the module validates the returned data.

The validation includes:

Successful HTTP response.
Valid JSON structure.
Dictionary format verification.

Invalid or malformed responses are safely replaced by the fallback response.

This prevents runtime errors from affecting the honeypot.

Thread Safety

The honeypot supports multiple concurrent attacker sessions.

To ensure safe communication between threads, backend availability is managed using threading.Event.

Benefits include:

Thread-safe backend status updates.
Fast availability checks.
No additional synchronization required.
Safe access from multiple client threads.

This makes the AI client suitable for multi-client deployments.

Logging

The module records important backend events, including:

Health monitor startup.
Backend becoming online.
Backend becoming offline.
Connection failures.
Request timeouts.
Unexpected communication errors.

To avoid excessive logging, backend status is recorded only when a state transition occurs.

For example:

Offline → Online
Online → Offline

Repeated health checks that do not change the backend status do not generate additional log messages.

Workflow
Attacker Command
        │
        ▼
Prepare AI Request
        │
        ▼
Check Backend Availability
        │
   ┌────┴────┐
   │         │
Available   Unavailable
   │         │
   ▼         ▼
Send HTTP   Return
Request     Offline Fallback
   │
   ▼
Receive AI Response
   │
   ▼
Validate Response
   │
   ▼
Clean Response
   │
   ▼
Return to Honeypot
Function Description
clean_response(text)

Removes unnecessary Markdown formatting from AI-generated responses before returning them to the attacker.

get_offline_fallback(attack_type, elapsed_ms)

Generates a standardized fallback response whenever the AI backend is unavailable or a request fails.

check_ai_backend()

Performs a health check by sending a request to the backend's /health endpoint and returns the backend availability status.

_health_monitor_loop()

Runs continuously in a background daemon thread, periodically checking backend health and updating the backend availability status.

start_health_monitor()

Starts the background health monitoring thread.

The function is safe to call multiple times because it ensures that only one monitor thread is active.

send_to_ai(ip, command, history, attack_type)

The main communication function responsible for:

Preparing the AI request.
Sending it to the backend.
Handling retries and timeouts.
Validating the response.
Returning structured AI output or a fallback response.
Integration with Other Modules

The ai_client.py module works closely with several components of the honeypot:

server.py – Starts the health monitor during server initialization.
command_router.py – Calls send_to_ai() whenever AI processing is required.
session_manager.py – Supplies command history and session information.
attack_analyzer.py – Provides attack classification included in AI requests.
AI Backend – Processes attacker commands and returns AI-generated deception responses.

This modular architecture keeps communication, analysis, and deception responsibilities separate while allowing them to work together efficiently.

Advantages
Reliable communication with the AI backend.
Automatic backend health monitoring.
Seamless recovery from backend failures.
Offline fallback mechanism for uninterrupted operation.
Thread-safe implementation suitable for multiple concurrent clients.
Efficient HTTP communication using persistent sessions.
Configurable timeout and retry logic.
Response validation to prevent runtime errors.
Clean separation between the honeypot and AI backend.