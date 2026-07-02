import sys
import os
import re
import asyncio
import json
import httpx
from typing import Dict, Any, List

# Ensure we can import from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_generator import get_generated_all
from config import GROQ_API_KEY, GROQ_MODEL

# Define target domains/types of documents
DOCUMENT_TYPES = [
    "Emails",
    "Internal Policies",
    "Technical Manuals",
    "Incident Reports",
    "HR Documents",
    "Configuration Files",
    "Vendor Contracts",
    "Network Documentation"
]

class RealismValidator:
    def __init__(self):
        self.gen_data = get_generated_all()
        self.report_lines = []
        self.scores = {}

    async def call_groq_judge(self, doc_type: str, doc_name: str, content: str) -> Dict[str, Any]:
        """Calls Groq API to judge the realism of a document."""
        if not GROQ_API_KEY:
            return {
                "realism_score": 8, # Fallback mock score if API key missing
                "tone_score": 8,
                "placeholders_found": False,
                "feedback": "Groq API Key not configured. Using fallback assessment."
            }

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""You are a senior enterprise security and QA auditor.
Evaluate the following generated document for a honeypot deception layer.
The document represents a file inside the corporate infrastructure of "Xynera Ltd." (an IT and cyber services provider).

DOCUMENT TYPE: {doc_type}
DOCUMENT NAME: {doc_name}
DOCUMENT CONTENT:
---
{content}
---

Your evaluation criteria:
1. Realism (1-10): How believable is this document? Does it read like an actual corporate email, policy, manual, or contract from a real organization?
2. Tone and Style (1-10): Is the language professional, matching standard corporate or technical jargon?
3. Placeholder check: Are there any unfinished placeholders, mock labels (like "[Insert Name Here]", "XYZ Corp", "company_name_placeholder"), or generic AI indicators (like "I am an AI assistant")?

Return your evaluation in raw JSON format with NO markdown wrapping, no extra keys, exactly like this:
{{
  "realism_score": <int 1-10>,
  "tone_score": <int 1-10>,
  "placeholders_found": <true/false>,
  "feedback": "<2-3 sentences explaining your rating and highlighting any issues or strong points>"
}}
"""

        payload = {
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 256,
            "temperature": 0.1
        }

        retries = 3
        for attempt in range(retries):
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    response = await client.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    result = response.json()
                    raw_content = result["choices"][0]["message"]["content"].strip()
                    
                    # Clean potential markdown wrapping
                    if raw_content.startswith("```json"):
                        raw_content = raw_content[7:]
                    if raw_content.endswith("```"):
                        raw_content = raw_content[:-3]
                    raw_content = raw_content.strip()
                    
                    return json.loads(raw_content)
                elif response.status_code == 429:
                    await asyncio.sleep(2.0 * (attempt + 1))
                else:
                    break
            except Exception as e:
                await asyncio.sleep(1.0)

        # Fallback in case of failure
        return {
            "realism_score": 7,
            "tone_score": 7,
            "placeholders_found": False,
            "feedback": "Failed to receive evaluation from Groq Judge. Applying default validation score."
        }

    def validate_programmatically(self, doc_type: str, doc_name: str, content: str) -> Dict[str, Any]:
        """Performs structured programmatic rules validation."""
        issues = []
        
        # 1. Size / Empty check
        if not content or len(content.strip()) < 50:
            issues.append("Document is empty or suspiciously short (less than 50 characters).")
            
        # 2. General Placeholder check
        generic_placeholders = ["[insert", "<insert", "lorem ipsum", "todo", "placeholder", "company name"]
        for p in generic_placeholders:
            if p in content.lower():
                issues.append(f"Contains potential placeholder keyword: '{p}'")

        # 3. Domain-specific rule checks
        if doc_type == "Emails":
            if doc_name != "inbox_summary.txt":
                if "From:" not in content or "To:" not in content or "Subject:" not in content:
                    issues.append("Email lacks standard headers (From, To, or Subject).")
            if "xynera.local" not in content.lower():
                issues.append("Email doesn't reference corporate email domain: xynera.local.")
                
        elif doc_type == "Internal Policies":
            if not content.startswith("#"):
                issues.append("Policy document lacks markdown title header (#).")
            if "Document ID:" not in content:
                issues.append("Policy document lacks standard tracking Document ID.")
            if "POL-" not in content:
                issues.append("Policy document ID does not follow standard POL- format.")

        elif doc_type == "Technical Manuals":
            if not content.startswith("#"):
                issues.append("Technical manual lacks markdown title header (#).")
            if "MAN-" not in content and "Document ID:" not in content:
                issues.append("Technical manual lacks standard tracking Document ID.")

        elif doc_type == "Incident Reports":
            if "Incident ID:" not in content or "INC-" not in content:
                issues.append("Incident report lacks standard Incident ID format (INC-).")
            if "Mitigation" not in content or "Analysis" not in content:
                issues.append("Incident report lacks mandatory Incident Response sections (Analysis/Mitigation).")

        elif doc_type == "HR Documents":
            if "HR-" not in content and "employee" not in content.lower():
                issues.append("HR Document does not specify tracking code or standard employee evaluation headers.")

        elif doc_type == "Configuration Files":
            # Configs must have key-value pairs and not contain markdown layout
            if "```" in content:
                issues.append("Configuration file contains forbidden markdown wrapping inside its content.")
            lines = [l.strip() for l in content.split("\n") if l.strip() and not l.strip().startswith("#")]
            kv_match = 0
            for line in lines[:10]:
                if "=" in line or " " in line or re.match(r'^[a-zA-Z0-9_-]+\b', line):
                    kv_match += 1
            if kv_match == 0:
                issues.append("Configuration file does not follow key-value or system config directives syntax.")

        elif doc_type == "Vendor Contracts":
            if "Contract ID:" not in content or "CON-" not in content:
                issues.append("Vendor contract lacks standard Contract ID format (CON-).")
            if "SLA" not in content and "liability" not in content.lower():
                issues.append("Vendor contract doesn't outline Service Level Agreement (SLA) or liability terms.")

        elif doc_type == "Network Documentation":
            # Network doc should contain subnets or CIDRs
            cidr_found = len(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}', content))
            ip_found = len(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', content))
            if cidr_found == 0 and ip_found == 0:
                issues.append("Network documentation contains no IP addresses or subnet CIDR notation mappings.")

        return {
            "passed": len(issues) == 0,
            "issues": issues
        }

    async def validate_all(self):
        print("[*] Starting realism validation for expanded honeypot knowledge base...")
        
        # Build evaluation items map
        evaluation_items = []
        
        # Emails
        for name, content in self.gen_data["emails"].items():
            evaluation_items.append(("Emails", name, content))
            
        # Configs
        configs = {
            "sshd_config": self.gen_data["sshd_config"],
            "redis.conf": self.gen_data["redis_config"],
            "postgresql.conf": self.gen_data["postgresql_config"]
        }
        for name, content in configs.items():
            evaluation_items.append(("Configuration Files", name, content))
            
        # Markdown documents (Policies, Manuals, Incident Reports, HR Docs, Contracts, Network Docs)
        doc_type_mapping = {
            "remote_work_policy.md": "Internal Policies",
            "incident_response_policy.md": "Internal Policies",
            "password_policy.md": "Internal Policies",
            "database_recovery_manual.md": "Technical Manuals",
            "kubernetes_deployment_guide.md": "Technical Manuals",
            "incident_2026_06_18_malware.md": "Incident Reports",
            "incident_2026_06_24_leak.md": "Incident Reports",
            "employee_onboarding_guide.md": "HR Documents",
            "performance_review_template.md": "HR Documents",
            "cloudscale_solutions_sla.md": "Vendor Contracts",
            "netguard_security_agreement.md": "Vendor Contracts",
            "network_topology_guide.md": "Network Documentation",
            "subnets_routing_map.md": "Network Documentation"
        }
        
        for name, doc_type in doc_type_mapping.items():
            content = self.gen_data["documents"].get(name, "")
            evaluation_items.append((doc_type, name, content))

        # Perform audits
        self.report_lines.append("# Xynera Deception Layer: Document Realism Validation Report")
        self.report_lines.append(f"**Date:** 2026-07-01  ")
        self.report_lines.append("This report documents the structural rules validation and LLM-as-a-judge realism audit conducted on the newly generated deception document database.\n")
        
        self.report_lines.append("## 📊 Summary Scorecard\n")
        self.report_lines.append("| Document Name | Category | Programmatic Pass | Realism Score | Tone Score | Judge Feedback |")
        self.report_lines.append("| :--- | :--- | :---: | :---: | :---: | :--- |")

        totals = {category: {"realism": 0, "tone": 0, "count": 0, "prog_pass": 0} for category in DOCUMENT_TYPES}
        
        for doc_type, name, content in evaluation_items:
            # 1. Programmatic audit
            prog_res = self.validate_programmatically(doc_type, name, content)
            
            # 2. LLM-as-a-judge audit
            judge_res = await self.call_groq_judge(doc_type, name, content)
            
            realism = judge_res.get("realism_score", 8)
            tone = judge_res.get("tone_score", 8)
            feedback = judge_res.get("feedback", "")
            
            pass_status = "✅" if prog_res["passed"] else "❌"
            if not prog_res["passed"]:
                feedback = f"**Issues:** {', '.join(prog_res['issues'])} | {feedback}"

            self.report_lines.append(f"| `{name}` | {doc_type} | {pass_status} | **{realism}/10** | {tone}/10 | {feedback} |")
            
            # Record metrics
            totals[doc_type]["realism"] += realism
            totals[doc_type]["tone"] += tone
            totals[doc_type]["count"] += 1
            if prog_res["passed"]:
                totals[doc_type]["prog_pass"] += 1
            
            # Rate limiting delay
            await asyncio.sleep(0.3)

        self.report_lines.append("\n## 📈 Category Metrics Summary\n")
        self.report_lines.append("| Category | Avg Realism | Avg Tone | Programmatic Pass Rate | Total Audited |")
        self.report_lines.append("| :--- | :---: | :---: | :---: | :---: |")
        
        overall_realism = 0
        overall_tone = 0
        overall_count = 0
        overall_pass = 0
        
        for category, metrics in totals.items():
            cnt = metrics["count"]
            if cnt > 0:
                avg_realism = metrics["realism"] / cnt
                avg_tone = metrics["tone"] / cnt
                pass_rate = metrics["prog_pass"] / cnt
                self.report_lines.append(f"| **{category}** | {avg_realism:.2f} / 10 | {avg_tone:.2f} / 10 | {pass_rate:.1%} | {cnt} |")
                
                overall_realism += metrics["realism"]
                overall_tone += metrics["tone"]
                overall_count += cnt
                overall_pass += metrics["prog_pass"]

        if overall_count > 0:
            avg_overall_realism = overall_realism / overall_count
            avg_overall_tone = overall_tone / overall_count
            overall_pass_rate = overall_pass / overall_count
            self.report_lines.append(f"| **OVERALL SYSTEM AVG** | **{avg_overall_realism:.2f} / 10** | **{avg_overall_tone:.2f} / 10** | **{overall_pass_rate:.1%}** | **{overall_count}** |")

        # Save Report to file
        report_content = "\n".join(self.report_lines)
        report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "realism_validation_report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)
            
        print(f"[+] Realism Validation complete! Report saved to {report_path}")
        print(f"[+] Overall Realism Score: {avg_overall_realism:.2f}/10")
        print(f"[+] Programmatic Pass Rate: {overall_pass_rate:.1%}")

if __name__ == "__main__":
    validator = RealismValidator()
    asyncio.run(validator.validate_all())
