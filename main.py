import socket

HOST = "www.google.ru"  # The server's hostname or IP address
PORT = 80  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(10)
    s.connect((HOST, PORT))
    request = b"GET / HTTP/1.1\r\nHost:www.google.ru\r\n\r\n"
    sent = 0
    while sent < len(request):
        sent = sent + s.send(request[sent:])  # Send a portion of 'request', starting from 'sent' byte
    response = b""
    try:
        while True:
            test_recv = s.recv(4096)
            if len(test_recv) == 0:
                break
            response = response + test_recv
    except socket.timeout as e:
        print("Time out!")
    s.send(b"GET / HTTP/1.1\r\nHost:www.google.ru\r\nConnection: close\r\n\r\n")