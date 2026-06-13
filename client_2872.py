#!/usr/bin/env python3
"""
client_2872.py
IE2102 - Network Programming
Student ID: IT24102872
FIX 3: Client now reads LEN-framed responses from server
"""

import socket

HOST = '127.0.0.1'
PORT = 50872

def send_cmd(sock, command):
    """Send LEN-framed command"""
    payload = command.encode('utf-8')
    frame   = f"LEN:{len(payload)}\n".encode() + payload
    sock.sendall(frame)

def recv_resp(sock):
    """
    FIX 3: Read LEN-framed response from server
    Server sends: LEN:<n>\n<payload>
    """
    # Step 1: Read header byte by byte until newline
    header = b""
    while True:
        ch = sock.recv(1)
        if not ch:
            return "[disconnected]"
        if ch == b'\n':
            break
        header += ch

    header_str = header.decode('utf-8').strip()

    # Step 2: Validate LEN:
    if not header_str.startswith("LEN:"):
        # fallback: return raw header
        return header_str

    # Step 3: Read exact payload bytes
    try:
        plen = int(header_str[4:])
    except ValueError:
        return f"[bad length: {header_str}]"

    if plen <= 0 or plen > 8192:
        return f"[invalid payload length: {plen}]"

    # Step 4: Read exact plen bytes
    payload = b""
    while len(payload) < plen:
        chunk = sock.recv(plen - len(payload))
        if not chunk:
            break
        payload += chunk

    return payload.decode('utf-8').strip()

def print_banner():
    print("╔══════════════════════════════════════════╗")
    print("║   IE2102 Client  |  IT24102872           ║")
    print("║   Server: 127.0.0.1:50872                ║")
    print("╠══════════════════════════════════════════╣")
    print("║  Commands:                               ║")
    print("║  REGISTER <user> <pass>                  ║")
    print("║  LOGIN    <user> <pass>                  ║")
    print("║  LOGOUT                                  ║")
    print("║  ECHO     <message with spaces>          ║")
    print("║  WHOAMI                                  ║")
    print("║  STATUS                                  ║")
    print("║  QUIT                                    ║")
    print("╚══════════════════════════════════════════╝")

def main():
    print_banner()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print(f"✓ Connected to {HOST}:{PORT}\n")

        while True:
            try:
                cmd = input("client>> ").strip()
                if not cmd:
                    continue

                send_cmd(sock, cmd)
                resp = recv_resp(sock)
                print(f"server<< {resp}\n")

                if cmd.upper() == "QUIT":
                    break

            except KeyboardInterrupt:
                print("\n[Ctrl+C] Disconnecting...")
                try:
                    send_cmd(sock, "QUIT")
                    recv_resp(sock)
                except:
                    pass
                break

    except ConnectionRefusedError:
        print(f"✗ Cannot connect to {HOST}:{PORT}")
        print("  → Is server running? Run: ./server_2872")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
