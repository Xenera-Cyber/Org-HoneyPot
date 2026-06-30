import sys
import os

# Set up paths
sys.path.append(r"c:\Users\VIDIT RATURI\Downloads\honey-main\honey-main\xynera-honey")

from fake_filesystem import ls, cd, cat, resolve_path, filesystem, file_contents

# Initialize a dummy session
session = {
    "ip": "10.200.200.10",
    "cwd": "/home/ubuntu",
    "commands": []
}

print("=== Testing path resolution ===")
assert resolve_path("/home/ubuntu", "company_directory") == "/home/ubuntu/company_directory"
assert resolve_path("/home/ubuntu", "../../var/www") == "/var/www"
assert resolve_path("/", "etc/passwd") == "/etc/passwd"
assert resolve_path("/home/ubuntu/documents", "../company_directory/../notes.txt") == "/home/ubuntu/notes.txt"
print("Path resolution tests passed!")

print("\n=== Testing directory navigation and listing ===")
print("Current CWD:", session["cwd"])
print("Contents of CWD:")
print(ls(session))

print("\nNavigating to company_directory...")
err = cd(session, "company_directory")
assert err == "", f"CD failed: {err}"
print("New CWD:", session["cwd"])
print("Contents:")
print(ls(session))

print("\nReading employees.csv...")
contents = cat(session, "employees.csv")
print("First 3 lines of employees.csv:")
print("\n".join(contents.split("\n")[:3]))
assert "EmployeeID,Name,Email" in contents

print("\nNavigating to absolute path /var/www/internal...")
err = cd(session, "/var/www/internal")
assert err == ""
print("New CWD:", session["cwd"])
print("Contents:")
print(ls(session))
assert "infrastructure_assets.yaml" in ls(session)

print("\nReading infrastructure_assets.yaml...")
yaml_contents = cat(session, "infrastructure_assets.yaml")
print("First 3 lines of infrastructure_assets.yaml:")
print("\n".join(yaml_contents.split("\n")[:5]))
assert "infrastructure_assets:" in yaml_contents

print("\nNavigating back using relative paths cd ../../../home/ubuntu/documents/incident_reports...")
err = cd(session, "../../../home/ubuntu/documents/incident_reports")
assert err == ""
print("New CWD:", session["cwd"])
print("Contents:")
print(ls(session))
assert "incident_2026_05_12_ddos.md" in ls(session)

print("\nReading incident_2026_05_12_ddos.md...")
incident_contents = cat(session, "incident_2026_05_12_ddos.md")
print("Snippet:")
print("\n".join(incident_contents.split("\n")[:5]))
assert "Incident ID:" in incident_contents

print("\nAll filesystem checks passed successfully!")
