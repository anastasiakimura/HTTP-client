import sys

from client.http_client import HttpClient
from parser.argv_parser import ArgvParser

if __name__ == '__main__':
    try:
        parser = ArgvParser(sys.argv)
        client = HttpClient(parser.parse())
        print(client.get_data())
    except Exception as e:
        print('\nlog: ' + str(e) + '\n')
