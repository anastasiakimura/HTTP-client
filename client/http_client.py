import socket

from cli_flags.cli_flags import CLIFlags


class HttpClient:
    def __init__(self, settings: dict):
        self.__flags = CLIFlags()
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
            timeout = 10

            try:
                if self.__settings.get(self.__flags.get_timeout_flag()) is not None:
                    timeout = int(self.__settings.get(self.__flags.get_timeout_flag()))
            except Exception as e:
                timeout = 10

            s.settimeout(timeout)
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

            response = response.decode()

            if self.__settings.get((self.__flags.get_save_in_file_flag())) is not None:
                print(self.__save_in_file(response, self.__settings.get((self.__flags.get_save_in_file_flag()))))

            return response

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

    def __save_in_file(self, text: str, file_path: str) -> bool:
        try:
            with open(file_path, 'w') as file:
                file.write(text)
                return True
        except Exception as e:
            return False
