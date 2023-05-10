import unittest

from client.http_client import HttpClient
from test_server import TestServer


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

        self.assertEqual(client.requests_text, result)


if __name__ == '__main__':
    unittest.main()