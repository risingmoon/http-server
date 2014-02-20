import socket

ADDRESS, PORT = '127.0.0.1', 50000

def parse_request(message):
    return method, uri, protocol = message.split() 

def socket_setup(ADDRESS, PORT):
    """Returns and setup a socket based on this
    project's configuration"""
    return socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP)

def recv(socket, buffer_size):
    """Receives Data Interface by passing socket
    and buffer_size argument into this method"""
    response = ''
    done = False
    while not done:
        msg_part = socket.recv(buffer_size)
        response += msg_part
        if len(msg_part) < buffer_size:
            done = True
    return response

if __name__ == '__main__':
    server_socket = socket_setup()
    server_socket.bind((ADDRESS, PORT))
    server_socket.listen(1)

    client_socket.connect(('127.0.0.1',50000))
    server.client_socket.sendall(sys.argv[1])
    client_socket.shutdown(socket.SHUT_WR)