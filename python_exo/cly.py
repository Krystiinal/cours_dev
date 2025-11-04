import argparse

# -p,--port
# -i,--ip

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--message", help="a message")
args = parser.parse_args()
if args.message:
    print(args.message)
