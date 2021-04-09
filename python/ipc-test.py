import argparse
import os
import socket
import sys
import time

# Address for Unix Domain Socket
#
# Note: This assumes the path will exist. For k8s testing,
#       this is being provided through a shared volume mount
#       to allow consumers and producers to access it.
SOCKET_ADDRESS = '/ipc_test/test_socket'

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--num_messages",
            type=int, 
            help="The number of messages to send. Only used when running as the producer")
    parser.add_argument(
            "--producer",
            help="Run as the IPC producer. Users must specify only one of the \'consumer\' or \'producer\' flags.",
            action="store_true")
    parser.add_argument(
            "--consumer",
            help="Run as the IPC consumer. Users must specify only one of the \'consumer\' or \'producer\' flags.",
            action="store_true")

    return parser.parse_args()

def consumer():
    print("Consumer: Running as consumer")

    # Connect to the socket established by the producer and wait for data
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(SOCKET_ADDRESS)
    try:
        print("Consumer: Connected to Producer")
        flag = True
        while flag:
            data = sock.recv(1024).decode()
            print("Consumer: Received message = {}".format(data))
            if data == 'Exit':
                flag = False;
            time.sleep(1)
    finally:
        print("Consumer: Closing socket")
        sock.close()
        

def unbindSocket():
    try:
        os.unlink(SOCKET_ADDRESS)
    except OSError:
        if os.path.exists(SOCKET_ADDRESS):
            raise

def producer(messages):
    print("Producer: Running as producer")
    if messages is None:
        print("Producer: Num messages was not set. Aborting.");
        exit(1)
   
    # Ensure socket is not already in use
    unbindSocket()

    # Establish new socket and wait for connection.
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(SOCKET_ADDRESS)
    sock.listen(1)

    completed = True;
    while completed:
        print("Producer: Waiting for client...")
        connection, client = sock.accept()

        # Once a connection is established, send the specified number of messages.
        # These messages will be sent at 5 second intervals.
        try:
            print("Producer: Found client")
            for x in range(messages):
                tmp_message = 'Sending Message: {}'.format(x)
                connection.send(tmp_message.encode('utf-8'))
                time.sleep(5)
            connection.send('Exit'.encode('utf-8'))
            completed = False
        finally:
            print("Producer: Closing connection")
            connection.close()



def main(args):
    if args.consumer and args.producer:
        print("Invalid arguments. Cannot be both producer and consumer.")
        exit(1)
    if args.consumer:
        consumer()
    elif args.producer:
        producer(args.num_messages)
    else:
        print("No argument specified")
        exit(1)


if __name__ == "__main__":
    main(parseArgs());
