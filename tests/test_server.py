import socket

from threading import Thread


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

    def test(self):
        Thread(target=self.__run_server).start()
