from __future__ import division
import socket
import sys
import re
import atexit
import random

# Handle cleanup on exit
def exit_handler():
    print("Closing connection...")
    if open_socket:
        sock.close()

atexit.register(exit_handler)

open_socket = False

# Set random ignore rate
error = 0
if len(sys.argv) == 2:
    error = float(sys.argv[1])
    if error > 1:
        print("Invalid, argument over 1")
        sys.exit(0)
#print('error set to: %s' % error)

# Set address information
server_address = ('localhost', 12000)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
open_socket = True

# Bind the socket to the server address
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

while True:
    command = ''
    print >> sys.stderr, '\nwaiting to receive message'

    # Receive data from client
    data, address = sock.recvfrom(2048)

    rand = random.random()
    #print('rand = %s' % rand)

    command = data

    # Notify client and close server (
    if command == "KILL":
        sock.sendto('server killed', address)
        sys.exit(0)

    # Ignore incoming data if false
    if rand > error:

        print >> sys.stderr, 'received %s bytes from %s' % (len(data), address)
        print >> sys.stderr,'"%s"' % data

        if data:

            # Parse command, check for invalid entry, return result
            e_msg = ''

            # Split command using accepted operator as delimiter
            parse = re.split(r'[+-/*]', command)

            # Check if two operands
            if len(parse) != 2:
                s_code = "300"
                e_msg = "-Invalid command"
                result = -1

            # Check both operands are integers
            elif not parse[0].strip().isdigit() or not parse[1].strip().isdigit():
                s_code = "300"
                e_msg = "-Invalid command"
                result = -1

            # Check if division by zero
            elif parse[1] == "0" and "/" in command:
                s_code = "300"
                e_msg = "-Cannot divide by zero"
                result = -1

            # Valid command, use eval() to calculate
            else:
                s_code = "200"
                result = eval(command)

            # Assemble return message and send
            r_msg = "Status code: " + s_code + e_msg + ", Result: %s" % result
            print >> sys.stderr, 'sending data back to the client'
            sent = sock.sendto(r_msg, address)
            print >> sys.stderr, 'sent %s bytes back to %s' % (sent, address)

    else:
        print("Incoming data 'lost'")