import re
import socket
import json

from client.http_client import HttpClient


def server():
    host = '127.0.0.1'
    port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        conn, addr = s.accept()
        with conn:

            data = conn.recv(8190).decode()
            origin = None

            if data.startswith('OPTIONS / HTTP/1.1'):
                origin = re.search(r'(?<=Origin: )(.+?)(?=\r\n)', data).group(0)

                response = "HTTP/1.1 200 OK\r\n"
                response += f"Access-Control-Allow-Origin: {origin}\r\n"
                response += "Access-Control-Allow-Methods: POST, GET, OPTIONS\r\n"
                response += "Access-Control-Allow-Headers: Content-Type\r\n"
                response += "Connection: keep-alive\r\n"
                response += "Content-Length: 0\r\n"
                response += "\r\n"

                conn.sendall(response.encode())

            data = conn.recv(8190).decode()
            print(data)

            body = re.search(r'(?<=\r\n\r\n)(.+)', data).group(0)
            settings = json.loads(body)
            client = HttpClient(settings)
            client_data = client.get_data()
            response = f'HTTP/1.1 200 OK\r\n' \
                       f'Content-Type: application/json\r\n' \
                       f'Content-Length: {len(client_data.encode())}\r\n' \
                       f'Connection: keep-alive\r\n' \
                       f'Content-Encoding: gzip\r\n' \
                       f'Access-Control-Allow-Origin: {origin}' \
                       f'\r\n'
            response+= json.dumps(client_data)

            conn.sendall(response.encode())
