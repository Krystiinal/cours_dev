import socket

# NOTE: listen on port 1337 with netcat: nc -l 1337


def scan(ip_target, port_target):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(3)
            s.connect((ip_target, port_target))
            print("OK")
            return "Port ouvert"
        except (TimeoutError, ConnectionRefusedError) as e:
            print(e)
            return f"Port fermé ou erreur: {e}"


def validate_port(port):
    try:
        p = int(port)
        if p in range(0, 65536):
            return True
        else:
            return False
    except ValueError as e:
        return False


def validate_ip(ip):
    adress = ip.split(".")
    if len(adress) == 4:
        for element in adress:
            try:
                e = int(element)
                if not (0 <= e <= 256):
                    return False
            except ValueError as e:
                return False
        return True
    else:
        return False


if __name__ == "__main__":
    # Test validate_port
    print("Port 65535:", validate_port("65535"))  # Doit être True

    # Test validate_ip
    print("IP 192.168.1.1:", validate_ip("192.168.1.1"))  # Doit être True
    print("IP 256.1.1.1:", validate_ip("256.1.1.1"))  # Doit être False
