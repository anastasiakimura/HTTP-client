import unittest

from tests.test_server import TestServer


class Tests(unittest.TestCase):
    def test_client(self):
        server = TestServer()
        result = server.test()

        self.assertEqual(result[0], result[1])
