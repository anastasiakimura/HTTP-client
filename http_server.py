import re
import socket
import json

from enums.client_messages_response import ClientMessagesResponse
from enums.requests_names import RequestsNames
from enums.server_validating_messages import ServerValidatingMessages
from http_client import HttpClient


class HttpServer:
    """
    HTTP-сервер, который умеет принимать запросы от клиентов и, используя HttpClient возвращает нужные запросы
    """

    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 8080

        self._server = None

        self._working = None

    def start(self):
        """
        Запускает сервер
        """

        try:
            self._create_server()
        except OSError as e:
            self.stop()
            print(e)

        if self._server is None:
            return

        self._server.listen()

        self._start_server()

        while self._working:
            if self._server is None:
                break

            conn, addr = self._server.accept()

            print(f'Client connected by addr: {addr}')

            with conn:
                data = conn.recv(8192).decode()

                origin = None

                if data.startswith('OPTIONS / HTTP/1.1'):
                    origin = re.search(r'(?<=Origin: )(.+?)(?=\r\n)', data).group(0)

                    response = self.create_option_response(origin)

                    conn.sendall(response.encode())

                data = conn.recv(8190).decode()

                body = re.search(r'(?<=\r\n\r\n)(.+)', data).group(0)
                settings = json.loads(body)

                settings_is_validated = HttpServer.validate_params(settings)

                if not settings_is_validated[0]:
                    response = HttpServer.create_bad_request_response(
                        origin,
                        settings_is_validated[1]
                    )

                    HttpServer.send_data(conn, response)
                else:
                    client = HttpClient(settings)
                    client_data = client.get_data()

                    if client_data == ClientMessagesResponse.incorrect_url_or_port.value:
                        response = HttpServer.create_bad_request_response(origin, client_data)
                        HttpServer.send_data(conn, response)
                    else:
                        data = client_data

                        if (
                                settings.get('request').lower() == RequestsNames.get.value
                                and
                                len(settings.get('get_form')) != 0
                        ):
                            data = self._take_data(settings, client_data)

                        response = HttpServer.create_ok_request_response(data, origin)
                        HttpServer.send_data(conn, response)

            print(f'Client with addr {addr} was disconnected')

    def _stop_server(self):
        self._working = False

    def _start_server(self):
        self._working = True

    def stop(self):
        self._stop_server()

    @staticmethod
    def _take_data(settings: dict, client_data: str):
        data = client_data

        if 'application/json' in client_data:
            matches = re.finditer(settings.get('get_form'), client_data, re.IGNORECASE)
            data = [match.start() for match in matches]

        return data

    def _create_server(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind((self.__HOST, self.__PORT))

    def stop(self):
        self._server.close()
        self._server = None

    @staticmethod
    def send_data(conn: socket, response: str) -> int:
        """
        Отправляет данные на сервер
        :param conn: подключение, по которому нужно отправить эти данные
        :param response: отправляемые данные
        :return: количество отправленных байт
        """
        data_to_send = response.encode('utf-8')
        bytes_sent = 0

        while bytes_sent < len(data_to_send):
            sent = conn.send(data_to_send[bytes_sent:])

            bytes_sent += sent

        return bytes_sent

    @staticmethod
    def validate_params(body: dict) -> tuple:
        """
        Проверяет являются ли параметры запроса валидными
        :return: возвращает tuple, где первый параметр - это true или false: результат валидности,
        а второй сообщение описывающее результат валидации
        """

        if body.get('url') is None:
            return False, ServerValidatingMessages.incorrect_url.value

        if body.get('request') is None:
            return False, ServerValidatingMessages.incorrect_type_request.value

        if not isinstance(body.get('cookie'), dict):
            return False, ServerValidatingMessages.incorrect_format_cookie.value

        if not isinstance(body.get('headers'), dict):
            return False, ServerValidatingMessages.incorrect_format_headers.value

        if not isinstance(body.get('body'), str):
            return False, ServerValidatingMessages.incorrect_body_type.value

        return True, ServerValidatingMessages.is_validated.value

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
                   f'\r\n\r\n{data}'

        return response

    @staticmethod
    def create_ok_request_response(data: str, origin: str):
        """
        Создает ответ на запрос с кодом успеха
        :param data: данные, которые будут помещены в тело запроса
        :param origin: значение заголовка Origin в Option запросе клиента
        :return: возвращает готовый ответ для клиента в формате протокола HTTP
        """

        body = dict()

        body['data'] = data
        body['code'] = 200

        return HttpServer.create_response(body['code'], 'OK', json.dumps(body), origin)

    @staticmethod
    def create_bad_request_response(origin: str, message: str):
        """
        Создает ответ с кодом плохого запроса (bad request)
        :return:
        """

        body = dict()

        body['message'] = message
        body['code'] = 400

        return HttpServer.create_response(body['code'], 'BAD REQUEST', json.dumps(body), origin)
