import socket

from flags import cli_flags


class http_client:
    def __init__(self, settings: dict):
        self.__flags = cli_flags()
        self.__settings = settings

        self.HOST = self.__settings.get(self.__flags.get_url_flag())
        self.PORT = self.__settings.get(self.__flags.get_port_flag())

    def get_data(self) -> str:
        """
        Получаем и возвращаем данные, полученные по http запросу
        :return: декодированные данные в кодировке Windows-1251, полученные по http запросу
        """
        if self.__settings.get(self.__flags.get_help_flag()):
            return self.__flags.get_help_text()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)

            s.connect((self.HOST, self.PORT))

            request = self.type_request(self.__settings.get(self.__flags.get_request_flag()))
            request += self.get_headers(self.__settings)
            request += self.__settings.get(self.__flags.get_body_flag())
            request = bytes(request)

            sent = 0

            while sent < len(request):
                sent = sent + s.send(request[sent:])

            response = b""

            try:
                while True:
                    response = response + s.recv(4096)
            except socket.timeout as e:
                print(f"Time out! {e=}")

            request = self.type_request(self.__settings.get(self.__flags.get_request_flag()))
            request += f'Host: {self.__settings.get(self.__flags.get_url_flag())}\r\n'
            request += 'Connection: close\r\n\r\n'

            s.send(bytes(request))

            return response.decode('Windows-1251')

    def type_request(self, request: str) -> str:
        return f'{request} / HTTP/1.1\r\n'

    def get_headers(self, settings: dict) -> str:
        headers = list()

        for key, value in settings[self.__flags.get_headers_flag()].items():
            value = value.replace('_', ' ')
            headers.append(f'{key}: {value}\r\n')

        cookies = ['Cookie:']

        for key, value in settings[self.__flags.get_cookie_flag()].items():
            value = value.replace('_', ' ')
            headers.append(f'{key}={value};')

        cookies = ' '.join(cookies)
        cookies = cookies[:-1]
        cookies += '\r\n'

        headers.append(cookies)

        headers_str = ' '.join(headers)
        headers_str += '\r\n'

        return headers_str

