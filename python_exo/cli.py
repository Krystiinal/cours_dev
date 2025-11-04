import argparse
from scan import validate_port, validate_ip, scan

# -p,--port
# -i,--ip

# parser = argparse.ArgumentParser()
# parser.add_argument("-m", "--message", help="a message")
# args = parser.parse_args()
# if args.message:
#     print(args.message)


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="ip")
parser.add_argument("-p", "--port", help="port")
arg = parser.parse_args()
port_arg = arg.port
ip_arg = arg.ip

if not validate_ip(ip_arg):
    print("IP invalide!")
    exit(1)  # Arrêter le programme

if "," in port_arg:
    port_list = port_arg.split(",")
    for element in port_list:
        if validate_port(element):
            scan(ip_arg, int(element))
        else:
            print(f"Port invalide: {element}")
            exit(1)
else:
    if validate_port(port_arg):
        scan(ip_arg, int(port_arg))
