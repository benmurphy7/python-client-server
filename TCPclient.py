import socket
import sys
import atexit

open_socket = False

# Close open socket on exit (in case of error)
def exit_handler():
    if (open_socket):
        print >> sys.stderr, 'closing socket'
        sock.close()

atexit.register(exit_handler)
server_address = ('localhost', 10000)

# Repeat until stop command given
while True:

    # Take user input
    input = raw_input("\nEnter request (ex: 2+2), 'stop' to close client, 'kill' to kill server: ")
    input = input.upper()

    # 'stop' will close client
    # 'kill' will close server
    if input == "STOP":
        print("Closing client...")
        exit()
    else:
        if(input!=""):
            print >>sys.stderr, '\nRequest: %s' % input

            # Create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect the socket to the port where the server is listening
            print >>sys.stderr, 'connecting to "%s" port %s' % server_address
            try:
                sock.connect(server_address)
                open_socket = True

                # Send data using socket
                message = input
                print >> sys.stderr, 'Sending "%s"' % message
                sock.sendall(message)

                # Done sending over socket
                #sock.shutdown(1)

                # Receive reply data using socket
                data = sock.recv(1024)
                if data:
                    print >> sys.stderr, 'Received "%s"' % data

                # Close client socket
                print("closing socket")
                sock.close()
                open_socket = False

            except socket.error:
                print("\nConnection could not be established. Is the server running?")
                sock.close()
                open_socket = False
