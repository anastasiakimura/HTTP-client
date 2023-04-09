import sys

from argv_parser import argv_parser
from http_client import http_client

if __name__ == '__main__':
    try:
        parser = argv_parser(sys.argv)
        client = http_client(parser.parse())
        print(client.get_data())
    except Exception as e:
        print('\nlog: ' + str(e) + '\n')
