from __future__ import division
import socket
import sys
import re
import atexit


# Closes connection and listening sockets on exit
def exit_handler():
    print("Closing connection...")
    connection.close()
    sock.close()

atexit.register(exit_handler)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)


while True:

    # Listen for incoming connections (queue at most 1 incoming connection)
    sock.listen(1)
    command = ''
    print >>sys.stderr, '\nwaiting for a connection'

    # Accept connection with new connection socket
    connection, client_address = sock.accept()
    try:
        print >> sys.stderr, 'connection from', client_address

        # Get data from connection socket
        data = connection.recv(1024)
        print("data received")
        if data:

            command = data

            # Close server and socket(s)
            if command == "KILL":
                sys.exit(0)

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
            connection.sendall(r_msg)

    finally:

        # Clean up the connection
        print("closing socket")
        connection.close()
