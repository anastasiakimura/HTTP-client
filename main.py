import sys

from cli_parser.cli_parser import CLIParser
from client.http_client import HttpClient

if __name__ == '__main__':
    try:
        parser = CLIParser(sys.argv)
        client = HttpClient(parser.parse())
        print(client.get_data())
    except Exception as e:
        print('\nlog: ' + str(e) + '\n')
