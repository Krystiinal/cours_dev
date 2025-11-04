import socket

# NOTE: listen on port 1337 with netcat: nc -l 1337


def scan(ip_target, port_target):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(3)
            s.connect((ip_target, port_target))
            print("OK")
        except (TimeoutError, ConnectionRefusedError) as e:
            print(e)
