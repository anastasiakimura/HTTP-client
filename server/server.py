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

                        response = self.__create_option_response(origin)

                        conn.sendall(response.encode())

                    data = conn.recv(8190).decode()

                    body = re.search(r'(?<=\r\n\r\n)(.+)', data).group(0)
                    settings = json.loads(body)

                    client = HttpClient(settings)

                    client_data = client.get_data()

                    response = self.__create_response(client_data, origin)
                    conn.sendall(response.encode())

                print(f'Client with addr {addr} was disconnected')

    @staticmethod
    def __create_option_response(origin: str):
        """
        Создает ответ на OPTION запрос клиента
        :param origin: значение заголовка Origin в Option запросе клиента
        :return: возвращает готовый ответ для клиента в формате протокола HTTP
        """

        response = "HTTP/1.1 200 OK\r\n"
        response += f"Access-Control-Allow-Origin: {origin}\r\n"
        response += "Access-Control-Allow-Methods: POST, GET, OPTIONS\r\n"
        response += "Access-Control-Allow-Headers: Content-Type\r\n"
        response += "Connection: keep-alive\r\n"
        response += "Content-Length: 0\r\n"
        response += "\r\n"

        return response

    @staticmethod
    def __create_response(data: str, origin: str):
        """
        Создает ответ на запрос
        :param data: данные, которые будут помещены в тело запроса
        :param origin: значение заголовка Origin в Option запросе клиента
        :return: возвращает готовый ответ для клиента в формате протокола HTTP
        """

        response = f'HTTP/1.1 200 OK\r\n' \
                   f'Content-Type: application/json\r\n' \
                   f'Content-Length: {len(data.encode())}\r\n' \
                   f'Connection: keep-alive\r\n' \
                   f'Access-Control-Allow-Origin: {origin}' \
                   f'\r\n\r\n'

        response += json.dumps({
            'data': data
        })

        return response
