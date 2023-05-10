import socket

from cli_flags.cli_flags import CLIFlags


class HttpClient:
    def __init__(self, settings: dict):
        self.__flags = CLIFlags()
        self.__settings = settings

        self.__HOST = self.__settings.get("url")
        self.__PORT = int(self.__settings.get("port"))

        self.requests_text = None

    def get_data(self) -> str:
        """
        Получаем и возвращаем данные, полученные по http запросу
        :return: декодированные данные в кодировке Windows-1251, полученные по http запросу
        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            timeout = 10

            if self.__settings.get("timeout") is not None:
                timeout = self.__settings.get("timeout")

            s.settimeout(timeout)
            s.connect((self.__HOST, self.__PORT))

            request = f'{self.__settings.get("request")} / HTTP/1.1\r\n'
            request += self.__get_headers(self.__settings)
            request += self.__settings.get("body")

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

            close_request = f'{self.__settings.get("request")} / HTTP/1.1\r\n'
            close_request += f'Host: {self.__settings.get("url")}\r\n'
            close_request += 'Connection: close\r\n\r\n'
            close_request = close_request.encode()

            try:
                s.sendall(close_request)
            except Exception as e:
                print('log: ' + str(e))

            response = response.decode()

            return response

    @staticmethod
    def __get_headers(settings: dict) -> str:
        """
        Формирует все заголовки для HTTP запроса
        :param settings: словарь, в котором должно быть поле '-h', которое является словарем
         и в нем хранятся все заголовки
        :return: - строчка со всеми заголовками в нужном формате
        """
        headers = list()

        for key, value in settings["headers"].items():
            headers.append(f'{key}: {value}\r\n')

        cookies = []

        for key, value in settings["cookie"].items():
            cookies.append(f'{key}={value};')

        if len(cookies) != 0:
            cookies = 'Cookie: ' + '  '.join(cookies)
            cookies = cookies[:-1]
            cookies += '\r\n'
            headers.append(cookies)

        headers_str = ''.join(headers)
        headers_str += '\r\n'

        return headers_str
