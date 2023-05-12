import re
import socket
import json

from client.http_client import HttpClient


class HttpServer:
    """
    HTTP-сервер, который умеет принимать запросы от клиентов и, используя HttpClient возвращает нужные запросы
    """

    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 8080

    def start(self):
        """
        Запускает сервер
        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__HOST, self.__PORT))
            s.listen()

            while True:
                conn, addr = s.accept()

                print(f'Client connected by addr: {addr}')

                with conn:
                    data = conn.recv(8190).decode()
                    origin = None

                    if data.startswith('OPTIONS / HTTP/1.1'):
                        origin = re.search(r'(?<=Origin: )(.+?)(?=\r\n)', data).group(0)

                        response = self.create_option_response(origin)

                        conn.sendall(response.encode())

                    data = conn.recv(8190).decode()

                    body = re.search(r'(?<=\r\n\r\n)(.+)', data).group(0)
                    settings = json.loads(body)

                    if not HttpServer.validate_body(settings):
                        response = HttpServer.create_bad_request_response(
                            origin,
                            'Вы не ввели либо url, либо тип запроса'
                        )
                        conn.sendall(response.encode())
                    else:
                        client = HttpClient(settings)
                        client_data = client.get_data()

                        response = HttpServer.create_ok_request_response(client_data, origin)
                        conn.sendall(response.encode())

                print(f'Client with addr {addr} was disconnected')

    @staticmethod
    def validate_body(body: dict):
        """
        Проверяет является ли тело запроса валидным
        :return: возвращает либо True, либо False
        """

        if \
                body.get('url') is None or \
                body.get('request') is None or \
                type(body.get('cookie')) != dict or \
                type(body.get('headers')) != dict or \
                type(body.get('body')) != str:
            return False

        return True

    @staticmethod
    def create_option_response(origin: str):
        """
        Создает ответ на OPTION запрос клиента
        :param origin: значение заголовка Origin в Option запросе клиента
        :return: возвращает готовый ответ для клиента в формате протокола HTTP
        """

        return f"HTTP/1.1 200 OK\r\n" \
               f"Access-Control-Allow-Origin: {origin}\r\n" \
               f"Access-Control-Allow-Methods: POST, GET, OPTIONS\r\n" \
               f"Access-Control-Allow-Headers: Content-Type\r\n" \
               f"Connection: keep-alive\r\n" \
               f"Content-Length: 0\r\n" \
               f"\r\n"

    @staticmethod
    def create_response(code: int, code_message: str, data: str, origin: str,):
        """
        Создает ответ на пользовательский запрос
        :param code: код ответа
        :param code_message: код ответа
        :param data: данные в теле ответа (должны быть в json формате)
        :param origin: значение заголовка Origin в Option запросе клиента
        :return: ответ
        """

        response = f'HTTP/1.1 {code} {code_message}\r\n' \
                   f'Content-Type: application/json\r\n' \
                   f'Content-Length: {len(data.encode())}\r\n' \
                   f'Connection: keep-alive\r\n' \
                   f'Access-Control-Allow-Origin: {origin}' \
                   f'\r\n\r\n'

        if len(data) != 0:
            response += json.dumps({
                'data': data
            })

        return response

    @staticmethod
    def create_ok_request_response(data: str, origin: str):
        """
        Создает ответ на запрос с кодом успеха
        :param data: данные, которые будут помещены в тело запроса
        :param origin: значение заголовка Origin в Option запросе клиента
        :return: возвращает готовый ответ для клиента в формате протокола HTTP
        """

        return HttpServer.create_response(200, 'OK', data, origin)

    @staticmethod
    def create_bad_request_response(origin: str, message: str):
        """
        Создает ответ с кодом плохого запроса (bad request)
        :return:
        """

        body = dict()

        body['message'] = message

        return HttpServer.create_response(400, "BAD REQUEST", json.dumps(body), origin)
