import socket

from cli_parser.flags import cli_flags


class HttpClient:
    def __init__(self, settings: dict):
        self.__flags = cli_flags()
        self.__settings = settings

        self.__HOST = self.__settings.get(self.__flags.get_url_flag())
        self.__PORT = self.__settings.get(self.__flags.get_port_flag())

        self.requests_text = None

    def get_data(self) -> str:
        """
        Получаем и возвращаем данные, полученные по http запросу
        :return: декодированные данные в кодировке Windows-1251, полученные по http запросу
        """
        if self.__settings.get(self.__flags.get_help_flag()):
            return self.__flags.get_help_text()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect((self.__HOST, self.__PORT))

            request = f'{self.__settings.get(self.__flags.get_request_flag())} / HTTP/1.1\r\n'
            request += self.__get_headers(self.__settings)
            request += self.__settings.get(self.__flags.get_body_flag())

            self.requests_text = request

            request = request.encode()

            try:
                s.sendall(request)
            except Exception as e:
                print('log: ' + str(e))

            response = b""

            try:
                while True:
                    data = s.recv(4096)

                    if not data:
                        break

                    response += data
            except socket.timeout:
                pass
            except Exception as e:
                print('log: ' + str(e))

            close_request = f'{self.__settings.get(self.__flags.get_request_flag())} / HTTP/1.1\r\n'
            close_request += f'Host: {self.__settings.get(self.__flags.get_url_flag())}\r\n'
            close_request += 'Connection: close\r\n\r\n'
            close_request = close_request.encode()

            try:
                s.sendall(close_request)
            except Exception as e:
                print('log: ' + str(e))

            return response.decode()

    def __get_headers(self, settings: dict) -> str:
        """
        Формирует все заголовки для HTTP запроса
        :param settings: словарь, в котором должно быть поле '-h', которое является словарем
         и в нем хранятся все заголовки
        :return: - строчка со всеми заголовками в нужном формате
        """
        headers = list()

        for key, value in settings[self.__flags.get_headers_flag()].items():
            value = value.replace('_', ' ')
            headers.append(f'{key}: {value}\r\n')

        cookies = []

        for key, value in settings[self.__flags.get_cookie_flag()].items():
            value = value.replace('_', ' ')
            cookies.append(f'{key}={value};')

        if len(cookies) != 0:
            cookies = 'Cookie: ' + '  '.join(cookies)
            cookies = cookies[:-1]
            cookies += '\r\n'
            headers.append(cookies)

        headers_str = ''.join(headers)
        headers_str += '\r\n'

        return headers_str

