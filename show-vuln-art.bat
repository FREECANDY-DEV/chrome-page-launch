@echo off
cd /d "%~dp0"
echo vuln part
echo Opening a GUI message with the ASCII art.
python show-vuln-art.py
if errorlevel 1 py -3 show-vuln-art.py
