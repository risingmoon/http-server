import unittest
from http_server import *


class HttpServerTest(unittest.TestCase):
    def setUp(self):
        self.server_socket = socket_setup()
        self.client_socket = socket_setup()

    def disconnect(self):
        self.server_socket.close()
        self.client_socket.close()

    def connect(self):
        self.server_socket.bind((ADDRESS, PORT))
        self.server_socket.listen(1)
        self.client_socket.connect((ADDRESS, PORT))

    def send_message(self, message):
        self.client_socket.sendall(message)
        self.client_socket.shutdown(socket.SHUT_WR)
        connection, address = self.server_socket.accept()
        response = recv(connection, BUFFER_SIZE)
        connection.close()
        return response

    def test_setup(self):
        message = "THIS IS A TEST"
        self.connect()
        response = self.send_message(message)
        self.disconnect()
        self.assertEqual(response, message)

    def test_check_methods(self):
        self.assertIsNone(check_method('GET'))
        with self.assertRaises(Error405):
            check_method("PUT")
        with self.assertRaises(Error405):
            check_method("POST")
        with self.assertRaises(Error405):
            check_method("DELETE")

    def test_check_uri(self):
        self.assertEqual(
            'webroot/a_web_page.html',
            check_uri('/a_web_page.html/'))
        with self.assertRaises(Error404):
            check_uri('/a_web_pag.html/')

if __name__ == "__main__":
    unittest.main()
