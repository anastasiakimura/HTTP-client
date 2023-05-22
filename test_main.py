import json
import unittest

from http_client import HttpClient
from server import HttpServer
from testing_server import TestServer


# ToDo: сделать тесты ещё для методов класса HttpClient: create_http_request, create_http_close_request и get_headers
# ToDo: а также сделать тесты для класса HttpServer: create_option_response и create_response

class Tests(unittest.TestCase):
    def test_client(self):
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

        client = HttpClient(settings)
        TestServer().test()

        result = client.get_data()

        self.assertEqual(HttpClient.create_http_request(settings), result)

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

    def test_validate_body_positive(self):
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

        self.assertEqual(HttpServer.validate_body(settings), True)

    def test_validate_body_negative_1(self):
        settings = {
            'port': 4444,
            'cookie': {
                'name': 'ilya',
                'surname': 'fomko'
            },
            'body': 'Привет, мир!',
            'request': 'GET'
        }

        self.assertEqual(HttpServer.validate_body(settings), False)

    def test_validate_body_negative_2(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'cookie': {
                'name': 'ilya',
                'surname': 'fomko'
            },
            'body': 'Привет, мир!',
        }

        self.assertEqual(HttpServer.validate_body(settings), False)

    def test_validate_body_negative_3(self):
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

        self.assertEqual(HttpServer.validate_body(settings), False)

    def test_validate_body_negative_4(self):
        settings = {
            'url': '127.0.0.1',
            'port': 4444,
            'headers': {},
            'body': 'Привет, мир!',
            'request': 'GET'
        }

        self.assertEqual(HttpServer.validate_body(settings), False)

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


if __name__ == '__main__':
    unittest.main()
