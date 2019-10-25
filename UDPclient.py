import socket
import sys
import atexit
import select

open_socket = False

# Handle cleanup on exit
def exit_handler():
    if (open_socket):
        print >> sys.stderr, 'closing socket'
        sock.close()

atexit.register(exit_handler)

# Set address information
server_address = ('localhost', 12000)

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

            message = input

            # Create a UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            open_socket = True

            # Reset default timeout
            d = 0.1

            # Begin send/wait loop
            wait = True
            while wait == True:

                try:
                    # Send message to server
                    print >> sys.stderr, '\nsending "%s" to "%s" port %s' % (
                    message, server_address[0], server_address[1])
                    sent = sock.sendto(message, server_address)

                    # Wait for response
                    print >> sys.stderr, 'waiting for reply'

                    # Set socket to non-blocking (won't hang if no data, socket timeout essentially 0)
                    sock.setblocking(0)

                    # Wait for readable data on socket, with timeout value d
                    ready = select.select([sock],[],[],d)
                    if ready[0]:
                        # Receive response
                        data, server = sock.recvfrom(2048)
                        print >> sys.stderr, 'received "%s"' % data
                        wait = False
                    else:
                        d=d*2
                        if d>2:
                            print("Timeout delay exceeds 2 seconds. Stopping.")
                            sys.exit(0)
                        # Loop and resend message
                        print("No reply before timeout. Resending message.")

                except socket.error:
                    print("\nConnection could not be established. Is the server running?")
                    sock.close()
                    open_socket = False
                    wait = False

            # Close socket when done
            print >> sys.stderr, 'closing socket'
            sock.close()
            open_socket = False