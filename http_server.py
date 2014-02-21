import socket
from os.path import isdir, isfile, exists
from os import listdir
from email.utils import formatdate
from mimetypes import guess_type

ADDRESS, PORT, BUFFER_SIZE = '127.0.0.1', 50000, 4092
PERMISSIONS = {"GET": 1, "POST": 0, "PUT": 0, "DELETE": 0}


def socket_setup():
    """Intialize socket"""
    return socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP)


def recv(socket, buffer_size):
    """parses buffer strings into response"""
    response = ''
    while True:
        msg_part = socket.recv(buffer_size)
        response += msg_part
        if len(msg_part) < buffer_size:
            break
    return response


def check_method(method):
    """Checks proper methods"""
    if method in PERMISSIONS:
        if PERMISSIONS[method]:
            pass
        else:
            raise Error405("METHOD NOT ALLOWED")
    else:
        raise Error400("BAD METHOD REQUEST")


def check_uri(uri):
    """Checks to see if URI is valid"""
    path_list = ["webroot"]
    path_list.extend([w for w in uri.split('/') if len(w) > 0])
    path = '/'.join(path_list)
    if exists(path):
        return path
    else:
        raise Error404('FILE NOT FOUND')


def map_uri(uri_path):
    """Maps URI onto webroot system"""
    if isdir(uri_path):
        list_dir = ['Current Path: %s' % (uri_path)]
        list_dir.extend(listdir(uri_path))
        body = "\r\n".join(list_dir)
        #print body
        content_type = 'text/plain'
        encoding = 'UTF-8'
        print "HERE"
        return (content_type, encoding, body)
    elif isfile(uri_path):
        content_type, encoding = guess_type(uri_path)
        with open(uri_path, 'rb') as file_handler:
            body = file_handler.read()
        return (content_type, encoding, body)
    else:
        raise Error500("Something is wrong...")


def parse_response(code, message, content_type=None, encoding=None):
    """Builds HTTP response based on HTTP Statuse"""
    header = []
    if code == 200:
        header.append("HTTP/1.1 200 OK")
        header.append(
            'Content-Type:%s; Char-Type:%s' % (content_type, encoding))
        header.append('Content-Length:%s' % str(len(message)))
        header.append("Date:%s" % formatdate(usegmt=True))
        return "\r\n".join(header) + '\r\n\r\n' + message
    else:
        print "THERE"
        print code
        header.append("HTTP/1.1 %s" % message)
        return "\r\n".join(header) + '\r\n\r\n'


def run_server():
    response = ''
    server_socket = socket_setup()
    server_socket.bind((ADDRESS, PORT))
    server_socket.listen(1)
    connection, address = server_socket.accept()
    message = recv(connection, BUFFER_SIZE)
    #request, body = message.split('\r\n', 1)
    #method, uri, protocol = request.split()
    method, uri, protocol = message.split()
    try:
        check_method(method)
        path = check_uri(uri)
        content_type, encoding, body = map_uri(path)
        response = parse_response(200, body, content_type, encoding)
    except Error400:
        response = parse_response(404, "BAD REQUEST")
    except Error404:
        print "HERE"
        response = parse_response(404, "FILE NOT FOUND")
    except Error405:
        response = parse_response(405, "METHOD NOT ALLOWED")
    finally:
        connection.sendall(response)
        connection.shutdown(socket.SHUT_WR)
        connection.close()


class Error400(Exception):
    pass


class Error404(Exception):
    pass


class Error405(Exception):
    pass


class Error500(Exception):
    pass
if __name__ == "__main__":
    while True:
        run_server()
