import json
import unittest
from unittest.mock import MagicMock

from http_server import HttpServer


class TestServer(unittest.TestCase):
    def test_validate_params_positive(self):
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

        self.assertEqual(HttpServer.validate_params(settings)[0], True)

    def test_validate_params_negative_1(self):
        settings = {
            'port': 4444,
            'cookie': {
                'name': 'ilya',
                'surname': 'fomko'
            },
            'body': 'Привет, мир!',
            'request': 'GET'
        }

        self.assertEqual(HttpServer.validate_params(settings)[0], False)

    def test_validate_params_negative_2(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'cookie': {
                'name': 'ilya',
                'surname': 'fomko'
            },
            'body': 'Привет, мир!',
        }

        self.assertEqual(HttpServer.validate_params(settings)[0], False)

    def test_validate_params_negative_3(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'cookie': {
                'name': 'ilya',
                'surname': 'fomko'
            },
            'body': 'Привет, мир!',
            'request': 'GET'
        }

        self.assertEqual(HttpServer.validate_params(settings)[0], False)

    def test_validate_params_negative_4(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'headers': {},
            'body': 'Привет, мир!',
            'request': 'GET'
        }

        self.assertEqual(HttpServer.validate_params(settings)[0], False)

    def test_validate_params_negative_5(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'headers': {},
            'body': 234,
            'request': 'GET'
        }

        self.assertEqual(HttpServer.validate_params(settings)[0], False)

    def test_validate_params_negative_6(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'headers': 23423,
            'body': '',
            'request': 'GET'
        }

        self.assertEqual(HttpServer.validate_params(settings)[0], False)

    def test_validate_params_negative_7(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'cookie': 1234,
            'headers': {},
            'body': '',
            'request': 'GET'
        }

        self.assertEqual(HttpServer.validate_params(settings)[0], False)

    def test_create_option_response(self):
        origin = '127.0.0.1'

        expected_result = "HTTP/1.1 200 OK\r\n" \
                          "Access-Control-Allow-Origin: 127.0.0.1\r\n" \
                          "Access-Control-Allow-Methods: POST, GET, OPTIONS\r\n" \
                          "Access-Control-Allow-Headers: Content-Type\r\n" \
                          "Connection: keep-alive\r\n" \
                          "Content-Length: 0\r\n" \
                          "\r\n"

        self.assertEqual(HttpServer.create_option_response(origin), expected_result)

    def test_create_response_with_body(self):
        code = 200
        code_message = 'OK'
        body = json.dumps({
            'message': 'все супер! ты молодец'
        })
        origin = '127.0.0.1'

        expected_result = 'HTTP/1.1 200 OK\r\n' \
                          'Content-Type: application/json\r\n' \
                          f'Content-Length: {len(body.encode())}\r\n' \
                          'Connection: keep-alive\r\n' \
                          'Access-Control-Allow-Origin: 127.0.0.1' \
                          '\r\n\r\n' + \
                          f'{body}'

        self.assertEqual(HttpServer.create_response(code, code_message, body, origin), expected_result)

    def test_create_response_without_body(self):
        code = 200
        code_message = 'OK'
        body = ''
        origin = '127.0.0.1'

        expected_result = 'HTTP/1.1 200 OK\r\n' \
                          'Content-Type: application/json\r\n' \
                          f'Content-Length: {len(body.encode())}\r\n' \
                          'Connection: keep-alive\r\n' \
                          'Access-Control-Allow-Origin: 127.0.0.1' \
                          '\r\n\r\n'

        self.assertEqual(HttpServer.create_response(code, code_message, body, origin), expected_result)

    def test_send_data(self):
        data = 'test send data'

        expected_result = len(data.encode())

        socket = MagicMock()
        socket.send.side_effect = [expected_result, 0]

        self.assertEqual(expected_result, HttpServer.send_data(socket, data))

    def test_create_ok_response(self):
        data = 'Hello, World!'
        origin = '127.0.0.1'

        body = dict()
        body['data'] = data
        body['code'] = 200

        body_json = json.dumps(body)

        expected_result = f'HTTP/1.1 200 OK\r\n' \
                          f'Content-Type: application/json\r\n' \
                          f'Content-Length: {len(body_json.encode())}\r\n' \
                          f'Connection: keep-alive\r\n' \
                          f'Access-Control-Allow-Origin: {origin}' \
                          f'\r\n\r\n{body_json}'

        self.assertEqual(expected_result, HttpServer.create_ok_request_response(data, origin))


if __name__ == '__main__':
    unittest.main()
