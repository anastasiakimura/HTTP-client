import socket

HOST = "www.google.ru"
PORT = 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(10)
    s.connect((HOST, PORT))
    request = b"GET / HTTP/1.1\r\nHost:www.google.ru\r\n\r\n"
    sent = 0
    while sent < len(request):
        sent = sent + s.send(request[sent:])
    response = b""
    try:
        while True:
            response = response + s.recv(4096)
    except socket.timeout as e:
        print("Time out!")
    s.send(b"GET / HTTP/1.1\r\nHost:www.google.ru\r\nConnection: close\r\n\r\n")
    print(response.decode('Windows-1251'))
