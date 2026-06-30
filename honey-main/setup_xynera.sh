#!/bin/bash

# Exit on error
set -e

echo "=== Xynera Honeypot Installer ==="

# 1. Update system packages
echo "[*] Updating apt package lists..."
sudo apt update -y

# 2. Install Python 3, pip, and venv if not present
echo "[*] Installing Python 3, pip, and virtual environment utilities..."
sudo apt install python3 python3-pip python3-venv build-essential -y

# 3. Setup AI Backend Environment
echo "[*] Setting up AI Backend Environment..."
cd "$(dirname "$0")/xynera-ai"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
echo "[*] Installing AI Backend dependencies..."
pip install --upgrade pip
pip install flask requests
# Note: if coeai is available locally or via pip, install it:
pip install coeai || echo "[!] Notice: coeai package not found in public pip, ignoring."
deactivate
cd ..

# 4. Setup Honeypot Environment
echo "[*] Setting up Honeypot Environment..."
cd xynera-honey
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
echo "[*] Installing Honeypot dependencies..."
pip install --upgrade pip
pip install requests
deactivate
cd ..

echo "================================="
echo "[+] Setup Complete successfully!"
echo "================================="
echo "To start the AI backend, open a terminal and run:"
echo "  cd $(pwd)/xynera-ai && source venv/bin/activate && python3 api_server.py"
echo ""
echo "To start the Honeypot, open another terminal and run:"
echo "  cd $(pwd)/xynera-honey && source venv/bin/activate && python3 server.py"
echo "================================="
