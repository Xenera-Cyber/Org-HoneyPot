import random
import json

# Setup seed for deterministic generation
random.seed(42)

def generate_employee_data():
    first_names = ["Alice", "Bob", "Carlos", "Diana", "Evan", "Fiona", "George", "Helen", "Ian", "Julia", "Kevin", "Laura", "Marcus", "Nadia", "Oliver", "Paula", "Quinn", "Rachel", "Steve", "Tina"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White"]
    
    departments = ["Engineering", "HR", "Finance", "IT Security", "Operations", "Sales"]
    
    roles_map = {
        "Engineering": ["Senior Software Engineer", "Software Engineer", "Frontend Developer", "QA Engineer"],
        "HR": ["HR Manager", "HR Generalist", "Recruiter"],
        "Finance": ["CFO", "Financial Analyst", "Accountant"],
        "IT Security": ["CISO", "Lead Security Analyst", "Security Engineer"],
        "Operations": ["DevOps Engineer", "System Administrator", "Site Reliability Engineer"],
        "Sales": ["Sales Director", "Account Executive", "Sales Representative"]
    }
    
    projects_pool = ["Project Phoenix", "Project Aurora", "Project Pegasus", "Project Hydra", "Project Aegis"]
    
    employees = []
    
    # CEO Robert Vance as the anchor of organizational hierarchy
    ceo_name = "Robert Vance"
    employees.append({
        "EmployeeID": "EMP100",
        "Name": ceo_name,
        "Email": "robert.vance@xynera.local",
        "Department": "Executive",
        "Role": "CEO",
        "Phone": "+1-555-0100",
        "AssignedProjects": "Project Phoenix;Project Aegis",
        "ReportsTo": "Board of Directors",
        "AccessLevel": "Admin"
    })
    
    # Generate C-Level / Managers
    managers = {
        "Engineering": "Marcus Davis",
        "HR": "Diana Taylor",
        "Finance": "Julia Miller",
        "IT Security": "Steve Williams",
        "Operations": "Carlos Rodriguez",
        "Sales": "Helen Martinez"
    }
    
    for i in range(1, 25):
        emp_id = f"EMP{100 + i}"
        first = random.choice(first_names)
        last = random.choice(last_names)
        name = f"{first} {last}"
        
        # Avoid duplicate names by checking
        if any(e['Name'] == name for e in employees):
            name = f"{first} {random.choice(last_names)}"
            
        dept = random.choice(departments)
        
        # Override to ensure managers exist
        if (i - 1) < len(departments):
            dept = departments[i - 1]
            name = managers[dept]
            role = "CISO" if dept == "IT Security" else f"{dept} Director" if dept in ["Engineering", "Sales"] else f"{dept} Manager" if dept == "HR" else "CFO" if dept == "Finance" else "Operations Director"
            reports_to = ceo_name
        else:
            role = random.choice(roles_map[dept])
            reports_to = managers[dept]
            
        # Pin Fiona Garcia's details to align with security reports
        if i == 10:
            name = "Fiona Garcia"
            dept = "IT Security"
            role = "Security Engineer"
            reports_to = managers[dept]
            
        email = f"{name.lower().replace(' ', '.')}@xynera.local"
        phone = f"+1-555-01{70 + i:02d}"
        
        # Projects assigned
        assigned_projs = random.sample(projects_pool, random.randint(1, 2))
        proj_str = ";".join(assigned_projs)
        
        # Access levels
        access = "Admin" if role in ["CISO", "Operations Director", "CEO"] or "Lead" in role else "User" if dept in ["Engineering", "IT Security", "Operations"] else "Restricted"
        
        employees.append({
            "EmployeeID": emp_id,
            "Name": name,
            "Email": email,
            "Department": dept,
            "Role": role,
            "Phone": phone,
            "AssignedProjects": proj_str,
            "ReportsTo": reports_to,
            "AccessLevel": access
        })
        
    # Format to CSV
    csv_lines = ["EmployeeID,Name,Email,Department,Role,Phone,AssignedProjects,ReportsTo,AccessLevel"]
    for e in employees:
        csv_lines.append(f"{e['EmployeeID']},{e['Name']},{e['Email']},{e['Department']},{e['Role']},{e['Phone']},{e['AssignedProjects']},{e['ReportsTo']},{e['AccessLevel']}")
        
    return "\n".join(csv_lines), employees

def generate_department_data(employees):
    # Locate managers
    dept_managers = {}
    for e in employees:
        if "Director" in e["Role"] or "Manager" in e["Role"] or e["Role"] in ["CFO", "CISO"]:
            dept_managers[e["Department"]] = e["Name"]
            
    depts = [
        {"Code": "ENG", "Name": "Engineering", "Manager": dept_managers.get("Engineering", "Marcus Davis"), "Budget": "$1,250,000", "Location": "Floor 3, Wing A"},
        {"Code": "HR", "Name": "HR", "Manager": dept_managers.get("HR", "Diana Taylor"), "Budget": "$300,000", "Location": "Floor 2, Wing B"},
        {"Code": "FIN", "Name": "Finance", "Manager": dept_managers.get("Finance", "Julia Miller"), "Budget": "$650,000", "Location": "Floor 4, Wing A"},
        {"Code": "SEC", "Name": "IT Security", "Manager": dept_managers.get("IT Security", "Steve Williams"), "Budget": "$850,000", "Location": "Floor 3, Wing B (Secure Access)"},
        {"Code": "OPS", "Name": "Operations", "Manager": dept_managers.get("Operations", "Carlos Rodriguez"), "Budget": "$950,000", "Location": "Floor 2, Wing A"},
        {"Code": "SLS", "Name": "Sales", "Manager": dept_managers.get("Sales", "Helen Martinez"), "Budget": "$1,100,000", "Location": "Floor 1, Wing A"}
    ]
    return json.dumps(depts, indent=2)

def generate_project_data():
    projects = [
        {
            "ProjectCode": "PHOENIX",
            "Name": "Project Phoenix",
            "ProjectLead": "Marcus Davis",
            "Description": "Next-generation software deception orchestration and automated response simulator.",
            "Client": "Apex Corp",
            "Budget": "$450,000",
            "StartDate": "2025-01-15",
            "EndDate": "2026-03-31",
            "TeamSize": 8,
            "Status": "In Progress"
        },
        {
            "ProjectCode": "AURORA",
            "Name": "Project Aurora",
            "ProjectLead": "Carlos Rodriguez",
            "Description": "Legacy infrastructure cloud migration and horizontal scaling framework deployment.",
            "Client": "Nexus Industries",
            "Budget": "$620,000",
            "StartDate": "2025-06-01",
            "EndDate": "2026-12-31",
            "TeamSize": 12,
            "Status": "In Progress"
        },
        {
            "ProjectCode": "PEGASUS",
            "Name": "Project Pegasus",
            "ProjectLead": "Marcus Davis",
            "Description": "Internal corporate vault and zero-trust credential manager service.",
            "Client": "Internal",
            "Budget": "$150,000",
            "StartDate": "2025-09-01",
            "EndDate": "2026-06-30",
            "TeamSize": 4,
            "Status": "Planning"
        },
        {
            "ProjectCode": "HYDRA",
            "Name": "Project Hydra",
            "ProjectLead": "Steve Williams",
            "Description": "Distributed threat feed parser and real-time SIEM event decorator.",
            "Client": "Quantum Tech",
            "Budget": "$350,000",
            "StartDate": "2024-11-01",
            "EndDate": "2025-05-15",
            "TeamSize": 6,
            "Status": "Completed"
        },
        {
            "ProjectCode": "AEGIS",
            "Name": "Project Aegis",
            "ProjectLead": "Steve Williams",
            "Description": "Corporate perimeter hardening, WAF optimization, and active network defense orchestration.",
            "Client": "Summit Logistics",
            "Budget": "$280,000",
            "StartDate": "2025-03-01",
            "EndDate": "2026-08-31",
            "TeamSize": 7,
            "Status": "In Progress"
        }
    ]
    
    csv_lines = ["ProjectCode,Name,ProjectLead,Description,Client,Budget,StartDate,EndDate,TeamSize,Status"]
    for p in projects:
        csv_lines.append(f"{p['ProjectCode']},{p['Name']},{p['ProjectLead']},{p['Description']},{p['Client']},{p['Budget']},{p['StartDate']},{p['EndDate']},{p['TeamSize']},{p['Status']}")
    return "\n".join(csv_lines)

def generate_client_data():
    clients = [
        {"ClientID": "CLI001", "Name": "Apex Corp", "Industry": "Finance & Banking", "Contact": "Sarah Jenkins", "Projects": "Project Phoenix", "ContractValue": "$450,000", "Status": "Active"},
        {"ClientID": "CLI002", "Name": "Nexus Industries", "Industry": "Retail & Logistics", "Contact": "Tom Sterling", "Projects": "Project Aurora", "ContractValue": "$620,000", "Status": "Active"},
        {"ClientID": "CLI003", "Name": "Summit Logistics", "Industry": "Supply Chain", "Contact": "Regina Hall", "Projects": "Project Aegis", "ContractValue": "$280,000", "Status": "Active"},
        {"ClientID": "CLI004", "Name": "Horizon Health", "Industry": "Healthcare", "Contact": "Dr. Alan Grant", "Projects": "None", "ContractValue": "$150,000", "Status": "Pending"},
        {"ClientID": "CLI005", "Name": "Quantum Tech", "Industry": "Aerospace & Defense", "Contact": "Elena Rostova", "Projects": "Project Hydra", "ContractValue": "$850,000", "Status": "Active"}
    ]
    return json.dumps(clients, indent=2)

def generate_vendor_data():
    vendors = [
        {"VendorID": "VEN001", "Name": "CloudScale Solutions", "Service": "Infrastructure & Public Cloud Hosting", "AccountManager": "Dave Grohl", "Status": "Active"},
        {"VendorID": "VEN002", "Name": "NetGuard Security", "Service": "Annual External Penetration Testing", "AccountManager": "Trent Reznor", "Status": "Active"},
        {"VendorID": "VEN003", "Name": "CyberPulse Systems", "Service": "SOC-as-a-Service and Managed Detection", "AccountManager": "Amy Lee", "Status": "Active"},
        {"VendorID": "VEN004", "Name": "GlobalTek Supplies", "Service": "Hardware Procurement & Laptops", "AccountManager": "Jimmy Page", "Status": "Reviewing"}
    ]
    return json.dumps(vendors, indent=2)

def generate_infrastructure_yaml():
    yaml_str = """# Xynera Corporate Infrastructure Directory
infrastructure_assets:
  - hostname: prod-db-01.xynera.local
    ip_address: 10.200.100.15
    operating_system: Ubuntu 22.04 LTS
    environment: AWS us-east-1
    role: Production PostgreSQL Database
    open_ports: [22, 5432]
    security_status: Fully Patched

  - hostname: staging-api-01.xynera.local
    ip_address: 10.200.100.22
    operating_system: Debian 12 (Bookworm)
    environment: AWS us-east-1
    role: Staging API Gateway Router
    open_ports: [22, 80, 8080]
    security_status: Outdated OpenSSL (Upgrade Scheduled)

  - hostname: vpn-gw-01.xynera.local
    ip_address: 10.200.100.5
    operating_system: Ubuntu 22.04 LTS
    environment: On-premise Data Center
    role: Corporate OpenVPN Gateway
    open_ports: [22, 1194]
    security_status: Active Defense Enabled

  - hostname: backup-node-02.xynera.local
    ip_address: 10.200.100.40
    operating_system: CentOS Stream 9
    environment: On-premise Data Center
    role: Weekly Encrypted File Archiver
    open_ports: [22, 873]
    security_status: Offline Sync (Secure)

  - hostname: security-siem-01.xynera.local
    ip_address: 10.200.100.10
    operating_system: Ubuntu 22.04 LTS
    environment: AWS us-east-1
    role: IT Security Central Splunk Logger
    open_ports: [22, 443, 514, 9997]
    security_status: Restricted access (Admin Only)
"""
    return yaml_str

def get_markdown_documents():
    docs = {}
    
    # Wednesday Documents
    docs["report_q1_security.md"] = """# Xynera Internal Report: Q1 Security Posture Assessment
**Date:** April 5, 2026  
**Author:** Steve Williams, CISO  
**Classification:** Confidential - Internal Only

## Executive Summary
This report summarizes the findings of our Q1 2026 security review. While firewall configurations remain robust, several vulnerabilities were identified in the staging environment.

## Key Findings
1. **Weak SSH Credentials:** Attacker probes target staging server `staging-api-01` (`10.200.100.22`). Weak passwords are still in use for the `ubuntu` test account.
2. **Outdated Dependencies:** The API Gateway on staging is running a version of OpenSSL susceptible to CVE-2024-XXXX.
3. **Log Centralization:** Centralized logging to `security-siem-01` has been completed for all production boxes.

## Action Plan
- Enforce RSA key authentication on all staging servers.
- Perform a package update (`apt update && apt upgrade`) on `10.200.100.22` by next Tuesday.
"""

    docs["report_cloud_migration.md"] = """# Xynera Internal Report: Cloud Migration Roadmap
**Date:** May 14, 2026  
**Author:** Carlos Rodriguez, Operations Director  
**Classification:** Internal Use Only

## 1. Objectives
The objective is to migrate all remaining on-premise components (excluding the core VPN gateway) to AWS to increase elasticity and reliability.

## 2. Target Architecture
- **Web App Tier:** AWS ECS Fargate
- **Database:** RDS PostgreSQL
- **Backups:** S3 bucket replication with Glacier archiving

## 3. Timeline
* **Phase 1 (Planning):** May 15 - June 10
* **Phase 2 (Staging Migration):** June 11 - July 5
* **Phase 3 (Production Cutover):** July 20 (Scheduled downtime 02:00 - 04:00 EST)
"""

    docs["meeting_notes_2026_06_22.md"] = """# Meeting Notes: Weekly Security Sync
**Date:** June 22, 2026  
**Participants:** Steve Williams, Marcus Davis, Carlos Rodriguez, Fiona Garcia  

## Agenda
- Review of firewall alerts on OpenVPN Gateway (`10.200.100.5`)
- Staging server credential issues
- Progress on Project Aurora

## Discussed Items
- **Firewall Probes:** Fiona reported a slight surge in SSH password guessing against `vpn-gw-01`. Standard fail2ban rules blocked the IPs.
- **Staging Cleanup:** Steve emphasized replacing password logins with public keys.
- **Project Aurora:** Carlos stated the cloud migration of API testing endpoints is currently on track.

## Action Items
- **Fiona:** Implement temporary geo-blocking on the corporate VPN gateway.
- **Marcus:** Audit the Engineering employee active directory credentials.
"""

    docs["meeting_notes_2026_06_15.md"] = """# Meeting Notes: Project Aurora Kickoff
**Date:** June 15, 2026  
**Participants:** Engineering Team, Operations Team  

## Summary
Official kickoff meeting for the AWS cloud migration process.

## Discussion Points
- **Scope:** Migrating legacy microservices from on-premise infrastructure.
- **Team Roles:** 
  - Operations handles Terraform configurations.
  - Engineering modifies services to run in containerized environments.
- **Milestones:** Staging environments must be live in AWS us-east-1 by July 5.
"""

    docs["vpn_access_guidelines.md"] = """# Technical Documentation: Employee VPN Access Guidelines
**Version:** 1.4  
**Last Updated:** June 10, 2026  
**Author:** IT Security Team  

## Overview
All employees accessing corporate resources from remote networks are required to connect through the corporate OpenVPN gateway.

## Setup Instructions
1. Obtain your OpenVPN client profile (`.ovpn`) from IT Helpdesk.
2. Target VPN Gateway: `vpn-gw-01.xynera.local` (`10.200.100.5`).
3. Connect using standard port: `1194 UDP`.

## Policy Constraints
- Use multi-factor authentication (MFA) via Authenticator App.
- Do not bypass VPN controls or map public IPs directly to dev machines.
"""

    docs["api_gateway_setup.md"] = """# Technical Documentation: Staging API Gateway Setup
**Version:** 1.0  
**Last Updated:** May 20, 2026  
**Author:** DevOps Team  

## Host Profile
- **Server:** `staging-api-01.xynera.local` (`10.200.100.22`)
- **OS:** Debian Bookworm

## Installation
The gateway runs using a lightweight reverse proxy forwarding requests to downstream developer clusters.
- Config file: `/etc/gateway/router.conf`
- Port mappings: `80 -> 8080` (Internal API endpoints)

## Security
SSL certificates are auto-renewed via Let's Encrypt script on the 1st of every month.
"""

    docs["incident_2026_05_12_ddos.md"] = """# Incident Report: DDoS Attack on Public Web Server
**Incident ID:** INC-2026-004  
**Date of Incident:** May 12, 2026  
**Reporter:** Carlos Rodriguez  

## Description
At 14:15 UTC, monitoring tools flagged a spike in ingress traffic on the public-facing gateway, peaking at 20 Gbps. Web server response latency increased to >10 seconds, causing service outage.

## Analysis
The attack was identified as a UDP reflection/amplification flood targeting port 443. The traffic originated from several compromised NTP servers.

## Resolution
- Upstream ISP blackhole routing was applied to filter UDP flood.
- System returned to normal service at 15:42 UTC.
- Added stricter rate limiting at firewall level.
"""

    docs["incident_2026_06_01_phishing.md"] = """# Incident Report: Phishing Attempt on HR Team
**Incident ID:** INC-2026-005  
**Date of Incident:** June 1, 2026  
**Reporter:** Steve Williams  

## Details
An HR representative received a spoofed email claiming to be from "e-signature-portal.com" requesting password confirmation. The employee entered their AD login.

## Mitigation
- Account was locked automatically due to risk-based detection alerts.
- Credential rotated within 15 minutes of occurrence.
- Security training modules redistributed to the HR department.
- No indicators of compromise or lateral movement found.
"""

    # Internal Policies
    docs["remote_work_policy.md"] = """# Xynera Corporate Policy: Remote Work Security Policy
**Document ID:** POL-2026-012  
**Effective Date:** January 1, 2026  
**Author:** Steve Williams, CISO  
**Classification:** Confidential - Internal Use Only

## 1. Purpose & Scope
This policy defines the security requirements for Xynera employees accessing corporate resources from remote locations. It applies to all full-time, part-time, and contract employees.

## 2. Remote Access Requirements
- All remote connections to internal servers and databases MUST route through the corporate OpenVPN gateway (`vpn-gw-01.xynera.local` / `10.200.100.5`) on port 1194 UDP.
- Multi-Factor Authentication (MFA) must be enabled and enforced for all remote access sessions.
- Users must only connect from corporate-managed and hardened endpoints running up-to-date antivirus software.

## 3. Local Endpoint Hardening
- Automatic OS security updates must be enabled.
- Hard drive encryption (FileVault/BitLocker) must be active.
- Local firewalls must be turned on, blocking all unauthorized inbound traffic.
- Never share corporate credentials or leave devices unattended.
"""

    docs["incident_response_policy.md"] = """# Xynera Corporate Policy: Incident Response Policy
**Document ID:** POL-2026-015  
**Effective Date:** March 15, 2026  
**Author:** Steve Williams, CISO  
**Classification:** Confidential - Internal Use Only

## 1. Classification of Incidents
Incidents are categorized by severity to determine escalation and resources:
- **Sev-1 (Critical):** Active breach of production databases, critical ransomware, or loss of access to primary systems. Immediate CISO notification.
- **Sev-2 (High):** Localized malware infection on dev/staging server, compromised developer credentials, or unauthorized access to staging environment. Escalation within 2 hours.
- **Sev-3 (Medium):** Standard phishing attempts, blocked firewall sweeps, or minor service outages. Investigation within 24 hours.
- **Sev-4 (Low):** Minor anomalies, port scanning, or unsuccessful brute-force attempts. Weekly log review.

## 2. Escalation Contacts
- **IT Security Lead:** Steve Williams (CISO) - steve.williams@xynera.local
- **Infrastructure Lead:** Carlos Rodriguez (Operations) - carlos.rodriguez@xynera.local
- **Engineering Lead:** Marcus Davis - marcus.davis@xynera.local
"""

    docs["password_policy.md"] = """# Xynera Corporate Policy: Password and Credential Policy
**Document ID:** POL-2026-003  
**Effective Date:** February 10, 2026  
**Author:** Steve Williams, CISO  
**Classification:** Confidential - Internal Use Only

## 1. Password Complexity Requirements
All local, Active Directory, and service passwords must satisfy the following minimum requirements:
- Minimum length: 14 characters.
- Must contain at least one uppercase letter, one lowercase letter, one number, and one special character.
- Must not contain dictionary words or the employee's name.

## 2. Rotation & Lockouts
- Passwords must be rotated every 90 days.
- Re-use of the last 10 passwords is prohibited.
- Accounts will be automatically locked after 5 consecutive failed login attempts. Lockout duration is set to 30 minutes.
- Service account passwords must be managed using the Project Pegasus corporate vault.
"""

    # Technical Manuals
    docs["database_recovery_manual.md"] = """# Technical Manual: PostgreSQL Backup & Recovery Guide
**Document ID:** MAN-2026-044  
**Version:** 2.1  
**Last Updated:** June 18, 2026  
**Author:** Carlos Rodriguez, Operations Director  

## 1. Overview
This manual details the step-by-step procedure to restore the production PostgreSQL database (`db-prod-01.xynera.local`) from daily logical backups.

## 2. Backup Location
- Local backups: `/var/www/internal/db_backup.sql`
- S3 Bucket: `s3://xynera-secure-vault-backup-2026/` (Glacier archiving active)

## 3. Restore Procedures
To restore the database on a clean server:
1. Set environment variables using `/home/ubuntu/.env`.
2. Terminate active sessions:
   ```sql
   SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'customers';
   ```
3. Drop and recreate database:
   ```bash
   dropdb -h localhost -U db_user customers
   createdb -h localhost -U db_user customers
   ```
4. Restore SQL dump:
   ```bash
   psql -h localhost -U db_user -d customers -f /var/www/internal/db_backup.sql
   ```
5. Verify count of tables and run sanity test queries.
"""

    docs["kubernetes_deployment_guide.md"] = """# Technical Manual: Production Kubernetes Deployment Guide
**Document ID:** MAN-2026-039  
**Version:** 1.2  
**Last Updated:** May 22, 2026  
**Author:** Carlos Rodriguez, Operations Director  

## 1. Architecture Overview
Xynera uses a Managed Kubernetes (EKS) cluster in AWS to orchestrate core API microservices. The production namespaces are divided into `prod` and `staging`.

## 2. Deployment Instructions
Deployments are managed using YAML manifests:
1. Verify resource parameters in `k8s_deployment.yaml`.
2. Apply changes:
   ```bash
   kubectl apply -f /home/ubuntu/documents/technical_docs/k8s_deployment.yaml --namespace=prod
   ```
3. Monitor rolling update status:
   ```bash
   kubectl rollout status deployment/xynera-api-deployment --namespace=prod
   ```

## 3. Secret Injection Configuration
Credentials must not be committed to Git. The EKS pod fetches the database URI and key variables dynamically from AWS Secrets Manager using IAM roles mapped to service accounts.
"""

    # Incident Reports
    docs["incident_2026_06_18_malware.md"] = """# Incident Report: Staging Server Malware Detection
**Incident ID:** INC-2026-008  
**Date of Incident:** June 18, 2026  
**Reporter:** Fiona Garcia, Security Engineer  

## Description
At 22:10 UTC, the file integrity monitoring agent on `staging-api-01` (`10.200.100.22`) triggered a Sev-2 alert. An unauthorized script was identified under `/tmp/miner.sh` executing in the background.

## Analysis
Investigation showed the script was downloaded via `wget` from a known malicious IP (`192.168.1.100`). The attacker gained access by brute-forcing the weak SSH password of the `ubuntu` test account, which had not been hardened. A crontab entry was added to re-download the miner every 5 minutes.

## Mitigation
- Terminated the execution processes of `/tmp/miner.sh` and deleted the file.
- Cleaned the user crontab and deleted the backdoor crontab entry.
- Hardened SSH configuration on `staging-api-01` by disabling password-based authentication.
- Rotated all local user passwords.
"""

    docs["incident_2026_06_24_leak.md"] = """# Incident Report: Accidental Credential Leak on Public Repository
**Incident ID:** INC-2026-009  
**Date of Incident:** June 24, 2026  
**Reporter:** Steve Williams, CISO  

## Description
At 10:15 UTC, GitGuardian automated tools alerted that a developer had pushed code to a public GitHub repository containing a production Slack Webhook URL and a mock Stripe Secret API Key.

## Analysis
The developer was testing integrations for Project Phoenix and accidentally included active credentials in the config.json file within the commit history. The commit was public for approximately 42 minutes before detection.

## Mitigation
- Revoked and rotated the Stripe secret API keys immediately.
- Deleted the exposed Slack Webhook URL and provisioned a new one.
- Performed a repository clean using BFG Repo-Cleaner to completely remove history secrets.
- Re-trained developers on using `.env` files and environment variables.
"""

    # HR Documents
    docs["employee_onboarding_guide.md"] = """# HR Onboarding: New Employee IT & Security Onboarding Guide
**Document ID:** HR-2026-001  
**Version:** 3.0  
**Author:** Diana Taylor, HR Manager  

## Welcome to Xynera!
This onboarding guide outlines the mandatory setup tasks to ensure compliance with our security and engineering guidelines.

## First-Week Action Items
1. **Security Policy Review:** Read and sign the Remote Work Policy (POL-2026-012) and Password Policy (POL-2026-003).
2. **IT Provisioning:** Your laptop has been pre-configured by IT Security with standard antivirus and OS hardening profiles.
3. **VPN Profile Setup:** Submit a ticket to support@xynera.local to obtain your `.ovpn` configuration file for the OpenVPN gateway (`10.200.100.5`).
4. **MFA Enrolment:** Scan the QR code provided by the administrator to set up Google Authenticator or Duo on your mobile device.
5. **Git Setup:** Clone your assigned repositories under `https://github.com/xynera-corp/` and configure your GPG signing keys.
"""

    docs["performance_review_template.md"] = """# HR Template: Biannual Employee Performance Review Template
**Document ID:** HR-2026-004  
**Author:** Diana Taylor, HR Manager  

## Employee Review Structure
This template is used by managers to conduct performance evaluations every 6 months.

### Section A: General Information
- Employee Name:
- Job Title:
- Department:
- Date of Evaluation:

### Section B: Core Performance Metrics (Scale 1-5)
1. **Technical Delivery & Execution:** Quality of code, design choices, and adherence to milestones.
2. **Collaboration & Leadership:** Team communication, peer reviews, and mentorship.
3. **Security Hygiene & Compliance:** Adherence to SSH practices, key management, and zero credential leak occurrences.

### Section C: Goal Realization
- Summary of Q1/Q2 achievements.
- Future development targets and objectives.
"""

    # Vendor Contracts
    docs["cloudscale_solutions_sla.md"] = """# Vendor Contract: CloudScale Solutions Service Level Agreement (SLA)
**Contract ID:** CON-2026-099  
**Effective Date:** April 1, 2026  
**Vendor:** CloudScale Solutions Inc.  
**Client:** Xynera Ltd.  

## 1. Scope of Services
CloudScale Solutions provides cloud virtual machine instances, PostgreSQL database hosting, and high-performance load balancers in the AWS us-east-1 region.

## 2. Service Level Commitments
- **Uptime SLA:** Vendor commits to a 99.9% monthly uptime SLA for all database nodes.
- **Service Credits:** If uptime falls below 99.9%, a 10% refund of monthly billing applies. If below 99.0%, a 25% refund applies.

## 3. Incident Support Response Times
- **Severity-1 (Critical):** Immediate response within 30 minutes (24/7 support line active).
- **Severity-2 (High):** Response within 2 hours.
- **Severity-3 (Normal):** Response within 24 hours.
"""

    docs["netguard_security_agreement.md"] = """# Vendor Contract: NetGuard Security Penetration Testing Agreement
**Contract ID:** CON-2026-104  
**Effective Date:** May 10, 2026  
**Vendor:** NetGuard Security Consultants LLC  
**Client:** Xynera Ltd.  

## 1. Scope of Testing
NetGuard Security is contracted to perform annual external and internal penetration testing against the following target IP scopes:
- Public Web Gateway: `10.200.100.10`
- OpenVPN Endpoint: `10.200.100.5`
- Staging API Gateway: `10.200.100.22`

## 2. Limitation of Liability
Testing is executed using standard cyber exploit simulations. The vendor is not liable for incidental system downtime or temporary packet loss if scan sweeps execute during business hours.

## 3. Payment Milestones
- 30% upfront payment upon execution of the agreement.
- 40% upon completion of scanning and report generation.
- 30% upon presentation of re-test results for patched items.
"""

    # Network Documentation
    docs["network_topology_guide.md"] = """# Network Documentation: Xynera Corporate Network Topology Guide
**Document ID:** NET-2026-001  
**Version:** 1.5  
**Last Updated:** June 15, 2026  
**Author:** IT Security Team  

## 1. VPC Network Layout
Xynera operates within a single virtual private cloud (VPC) split into three security zones:
- **Public Subnet (DMZ):** Houses public gateways, ELB load balancers, and external routing interfaces.
- **Private App Subnet:** Houses API gateway microservices (`staging-api-01` / `10.200.100.22`) and core logic.
- **Secure Database Subnet:** Houses backend databases (`prod-db-01` / `10.200.100.15`) with access limited to staging-api subnets.

## 2. Firewall and Access Controls
- All outbound traffic is routed through NAT gateways.
- SSH access requires connection to the OpenVPN gateway (`10.200.100.5`) first. Direct SSH from the public internet is blocked.
"""

    docs["subnets_routing_map.md"] = """# Network Documentation: CIDR Subnets and Routing Map
**Document ID:** NET-2026-002  
**Last Updated:** June 18, 2026  
**Author:** IT Security Team  

## CIDR Subnet Mappings
| Subnet Name | CIDR Range | Gateway IP | Primary Description | Status |
| :--- | :--- | :--- | :--- | :--- |
| Public-DMZ | `10.200.100.0/28` | `10.200.100.1` | Public API & load balancer ingress | Active |
| Secure-VPN | `10.200.100.4/30` | `10.200.100.5` | Corporate OpenVPN Gateway interface | Active |
| SIEM-Log | `10.200.100.8/29` | `10.200.100.9` | Splunk and SIEM log aggregation endpoints | Active |
| Database-Prod | `10.200.100.12/29` | `10.200.100.13` | Production PostgreSQL data cluster | Active |
| Gateway-Staging | `10.200.100.20/29` | `10.200.100.21` | Staging testing endpoints & API GATEWAY | Active |
| Backup-Vault | `10.200.100.32/28` | `10.200.100.33` | Encrypted Backup and Glacier sync nodes | Active |
"""

    return docs

def generate_ssh_private_key():
    return """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtcn
NhAAAAAwEAAQAAAYEA0Gf3Y3g5aDg5Y2g4OWFnZHNhZ2RzYWc1NnNmZ2RzZ2RzZ2RzZ2c1
c2RmZ3NkZ3NkZ3NkZ3NkZ2RmZ2RzZ2RzZ2RzZ2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2
dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dk
c2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2
dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dk
c2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2
dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dk
-----END OPENSSH PRIVATE KEY-----
"""

def generate_shadow_file():
    # Passwords:
    # root: [SUPER SECURE - UNCRACKABLE]
    # ubuntu: [SSH-ONLY / DISABLED PASSWORD]
    # dev: devPassword2026!
    # admin: adminSecurePassword2026#
    # support: supportHelpdesk2026$
    # backupuser: backupOperator2026
    return """root:$6$rounds=40000$saltsaltsalt$M1U5B2r7s7d1i9s1j2k3l4m5n6o7p8q9r0s1t2u3v4w5x6y7z8a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2:19000:0:99999:7:::
ubuntu:$6$rounds=40000$anothersalt$v4w5x6y7z8a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k7l8m9n0o1p2q3r4s5t6u7v8w9x0y1z2a3b4c5d6e7f8:19000:0:99999:7:::
dev:$6$rounds=40000$yetanothersalt$f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k7l8m9n0o1p2q3r4s5t6u7v8w9x0y1z2a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7:19000:0:99999:7:::
admin:$6$rounds=40000$adminsalt$M6t8Y9d0e1f2g3h4i5j6k7l8m9n0o1p2q3r4s5t6u7v8w9x0y1z2a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r0s1t2u3v4w5x6y7z8a1b2c3d4e5f6g7h8:19000:0:99999:7:::
support:$6$rounds=40000$supportsalt$p8q9r0s1t2u3v4w5x6y7z8a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k7l8m9n0o1p2q3r4s5t6u7v8w9:19000:0:99999:7:::
backupuser:$6$rounds=40000$backupsalt$y2z3A4B5C6D7E8F9G0H1I2J3K4L5M6N7O8P9Q0R1S2T3U4V5W6X7Y8Z9a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1:19000:0:99999:7:::
"""

def generate_aws_credentials():
    return """[default]
aws_access_key_id = AKIA2T3U4V5W6X7Y8Z9A
aws_secret_access_key = pT2d+G8fL9K1j4h3M7N6q9z2R5t8v1w4x7Y0z3A1
region = us-east-1
"""

def generate_slack_config():
    config = {
        "slack_webhook_url": "https://hooks.slack.com/services/T_MOCK_DEV/B_MOCK_DEV/s8D9f0G1h2J3k4L5m6N7o8P9_MOCK",
        "channel": "#alerts-security",
        "username": "Xynera-Deception-Bot"
    }
    return json.dumps(config, indent=2)

def generate_stripe_config():
    config = {
        "stripe_publishable_key": "pk_tst_51NvA01B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6a7b8c9d0e1f2g3h4i5j6k7l8m9n0o1p2q3r",
        "stripe_secret_key": "sk_tst_51NvA01B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6a7b8c9d0e1f2g3h4i5j6k7l8m9n0o1p2q3r",
        "api_version": "2023-10-16"
    }
    return json.dumps(config, indent=2)



def generate_db_backup_sql(employees=None):
    if not employees:
        employees = [
            {"EmployeeID": "EMP100", "Name": "Robert Vance", "Email": "robert.vance@xynera.local", "Role": "CEO"},
            {"EmployeeID": "EMP101", "Name": "Marcus Davis", "Email": "marcus.davis@xynera.local", "Role": "Engineering Director"},
            {"EmployeeID": "EMP102", "Name": "Fiona Garcia", "Email": "fiona.garcia@xynera.local", "Role": "Security Engineer"}
        ]
    
    insert_rows = []
    insert_rows.append("(1, 'admin', '$2b$12$eImiTXAk4VMV619eFv02eO/J5jVv2uHj2.Hn2s994m8.O/eX/f6H.', 'admin@xynera.local', 'administrator')")
    
    id_counter = 2
    for emp in employees:
        username = emp["Email"].split("@")[0]
        email = emp["Email"]
        role = emp["Role"].lower().replace(" ", "_")
        pwd_hash = f"$2b$12$K3h9j2H8s2h1i9s1j2k3l4m5n6o7p8q9r{id_counter:02d}s1t2u3v4w5x6y7z8"
        insert_rows.append(f"({id_counter}, '{username}', '{pwd_hash}', '{email}', '{role}')")
        id_counter += 1
        
    users_insert_statement = "INSERT INTO public.users (id, username, password_hash, email, role) VALUES\n" + ",\n".join(insert_rows) + ";"

    return f"""-- PostgreSQL Database Dump
-- Dumped by pg_dump version 14.5 (Ubuntu 14.5-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF-8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL,
    email character varying(100) NOT NULL,
    role character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE public.users OWNER TO db_user;

{users_insert_statement}

CREATE TABLE public.transactions (
    transaction_id character varying(36) NOT NULL,
    user_id integer NOT NULL,
    amount numeric(10,2) NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE public.transactions OWNER TO db_user;

INSERT INTO public.transactions (transaction_id, user_id, amount, status) VALUES
('tx_9876543210', 2, 1250.00, 'completed'),
('tx_1234567890', 1, 45000.00, 'pending');

ALTER TABLE ONLY public.users ADD CONSTRAINT users_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_username_key UNIQUE (username);
ALTER TABLE ONLY public.transactions ADD CONSTRAINT transactions_pkey PRIMARY KEY (transaction_id);
ALTER TABLE ONLY public.transactions ADD CONSTRAINT transactions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
"""

def generate_audit_log_csv():
    return """Timestamp,User,IPAddress,Action,Status
2026-06-25 10:15:22,ubuntu,192.168.1.10,SSH Login,Success
2026-06-25 10:18:45,ubuntu,192.168.1.10,Sudo Command: apt-get update,Success
2026-06-25 10:22:11,dev,192.168.1.12,Database Access,Success
2026-06-25 10:24:55,dev,192.168.1.12,Database Backup Initiated,Success
2026-06-25 10:30:00,root,127.0.0.1,Log Rotation Service,Success
"""

def generate_nginx_conf():
    return """server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name xynera.local;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
"""

def generate_kubernetes_yaml():
    return """apiVersion: apps/v1
kind: Deployment
metadata:
  name: xynera-api-deployment
  namespace: prod
  labels:
    app: xynera-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: xynera-api
  template:
    metadata:
      labels:
        app: xynera-api
    spec:
      containers:
      - name: xynera-api
        image: xynera/api-server:v1.2.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          value: "postgresql://db_user:securePassword123@prod-db-01.xynera.local:5432/xynera_prod"
        - name: STRIPE_API_KEY
          valueFrom:
            secretKeyRef:
              name: stripe-secret
              key: api-key
"""

def generate_env_file():
    return """# Environment variables for Xynera application
DEBUG=false
ENVIRONMENT=production
PORT=8080

# Database credentials
DATABASE_URL=postgresql://db_user:securePassword123@prod-db-01.xynera.local:5432/xynera_prod

# Third-party APIs
STRIPE_API_KEY=sk_tst_51NvA01B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6a7b8c9d0e1f2g3h4i5j6k7l8m9n0o1p2q3r
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T_MOCK_DEV/B_MOCK_DEV/s8D9f0G1h2J3k4L5m6N7o8P9_MOCK
GITHUB_TOKEN=ghp_DECEPTION_MOCK_TOKEN_XYNERA_DECOY
OPENAI_API_KEY=sk-proj-DECEPTION_MOCK_OPENAI_KEY_XYNERA_DECOY
"""

def generate_aws_config():
    return """[default]
region = us-east-1
output = json
"""

def generate_kube_config():
    return """apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://k8s-cluster.xynera.local:6443
  name: xynera-prod-cluster
contexts:
- context:
    cluster: xynera-prod-cluster
    namespace: prod
    user: kubernetes-admin
  name: xynera-prod-context
current-context: xynera-prod-context
kind: Config
preferences: {}
users:
- name: kubernetes-admin
  user:
    token: eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJib290c3RyYXAtdG9rZW4tOTk5OTkiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2VhY2NvdW50Lm5hbWUiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlYWNjb3VudC51aWQiOiI5OTk5OTk5OS05OTk5LTk5OTktOTk5OS05OTk5OTk5OTk5OTkiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06ZGVmYXVsdCJ9.signature
"""

def generate_netplan_config():
    return """network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 10.200.100.10/28
      nameservers:
        addresses:
          - 10.200.100.1
          - 1.1.1.1
      routes:
        - to: default
          via: 10.200.100.1
"""

def generate_hosts_file():
    return """127.0.0.1 localhost
127.0.1.1 web-prod-01
10.200.100.15 prod-db-01.xynera.local prod-db-01
10.200.100.22 staging-api-01.xynera.local staging-api-01
10.200.100.5 vpn-gw-01.xynera.local vpn-gw-01
10.200.100.40 backup-node-02.xynera.local backup-node-02
10.200.100.10 security-siem-01.xynera.local security-siem-01
"""

def generate_pgpass_file():
    return """prod-db-01.xynera.local:5432:xynera_prod:db_user:securePassword123
staging-db-01.xynera.local:5432:xynera_staging:staging_developer:TemporaryStagingPassword2026!
"""

def generate_dev_tasks_md():
    return """# Cloud Migration dev tasks
1. Staging API Gateway deployment:
   Access the staging API gateway router at `staging-api-01.xynera.local` (`10.200.100.22`) via SSH.
   Use the local private key stored in `/home/ubuntu/.ssh/id_rsa` (user: `ubuntu`).
2. API secrets mapping:
   Ensure the production environment variables inside `/home/ubuntu/.env` are synchronized to the API gateway.
3. Database replication backup:
   PostgreSQL schemas are dumped to `/var/www/internal/db_backup.sql`.
   Ensure they are uploaded to the secure S3 bucket using the credentials in `/home/ubuntu/.aws/credentials`.
"""

def generate_gateway_router_conf():
    return """# API Gateway Router configurations
# Upstream configuration for public endpoints
server {
    listen 8080;
    server_name staging-api-01.xynera.local;

    # Downstream services mapping
    location /api/v1/users {
        # Users data served from production database
        proxy_pass http://prod-db-01.xynera.local:5432;
    }

    location /api/v1/backups {
        # Backups log and status service
        # To access backup archives on backup-node-02 (10.200.100.40), use the private SSH sync key:
        # Key file path: /home/ubuntu/.ssh/backup_key (user: dev)
        proxy_pass http://backup-node-02.xynera.local:873;
    }
}
"""

def generate_backup_key():
    return """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtcn
NhAAAAAwEAAQAAAYEA0Gf3Y3g5aDg5Y2g4OWFnZHNhZ2RzYWc1NnNmZ2RzZ2RzZ2RzZ2c1
c2RmZ3NkZ3NkZ3NkZ3NkZ2RmZ2RzZ2RzZ2RzZ2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2
dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dk
YmFja3VwX2tleV9mb3JfYmFja3VwX25vZGVfMDJfZGVjMHlfZGVjb3lfZGVjb3lfZGVjb3
c2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2
dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dkc2dk
-----END OPENSSH PRIVATE KEY-----
"""

def generate_backup_status_txt():
    return """System Backups Status: SUCCESS
All systems back up verified at 2026-06-25 04:00:00 UTC.

Archives Location:
- S3 Bucket: `s3://xynera-secure-vault-backup-2026/weekly-prod-db-backup.tar.gz`
- Storage Tier: Amazon Glacier Deep Archive
- Vault Region: us-east-1

Encryption Key for DB Archive:
- Cipher: AES-256-GCM
- Passphrase: `xynera-super-secure-encryption-key-2026`

Note: In case of failover or sync issues, contact the system administrator (admin@xynera.local).
"""

def generate_passwd_file():
    return """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug Reporting:/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:Systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:101:103:Systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:102:106:D-Bus Message Bus:/nonexistent:/usr/sbin/nologin
syslog:x:103:110:Syslog:/home/syslog:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
uuidd:x:105:111:UUID Daemon:/run/uuidd:/usr/sbin/nologin
tcpdump:x:106:112::/nonexistent:/usr/sbin/nologin
tss:x:107:113:TPM Software Stack:/var/lib/tpm:/bin/false
landscape:x:108:114:Landscape Client:/var/lib/landscape:/usr/sbin/nologin
pollinate:x:109:1:Pollinate:/var/cache/pollinate:/bin/false
mysql:x:110:115:MySQL Server:/nonexistent:/bin/false
postgres:x:111:116:PostgreSQL Administrator:/var/lib/postgresql:/bin/bash
redis:x:112:117:Redis Server:/var/lib/redis:/usr/sbin/nologin
docker:x:113:118:Docker Engine:/var/lib/docker:/usr/sbin/nologin
nginx:x:114:119:Nginx Service:/var/cache/nginx:/usr/sbin/nologin
ubuntu:x:1000:1000:Ubuntu User:/home/ubuntu:/bin/bash
dev:x:1001:1001:Developer:/home/dev:/bin/bash
admin:x:1002:1002:System Administrator:/home/admin:/bin/bash
support:x:1003:1003:Support Engineer:/home/support:/bin/bash
backupuser:x:1004:1004:Backup Operator:/home/backupuser:/bin/bash
"""

def generate_sshd_config():
    return """# SSH Server Configuration File for Xynera Production Servers
Port 22
Protocol 2
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

# Logging Configuration
SyslogFacility AUTH
LogLevel INFO

# Authentication Settings
LoginGraceTime 120
PermitRootLogin no
StrictModes yes
MaxAuthTries 3
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys

# Password Authentication Configuration
PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
UsePAM yes

# Access Control
AllowUsers ubuntu dev admin support
X11Forwarding no
PrintMotd no
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
ClientAliveInterval 300
ClientAliveCountMax 2
"""

def generate_redis_conf():
    return """# Redis configuration file for Xynera Local Cache Service
bind 127.0.0.1 10.200.100.15
protected-mode yes
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize yes
supervised systemd
pidfile /var/run/redis_6379.pid
loglevel notice
logfile /var/log/redis/redis-server.log
databases 16
always-show-logo no

# Snapshotting / Persistence
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /var/lib/redis

# Security
requirepass superSecureRedisPassword2026

# Clients Limit
maxclients 10000
maxmemory 536870912
maxmemory-policy allkeys-lru
"""

def generate_postgresql_conf():
    return """# PostgreSQL Configuration File for db-prod-01.xynera.local
listen_addresses = '10.200.100.15,127.0.0.1'
port = 5432
max_connections = 100
shared_buffers = 512MB
effective_cache_size = 1536MB
maintenance_work_mem = 128MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 5242kB
min_wal_size = 1GB
max_wal_size = 4GB

# Logging Configuration
log_destination = 'stderr'
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_min_messages = warning
log_min_error_statement = error
log_min_duration_statement = 250

# Replication Configuration
wal_level = replica
max_wal_senders = 10
hot_standby = on
"""

def generate_emails():
    emails = {}
    emails["inbox_summary.txt"] = """Xynera Corporate Mail Server - Inbox for user ubuntu
Total Unread: 4 | Last Synchronized: 2026-07-01 10:15:00 UTC

[1] Received: 2026-06-23 09:15:00 UTC | From: steve.williams@xynera.local | Subject: Urgent: Phishing Attempt Targeting HR Department
[2] Received: 2026-06-18 11:22:00 UTC | From: carlos.rodriguez@xynera.local | Subject: Staging Database Access Info
[3] Received: 2026-06-12 14:05:00 UTC | From: diana.taylor@xynera.local | Subject: Action Required: Q2 Performance Review Cycle
[4] Received: 2026-06-05 16:30:00 UTC | From: julia.miller@xynera.local | Subject: CloudScale Solutions Contract & SLA Renewal
"""

    emails["security_phishing_alert.txt"] = """From: Steve Williams <steve.williams@xynera.local>
To: employees@xynera.local
Date: 2026-06-23 09:15:00 UTC
Subject: Urgent: Phishing Attempt Targeting HR Department

Dear Team,

It has come to the attention of the IT Security Team that several employees within our Human Resources department have received sophisticated phishing emails over the past 24 hours. These emails claim to be from "e-signature-portal.com" and prompt users to verify their Active Directory credentials to sign an urgent employee policy document.

If you received this message, DO NOT click any links and DO NOT enter your credentials. Our automated identity defenses successfully flagged and locked one compromised account, and we are auditing active directory logs for lateral movement.

As a reminder, all remote authentication must go through our corporate OpenVPN gateway (vpn-gw-01.xynera.local / 10.200.100.5) and is subject to Multi-Factor Authentication (MFA) enforcement. Please review our Remote Work Security Policy and Password Policy under /home/ubuntu/documents/policies/ for standard procedures.

Report any suspicious emails immediately to security@xynera.local.

Best regards,
Steve Williams
Chief Information Security Officer (CISO)
Xynera Ltd.
"""

    emails["staging_db_access.txt"] = """From: Carlos Rodriguez <carlos.rodriguez@xynera.local>
To: dev-team@xynera.local
Date: 2026-06-18 11:22:00 UTC
Subject: Staging Database Access Info

Hey team,

To facilitate the ongoing cloud migration under Project Aurora, we have deployed a replica staging database.

You can connect to the database host at staging-db-01.xynera.local (IP: 10.200.100.22, Port: 5432).
Credentials:
- Database: xynera_staging
- Username: staging_developer
- Password: TemporaryStagingPassword2026! (Remember to rotate this!)

The database schemas match the production snapshot. Please run your validation queries against this host. For details on server tasks, credentials sync, and backups verification, refer to /var/www/internal/dev_tasks.md.

Reach out to me if you face any connection timeouts or firewall blocking issues.

Thanks,
Carlos Rodriguez
Operations Director
Xynera Ltd.
"""

    emails["performance_review_cycle.txt"] = """From: Diana Taylor <diana.taylor@xynera.local>
To: managers@xynera.local
Date: 2026-06-12 14:05:00 UTC
Subject: Action Required: Q2 Performance Review Cycle

Hi Managers,

Our Q2 Performance Review Cycle is officially open today. 

Please ensure that you schedule 1-on-1 reviews with all direct reports in your respective departments before July 15. The evaluations should be filled out using the standard corporate evaluation template. You can find the template on the local file server at /home/ubuntu/documents/hr/performance_review_template.md.

For new employees onboarding this month, please refer to the /home/ubuntu/documents/hr/employee_onboarding_guide.md to complete their IT provisioning and policy sign-offs.

All completed evaluations must be sent to hr@xynera.local.

Thanks,
Diana Taylor
HR Manager
Xynera Ltd.
"""

    emails["vendor_contract_renewal.txt"] = """From: Julia Miller <julia.miller@xynera.local>
To: steve.williams@xynera.local, carlos.rodriguez@xynera.local
Date: 2026-06-05 16:30:00 UTC
Subject: CloudScale Solutions Contract & SLA Renewal

Hi Steve, Carlos,

We are in the process of finalizing our infrastructure hosting contract renewal with CloudScale Solutions. 

Before I sign the new agreement, I need you both to review the updated Service Level Agreement (SLA). The draft document has been uploaded to /home/ubuntu/documents/contracts/cloudscale_solutions_sla.md. 

Specifically, please verify:
1. If the 99.9% uptime commitment is sufficient for our production PostgreSQL databases.
2. If the support response times (Sev-1 incident response within 30 minutes) align with our Incident Response Policy.

Please send me your feedback by next Tuesday so we can execute the contract.

Regards,
Julia Miller
CFO
Xynera Ltd.
"""
    return emails

def get_generated_all():
    csv_emp, list_emp = generate_employee_data()
    dept_json = generate_department_data(list_emp)
    proj_csv = generate_project_data()
    cli_json = generate_client_data()
    vend_json = generate_vendor_data()
    infra_yaml = generate_infrastructure_yaml()
    docs = get_markdown_documents()
    
    ssh_key = generate_ssh_private_key()
    shadow = generate_shadow_file()
    passwd = generate_passwd_file()
    aws_creds = generate_aws_credentials()
    aws_config = generate_aws_config()
    kube_config = generate_kube_config()
    netplan_config = generate_netplan_config()
    hosts_file = generate_hosts_file()
    pgpass_file = generate_pgpass_file()
    
    slack_conf = generate_slack_config()
    stripe_conf = generate_stripe_config()
    db_backup = generate_db_backup_sql(list_emp)
    audit_log = generate_audit_log_csv()
    nginx = generate_nginx_conf()
    k8s = generate_kubernetes_yaml()
    env = generate_env_file()
    
    dev_tasks = generate_dev_tasks_md()
    gateway_conf = generate_gateway_router_conf()
    bkey = generate_backup_key()
    bstatus = generate_backup_status_txt()

    sshd_config = generate_sshd_config()
    redis_conf = generate_redis_conf()
    postgresql_conf = generate_postgresql_conf()
    emails = generate_emails()
    
    return {
        "employees_csv": csv_emp,
        "departments_json": dept_json,
        "projects_csv": proj_csv,
        "clients_json": cli_json,
        "vendors_json": vend_json,
        "infrastructure_yaml": infra_yaml,
        "documents": docs,
        "ssh_private_key": ssh_key,
        "shadow_file": shadow,
        "passwd_file": passwd,
        "aws_credentials": aws_creds,
        "aws_config": aws_config,
        "kube_config": kube_config,
        "netplan_config": netplan_config,
        "hosts_file": hosts_file,
        "pgpass_file": pgpass_file,
        "slack_config_json": slack_conf,
        "stripe_config_json": stripe_conf,
        "db_backup_sql": db_backup,
        "audit_log_csv": audit_log,
        "nginx_conf": nginx,
        "kubernetes_yaml": k8s,
        "env_file": env,
        "dev_tasks_md": dev_tasks,
        "gateway_router_conf": gateway_conf,
        "backup_key": bkey,
        "backup_status_txt": bstatus,
        "sshd_config": sshd_config,
        "redis_config": redis_conf,
        "postgresql_config": postgresql_conf,
        "emails": emails
    }

if __name__ == "__main__":
    # Test print to verify
    data = get_generated_all()
    print("Employee CSV lines count:", len(data["employees_csv"].split("\n")))
    print("Client JSON length:", len(data["clients_json"]))
    print("Infrastructure YAML length:", len(data["infrastructure_yaml"]))
    print("Generated documents keys:", list(data["documents"].keys()))
    print("SSH Private Key length:", len(data["ssh_private_key"]))
    print("Shadow File length:", len(data["shadow_file"]))
    print("AWS Credentials length:", len(data["aws_credentials"]))
    print("AWS Config length:", len(data["aws_config"]))
    print("Kube Config length:", len(data["kube_config"]))
    print("Netplan Config length:", len(data["netplan_config"]))
    print("Hosts File length:", len(data["hosts_file"]))
    print("PGPass File length:", len(data["pgpass_file"]))
    print("Slack Webhook config length:", len(data["slack_config_json"]))
    print("Stripe config length:", len(data["stripe_config_json"]))
    print("DB Backup length:", len(data["db_backup_sql"]))
    print("Audit Log length:", len(data["audit_log_csv"]))
    print("Nginx config length:", len(data["nginx_conf"]))
    print("Kubernetes YAML length:", len(data["kubernetes_yaml"]))
    print("Env file length:", len(data["env_file"]))
    print("Dev Tasks length:", len(data["dev_tasks_md"]))
    print("Gateway Router Conf length:", len(data["gateway_router_conf"]))
    print("Backup Key length:", len(data["backup_key"]))
    print("Backup Status length:", len(data["backup_status_txt"]))
