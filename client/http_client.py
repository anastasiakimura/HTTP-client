import socket


class HttpClient:
    def __init__(self, settings: dict):
        self.__settings = settings

        self.__HOST = self.__settings.get("url")
        self.__PORT = int(self.__settings.get("port"))

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

            request = self.create_http_request(self.__settings).encode()

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

            close_request = self.create_http_close_request(self.__settings).encode()

            try:
                s.sendall(close_request)
            except Exception as e:
                print('log: ' + str(e))

            response = response.decode()

            return response

    @staticmethod
    def get_headers(settings: dict) -> str:
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

        return headers_str

    @staticmethod
    def create_http_request(settings: dict) -> str:
        """
        Формирует HTTP запрос к серверу
        :param settings: настройки HTTP запроса
        :return: возвращает запрос в формате HTTP
        """
        return f'{settings.get("request")} / HTTP/1.1\r\n' + \
               HttpClient.get_headers(settings) + \
               '\r\n' + \
               settings.get("body")

    @staticmethod
    def create_http_close_request(settings: dict) -> str:
        """
        Формирует закрывающий HTTP запрос
        :param settings: настройки закрывающего запроса
        :return: возвращает запрос в формате HTTP
        """

        return f'{settings.get("request")} / HTTP/1.1\r\n' \
               f'Host: {settings.get("url")}\r\n' \
               f'Connection: close\r\n\r\n'
