import unittest
import socket
from http_server import *

MESSAGE = """GET /index.html HTTP/1.1\r\n"""
METHODS= ["GET","POST","DELETE","UPDATE"]

class HttpServerTest(unittest.TestCase):

    def setUp(self):
         self.server_socket = socket_setup(ADDRESS, PORT)
         self.client_socket = socket_setup(ADDRESS, PORT)

    def connect_client_server(self,message):
        self.server_socket.bind((ADDRESS, PORT))
        self.server_socket.listen(1)

        self.client_socket.connect((ADDRESS, PORT))
        self.client_socket.sendall(message)
        self.client_socket.shutdown(socket.SHUT_WR)

        connection, address = self.server_socket.accept()
        response = recv(connection,32)
        connection.close()
        self.client_socket.close()
        self.server_socket.close()
        return response

    def test_socket_setup(self):
        response = self.connect_client_server(MESSAGE)
        self.assertEqual(response,MESSAGE)

    def test_parse_request(self):
        method, uri, protocol = parse_request(MESSAGE)
        self.assertIn(method, METHODS)

if __name__ == '__main__':
    unittest.main()
