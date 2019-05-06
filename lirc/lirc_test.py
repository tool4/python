#!/usr/bin/python
#import pylirc, time

#"/var/run/lirc/lircd"

import socket
import sys
import os

server_address = "/var/run/lirc/lircd"

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

print >>sys.stderr, 'connecting to %s' % server_address
try:
    sock.connect(server_address)

except socket.error, msg:
    print >>sys.stderr, msg
    sys.exit(1)

try:
    print("listening to: ", server_address)
#    sock.setblocking(False)
    while 1:
        data = sock.recv(64)
        if( (data) ):
            print(data)
        
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
