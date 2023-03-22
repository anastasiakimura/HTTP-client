from client import HttpClient

if __name__ == '__main__':
    client = HttpClient("www.google.ru", 80)

    print(client.get_data())
