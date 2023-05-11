import unittest

from client.http_client import HttpClient
from test_server import TestServer


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


if __name__ == '__main__':
    unittest.main()
