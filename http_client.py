import socket

from flags import cli_flags


class http_client:
    def __init__(self, settings: dict):
        self.__flags = cli_flags()
        self.__settings = settings

        self.HOST = self.__settings.get(self.__flags.get_url_flag())
        self.PORT = self.__settings.get(self.__flags.get_port_flag())

    def get_data(self) -> str:
        if self.__settings.get(self.__flags.get_help_flag()):
            return self.__flags.get_help_text()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)

            s.connect((self.HOST, self.PORT))

            request = b"GET / HTTP/1.1\r\nHost:www.google.ru\r\n\r\n"

            sent = 0

            while sent < len(request):
                sent = sent + s.send(request[sent:])

            response = b""

            try:
                while True:
                    response = response + s.recv(4096)
            except socket.timeout as e:
                print(f"Time out! {e=}")

            s.send(b"GET / HTTP/1.1\r\nHost:www.google.ru\r\nConnection: close\r\n\r\n")

            return response.decode('Windows-1251')
