================================================================================
  WSUS Security Research Toolkit - Installation Guide [CVE-2025-59287]
================================================================================

System Requirements
-------------------
  Operating System: Windows 10/11 or Linux (Ubuntu 20.04+)
  Python Version:   3.4 or higher
  Network Access:   Connection to target WSUS server

Installation Steps
------------------
  1. Install dependencies:
       pip install -r requirements.txt

  2. Check Python version:
       python --version

  3. Ensure these files are in the same directory:
       exp.py       - Main execution script
       encrypt.py   - Payload preparation utility
       payload.txt  - Base64 encoded test data (optional)
       ui.py        - CMD styling (used by exp.py and encrypt.py)

Prepare Your Test Data
----------------------
  Method A: Using payload.txt
    - Create or edit payload.txt in the same directory as exp.py
    - Paste your Base64 encoded test data into the file
    - Save the file

  Method B: Using encrypt.py
    python encrypt.py -i input_file.bin -o output.txt --key YOUR_HEX_KEY
    Then copy output.txt content into payload.txt

Running the Toolkit
-------------------
  Basic:
    python exp.py http://wsus-server.example.local:8533

  Without delay:
    python exp.py http://192.168.1.100:8533 --no-wait

  Custom port:
    python exp.py http://wsus-lab.local:8534

  Help:
    python exp.py --help

Understanding the Output
------------------------
  The toolkit displays (in styled terminal boxes):
    - Connection status to WSUS server
    - SOAP request/response information
    - Success/failure status
    - Payload usage note

Troubleshooting
---------------
  "Connection refused": Check WSUS is running, firewall, IP and port.
  "Module not found":   Install requirements.txt; use Python 3.4+.
  "Permission denied":  Run with appropriate permissions.
  Payload not working:  Verify Base64; no extra spaces/newlines in payload.txt.

Security & Legal
----------------
  - Use only on systems you own or have written authorization to test.
  - Recommended for isolated lab environments.
  - Document all testing activities.
  - Comply with all applicable laws and regulations.

File Structure
--------------
  wsus-toolkit/
    exp.py         Main execution script
    encrypt.py     Payload encoder
    ui.py          Terminal UI
    payload.txt    Test data (optional)
    README.txt     This file
    requirements.txt

================================================================================
