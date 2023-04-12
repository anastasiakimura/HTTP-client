import socket

from threading import Thread

from client.http_client import HttpClient


class TestServer:
    def __init__(self):
        super().__init__()
        self.__HOST = '127.0.0.1'
        self.__PORT = 4444

    def __run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15)
            s.bind((self.__HOST, self.__PORT))

            s.listen()

            conn, addr = s.accept()

            with conn:
                try:
                    while True:
                        data = conn.recv(4096)

                        if not data:
                            break

                        conn.sendall(data)
                except Exception as e:
                    print('log: ' + str(e))

    def __run_client(self) -> tuple:
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

        result = (client.get_data(), client.request)

        return result

    def test(self):
        Thread(target=self.__run_server).start()

        return self.__run_client()
