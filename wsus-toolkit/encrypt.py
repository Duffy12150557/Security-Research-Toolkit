# -*- coding: utf-8 -*-
"""
WSUS Security Research Toolkit - Payload preparation utility.
Prepares Base64-encoded test data for use with exp.py.
"""
import argparse
import base64
import sys

from ui import banner, box, box_bottom, line, ok, fail, warn, info, section


def encode_file(input_path, output_path, key_hex=None):
    """
    Read binary file, optionally XOR with key, then Base64 encode and write to output.
    """
    try:
        with open(input_path, "rb") as f:
            data = bytearray(f.read())
    except FileNotFoundError:
        fail("Input file not found: " + input_path)
        return False
    except Exception as e:
        fail("Read error: " + str(e))
        return False

    if key_hex:
        try:
            key = bytes.fromhex(key_hex.replace(" ", ""))
            if not key:
                warn("Empty key; writing raw Base64.")
            else:
                for i in range(len(data)):
                    data[i] ^= key[i % len(key)]
        except ValueError as e:
            fail("Invalid hex key: " + str(e))
            return False

    b64 = base64.b64encode(bytes(data)).decode("ascii")

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(b64)
    except Exception as e:
        fail("Write error: " + str(e))
        return False

    ok("Written " + str(len(b64)) + " chars to " + output_path)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="WSUS Toolkit - Payload encoder for test data preparation."
    )
    parser.add_argument("-i", "--input", required=True, help="Input binary file")
    parser.add_argument("-o", "--output", required=True, help="Output file (Base64 text)")
    parser.add_argument("--key", default=None, help="Optional XOR key (hex string)")
    args = parser.parse_args()

    banner()
    section(" Payload Encoder ")
    info("Input:  " + args.input)
    info("Output: " + args.output)
    if args.key:
        info("Key:    " + args.key[: min(32, len(args.key))] + ("..." if len(args.key) > 32 else ""))
    else:
        info("Key:    (none - raw Base64)")
    print(box_bottom(60))
    section(" Processing ")
    success = encode_file(args.input, args.output, args.key)
    print(box_bottom(60))
    if success:
        info("Use the output file as payload.txt or paste into payload.txt for exp.py")
    print()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
