import unittest

from cli_flags.flags import CLIFlags
from cli_parser.cli_parser import CLIParser
from client.http_client import HttpClient
from test_server import TestServer


class Tests(unittest.TestCase):
    def test_client(self):
        settings = {
            '-u': '127.0.0.1',
            '-p': 4444,
            '-c': {
                'name': 'ilya',
                'surname': 'fomko'
            },
            '-h': {
                'Host': '127.0.0.1'
            },
            '-b': 'Привет, мир!',
            '-help': False,
            '-r': 'GET'
        }

        client = HttpClient(settings)
        TestServer().test()

        result = client.get_data()

        self.assertEqual(client.requests_text, result)

    def test_parser_for_base(self):
        argv = 'main.py -u 127.0.0.1 -p 4444 -h 1 Host 127.0.0.1 -r GET'.split()

        argv_parser = CLIParser(argv)

        actual_result = argv_parser.parse()

        expected_result = {
            '-u': '127.0.0.1',
            '-p': 4444,
            '-c': dict(),
            '-h': {
                'Host': '127.0.0.1'
            },
            '-help': False,
            '-r': 'GET',
            '-b': ''
        }

        self.assertDictEqual(expected_result, actual_result)

    def test_parser_for_help(self):
        argv_parser = CLIParser(['main.py', '-help'])

        actual_result = argv_parser.parse()

        expected_result = {
            '-help': True
        }

        self.assertDictEqual(expected_result, actual_result)

    def test_parser_with_lot_headers(self):
        argv = 'main.py -u 127.0.0.1 -p 4444 -h 3 Host 127.0.0.1 ' \
               'Connection keep-alive Content-Length 13 -r GET -b 2 Hello, World!'.split(' ')

        argv_parser = CLIParser(argv)

        actual_result = argv_parser.parse()
        expected_result = {
            '-u': '127.0.0.1',
            '-p': 4444,
            '-c': dict(),
            '-h': {
                'Host': '127.0.0.1',
                'Content-Length': '13',
                'Connection': 'keep-alive'
            },
            '-b': 'Hello, World!',
            '-help': False,
            '-r': 'GET'
        }

        self.assertDictEqual(expected_result, actual_result)

    def test_parser_with_lot_cookies(self):
        argv = 'main.py -u 127.0.0.1 -p 4444 -h 3 Host 127.0.0.1 ' \
               'Connection keep-alive Content-Length 13 -r GET -b 2 Hello, World! -c 2 name petr surname petrov'.split(
            ' ')

        argv_parser = CLIParser(argv)

        actual_result = argv_parser.parse()
        expected_result = {
            '-u': '127.0.0.1',
            '-p': 4444,
            '-c': {
                'name': 'petr',
                'surname': 'petrov'
            },
            '-h': {
                'Host': '127.0.0.1',
                'Content-Length': '13',
                'Connection': 'keep-alive'
            },
            '-b': 'Hello, World!',
            '-help': False,
            '-r': 'GET'
        }

        self.assertDictEqual(expected_result, actual_result)

    def test_parser_with_timeout(self):
        argv = 'main.py -u 127.0.0.1 -p 4444 -h 1 Host 127.0.0.1 -r GET -t 15'.split()

        argv_parser = CLIParser(argv)

        actual_result = argv_parser.parse()

        expected_result = {
            '-u': '127.0.0.1',
            '-p': 4444,
            '-c': dict(),
            '-h': {
                'Host': '127.0.0.1'
            },
            '-help': False,
            '-r': 'GET',
            '-b': '',
            '-t': '15'
        }

        self.assertDictEqual(expected_result, actual_result)

    def test_parser_with_save_in_file(self):
        argv = 'main.py -u 127.0.0.1 -p 4444 -h 1 Host 127.0.0.1 -r GET' \
               ' -t 15 -sf C:\\Users\\Iluha\\Documents\\HTTP-client\\input.txt'.split()

        argv_parser = CLIParser(argv)

        actual_result = argv_parser.parse()

        expected_result = {
            '-u': '127.0.0.1',
            '-p': 4444,
            '-c': dict(),
            '-h': {
                'Host': '127.0.0.1'
            },
            '-help': False,
            '-r': 'GET',
            '-b': '',
            '-t': '15',
            '-sf': 'C:\\Users\\Iluha\\Documents\\HTTP-client\\input.txt'
        }

        self.assertDictEqual(expected_result, actual_result)

    def test_parser_with_body_exception(self):
        argv = 'main.py -u 127.0.0.1 -p 4444 -h 1 Host 127.0.0.1 -r GET -b 2 Hello, World!'.split(' ')

        argv_parser = CLIParser(argv)
        flags = CLIFlags()

        msg = 'Вы не указали заголовок Content-Length! \n' \
              f'Для того, чтобы посмотреть справку' \
              f' вызовите эту утилиту с флагом {flags.get_help_flag()}'

        with self.assertRaises(Exception, msg=msg):
            argv_parser.parse()

    def test_parser_with_no_header_host(self):
        argv = 'main.py -u 127.0.0.1 -p 4444 -r GET!'.split(' ')

        argv_parser = CLIParser(argv)

        msg = 'Вы указали на какой url слать запрос, но не указали его в заголовках (заголовок "Host")\n'

        with self.assertRaises(Exception, msg=msg):
            argv_parser.parse()

    def test_parser_with_no_requests(self):
        argv = 'main.py -u 127.0.0.1 -h 1 Host 127.0.0.1 -p 4444!'.split(' ')

        argv_parser = CLIParser(argv)
        flags = CLIFlags()

        msg = 'Вы не указали тип запроса!\n' \
              f'Для того, чтобы посмотреть справку' \
              f' вызовите эту утилиту с флагом {flags.get_help_flag()}'

        with self.assertRaises(Exception, msg=msg):
            argv_parser.parse()

    def test_parser_not_exists_flag(self):
        argv = 'main.py -u 127.0.0.1 -h 1 Host 127.0.0.1 -p 4444 -r GET -sdfs dsdf!'.split(' ')

        argv_parser = CLIParser(argv)
        flags = CLIFlags()

        msg = 'Вы указали не существующий флаг!\n' \
              f'Для того, чтобы посмотреть справку' \
              f' вызовите эту утилиту с флагом {flags.get_help_flag()}'

        with self.assertRaises(Exception, msg=msg):
            argv_parser.parse()

    def test_parser_not_exists_request_value(self):
        argv = 'main.py -u 127.0.0.1 -h 1 Host 127.0.0.1 -p 4444 -r sdf'.split(' ')

        argv_parser = CLIParser(argv)
        flags = CLIFlags()

        msg = 'Вы указали некорректное значение запроса!\n' \
              f'Для того, чтобы посмотреть справку' \
              f' вызовите эту утилиту с флагом {flags.get_help_flag()}'

        with self.assertRaises(Exception, msg=msg):
            argv_parser.parse()


if __name__ == '__main__':
    unittest.main()