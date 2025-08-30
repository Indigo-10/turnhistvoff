# turnhistvoff

Exploit scripts for ISTS (Information Security Talent Search Competition) King of The Hill challenges. These scripts target specific vulnerabilities found in KOTH competition environments.

## What the scripts do

**tvoff.py** - Exploits a web application vulnerability:
- Targets ffmpeg-settings API endpoints
- Performs command injection through ffmpegPath parameter
- Downloads and executes payload scripts
- Creates KOTH flag files with specific UUIDs
- Uses curl to download payloads and establish persistence

**fart.py** - OpenSMTPD exploitation script:
- Exploits OpenSMTPD via SMTP command injection
- Injects commands through MAIL FROM field
- Creates KOTH flag files and user accounts
- Establishes persistence with hardcoded credentials

**fartgpt.py** - Cleaned up version of fart.py:
- Same OpenSMTPD exploitation technique
- Better error handling and code structure
- Accepts payload URL as parameter
- More reliable command execution flow

## Exploitation Details

Both main scripts create the same KOTH flag:
- File: `/home/$USER/koth.txt`
- Content: `cd1a5cf3-70b4-403b-a60e-cd883667dfa2`
- Creates user "datadag" with password "CCSOdog123"

## Usage

```bash
# Web application exploit
python3 tvoff.py <target_ip> <port> <payload_url>

# SMTP exploits  
python3 fart.py <victim_ip> <victim_port>
python3 fartgpt.py <victim_ip> <victim_port> <payload_url>
```

---
*Developed for ISTS cybersecurity competition participation*
