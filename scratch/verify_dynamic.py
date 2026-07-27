import asyncio
import sys
import os

# Prepend the xynera-ai folder to path to load imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "xynera-ai"))

from rag_engine import generate_deception
from attacker_profile import get_session_data

async def main():
    print("=== Verification of Dynamic Honeypot Deception ===")
    
    session_a = "session_alpha_123"
    session_b = "session_beta_456"
    
    # 1. Verify session consistency (same session returns same employees)
    data_a1 = get_session_data(session_a, commands=[])
    data_a2 = get_session_data(session_a, commands=[])
    
    emp_a1 = data_a1["employees_csv"].split("\n")[1].split(",")[1]
    emp_a2 = data_a2["employees_csv"].split("\n")[1].split(",")[1]
    
    print(f"\n[Test 1] Session A stability: {emp_a1} == {emp_a2} -> {emp_a1 == emp_a2}")
    
    # 2. Verify session randomization (different sessions return different employees)
    data_b = get_session_data(session_b, commands=[])
    emp_b = data_b["employees_csv"].split("\n")[1].split(",")[1]
    print(f"[Test 2] Session B randomization: {emp_a1} != {emp_b} -> {emp_a1 != emp_b}")
    
    # 3. Verify unique credentials
    aws_a = data_a1["aws_credentials"]
    aws_b = data_b["aws_credentials"]
    print(f"[Test 3] Unique credentials check: AWS keys are different -> {aws_a != aws_b}")
    
    # 4. Verify dynamic audit logs updating based on attacker actions
    cmds = ["whoami", "sudo su", "cat /etc/shadow"]
    data_a_updated = get_session_data(session_a, commands=cmds)
    audit_log = data_a_updated["audit_log_csv"]
    
    print("\n[Test 4] Dynamic Audit Log updated with attacker commands:")
    for cmd in cmds:
        present = cmd in audit_log
        print(f"  Command '{cmd}' logged: {present}")
        
    print("\n=== RAG Context Retrieval Interceptor Test ===")
    # Mock RAG call for session A
    output_a = await generate_deception("cat /home/ubuntu/company_directory/employees.csv", session_id=session_a)
    output_b = await generate_deception("cat /home/ubuntu/company_directory/employees.csv", session_id=session_b)
    
    first_emp_a = output_a.split("\n")[1].split(",")[1] if len(output_a.split("\n")) > 1 else "None"
    first_emp_b = output_b.split("\n")[1].split(",")[1] if len(output_b.split("\n")) > 1 else "None"
    
    print(f"RAG output Session A CEO/First Employee: {first_emp_a}")
    print(f"RAG output Session B CEO/First Employee: {first_emp_b}")
    print(f"RAG successfully returned unique session data -> {first_emp_a != first_emp_b}")

if __name__ == "__main__":
    asyncio.run(main())
