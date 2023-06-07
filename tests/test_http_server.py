import json
import re
import socket
import unittest
from unittest.mock import MagicMock

from enums.server_validating_messages import ServerValidatingMessages
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
            'body': None,
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
        socket.send.side_effect = [expected_result]

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

    def test_create_bad_response(self):
        message = 'Hello, World!'
        origin = '127.0.0.1'

        body = dict()
        body['message'] = message
        body['code'] = 400

        body_json = json.dumps(body)

        expected_result = f'HTTP/1.1 400 BAD REQUEST\r\n' \
                          f'Content-Type: application/json\r\n' \
                          f'Content-Length: {len(body_json.encode())}\r\n' \
                          f'Connection: keep-alive\r\n' \
                          f'Access-Control-Allow-Origin: {origin}' \
                          f'\r\n\r\n{body_json}'

        self.assertEqual(expected_result, HttpServer.create_bad_request_response(origin, message))

    def test_take_data(self):
        client_data = 'Content-Type: application/json\r\n{"data": "test test test"}'
        settings = {'get_form': 'test'}

        matches = re.finditer(settings.get('get_form'), client_data, re.IGNORECASE)
        expected_result = [match.start() for match in matches]

        self.assertEqual(expected_result, HttpServer._take_data(settings, client_data))

    def test_start_working(self):
        server = HttpServer()

        server._start_server()

        self.assertEqual(True, server._working)

    def test_stop_working(self):
        server = HttpServer()

        server._start_server()
        server._stop_server()

        self.assertEqual(False, server._working)
