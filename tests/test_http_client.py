import unittest
from unittest.mock import MagicMock

from enums.client_messages_response import ClientMessagesResponse
from http_client import HttpClient


class TestClient(unittest.TestCase):
    def test_create_request(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'cookie': {
                'name': 'ilya',
                'surname': 'fomko'
            },
            'headers': {
                'Host': '127.0.0.1'
            },
            'body': 'Привет, мир!',
            'request': 'GET'
        }

        expected_result = f'GET / HTTP/1.1\r\n' + \
                          f'Host: 127.0.0.1\r\n' \
                          f'Cookie: name=ilya; surname=fomko\r\n\r\n' \
                          f'Привет, мир!'

        self.assertEqual(HttpClient.create_http_request(settings), expected_result)

    #
    def test_create_request_without_cookie(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'cookie': {},
            'headers': {
                'Host': '127.0.0.1'
            },
            'body': 'Привет, мир!',
            'request': 'GET'
        }

        expected_result = f'GET / HTTP/1.1\r\n' + \
                          f'Host: 127.0.0.1\r\n\r\n' \
                          f'Привет, мир!'

        self.assertEqual(HttpClient.create_http_request(settings), expected_result)

    def test_create_request_without_headers(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'cookie': {
                'name': 'ilya',
                'surname': 'fomko'
            },
            'headers': {},
            'body': 'Привет, мир!',
            'request': 'GET'
        }

        expected_result = f'GET / HTTP/1.1\r\n' + \
                          f'Cookie: name=ilya; surname=fomko\r\n\r\n' \
                          f'Привет, мир!'

        self.assertEqual(HttpClient.create_http_request(settings), expected_result)

    def test_create_headers_string_with_cookie(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'cookie': {
                'name': 'ilya',
                'surname': 'fomko'
            },
            'headers': {
                'Host': '127.0.0.1',
                'Connection': 'keep-alive'
            },
            'body': 'Привет, мир!',
            'request': 'GET'
        }

        expected_result = 'Host: 127.0.0.1\r\nConnection: keep-alive\r\nCookie: name=ilya; surname=fomko\r\n'

        self.assertEqual(HttpClient.get_headers(settings), expected_result)

    def test_create_headers_string_without_cookie(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'cookie': {},
            'headers': {
                'Host': '127.0.0.1',
                'Connection': 'keep-alive'
            },
            'body': 'Привет, мир!',
            'request': 'GET'
        }

        expected_result = 'Host: 127.0.0.1\r\nConnection: keep-alive\r\n'

        self.assertEqual(HttpClient.get_headers(settings), expected_result)

    def test_create_close_http_request(self):
        settings = {
            'url': '127.0.0.1',
            'request': 'GET'
        }

        expected_result = 'GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n'

        self.assertEqual(HttpClient.create_http_close_request(settings), expected_result)

    def test_create_close_request(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'cookie': {
                'name': 'ilya',
                'surname': 'fomko'
            },
            'headers': {
                'Host': '127.0.0.1'
            },
            'body': 'Привет, мир!',
            'request': 'GET'
        }

        expected_result = 'GET / HTTP/1.1\r\n' \
                          'Host: 127.0.0.1\r\n' \
                          'Connection: close\r\n\r\n'

        self.assertEqual(expected_result, HttpClient.create_http_close_request(settings))

    def test_create_headers(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'cookie': {
                'name': 'ilya',
                'surname': 'fomko'
            },
            'headers': {
                'Host': '127.0.0.1'
            },
            'body': 'Привет, мир!',
            'request': 'GET'
        }

        expected_result = 'Host: 127.0.0.1\r\nCookie: name=ilya; surname=fomko\r\n'

        self.assertEqual(expected_result, HttpClient.get_headers(settings))

    def test_receive_data(self):
        socket = MagicMock()
        socket.recv.side_effect = [b'test_data', None]

        expected_result = b'test_data'

        self.assertEqual(expected_result, HttpClient.receive_data(socket))

    def test_send_data(self):
        data = 'test send data'

        expected_result = len(data.encode())

        socket = MagicMock()
        socket.send.side_effect = [expected_result, 0]

        self.assertEqual(expected_result, HttpClient.send_data(socket, data))

    def test_connect_with_host_or_port_exc(self):
        settings = {
            'url': 'xcvx',
            'port': -234,
            'cookie': {
                'name': 'ilya',
                'surname': 'fomko'
            },
            'headers': {
                'Host': '127.0.0.1'
            },
            'body': 'Привет, мир!',
            'request': 'GET'
        }

        self.assertEqual(str(ClientMessagesResponse.incorrect_url_or_port.value), HttpClient(settings).get_data())


if __name__ == '__main__':
    unittest.main()
