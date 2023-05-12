
from server.server import HttpServer

if __name__ == '__main__':
    print(type(dict()) == dict)
    server = HttpServer()
    server.start()

