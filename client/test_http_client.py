import unittest
from mock import patch

from client.HttpClient import HttpClient


class MyTestCase(unittest.TestCase):
    def test_get_data(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
