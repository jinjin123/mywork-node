import socket
import sys

IP = sys.argv[1]
PORT = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(1)

try:
    sock.connect((IP,PORT))
    print 'ok'
    sock.close()
except:
    print 'error'
