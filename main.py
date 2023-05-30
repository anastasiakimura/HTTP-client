from http_server import HttpServer


class Main:
    def __init__(self):
        self._server = HttpServer()

    def run(self):
        self._server.start()

    def finish(self):
        self._server.stop()


if __name__ == '__main__':
    Main().run()
