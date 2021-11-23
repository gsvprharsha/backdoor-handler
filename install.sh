#!/bin/sh

GREEN='\033[1;32m'
NC='\033[0m'

echo -e "${GREEN}[+] Installing the dependencies for tool to work perfectly${NC}"

pip3 install sockets
pip3 install termcolour
pip3 install os
pip3 install json
pip3 install subprocess
pip3 install pyautogui

echo -e "${GREEN}[+] All dependencies are installed & The tool is ready to be used. Have Fun!!${NC}"
