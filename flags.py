class cli_flags:
    def __init__(self):
        self.__url = '-u'
        self.__port = '-p'
        self.__request = '-r'
        self.__headers = '-h'
        self.__cookie = '-c'
        self.__timeout = '-t'
        self.__save_in_file = '-sf'
        self.__body = '-b'
        self.__help = '-help'

        self.__accessed_flags = {
            self.__url, self.__port, self.__request, self.__headers, self.__cookie, self.__timeout, self.__save_in_file, self.__body,
            self.__help
        }
        self.__accessed_requests_values = {'GET', 'POST', 'DELETE', 'PATCH', 'PUT'}

    def get_accessed_flags(self):
        '''
        :return: возвращает множество всех разрешенных флагов
        '''
        return self.__accessed_flags

    def get_accessed_requests_values(self):
        '''
        :return: возвращает множество доступных значений для флага -r (Requests)
        '''
        return self.__accessed_requests_values

    def get_help_text(self):
        '''
        :return: возвращает актуальную доку для флага -help
        '''
        return '\n\n\tФлаги:\n' \
               f'\t  {self.__url} <url> - url, на который хотите отправить запрос (обязательный флаг)\n' \
               f'\t  {self.__port} <port> - порт (необязательный флаг)\n' \
               f'\t  {self.__request} <название запроса> - тип HTTP запроса, который хотите сделать (обязательный флаг)' \
               '\n' \
               f'\t  {self.__headers} <количество заголовков> <заголовок 1> <значение 1> <заголовок 2> <значение 2>' \
               ' ... - HTTP заголовки.' \
               '\n\t     В значении заголовка нужно вместо пробелов указывать нижние подчеркивания (_). Количество ' \
               'заголовков' \ 
               '\n\t     должно быть ровно столько, сколько указано в параметре <количество заголовков>\n' \
               f'\t  {self.__cookie} - если указать данный флаг, то в HTTP запросе вы указываете поддержку Cookie\n' \
               f'\t  {self.__timeout} <миллисекунды> - время, в течении которого мы будем ожидать ответ\n' \
               f'\t  {self.__save_in_file} <абсолютный путь до файла> - этот флаг подключает возможность сохранить ' \
               f'ответ файл\n' \ 
               f'\t  {self.__body} <количество слов в теле> <слово 1> <слово 2> ... - тело запроса\n\n'

    def get_url_flag(self):
        f'''
        :return: возвращает текстовый формат флага {self.__url}
        '''
        return self.__url

    def get_port_flag(self):
        '''
        :return: возвращает текстовый формат флага -u
        '''
        return self.__port

    def get_request_flag(self):
        '''
        :return: возвращает текстовый формат флага -r
        '''
        return self.__request

    def get_headers_flag(self):
        '''
        :return: возвращает текстовый формат флага -h
        '''
        return self.__headers

    def get_cookie_flag(self):
        '''
        :return: возвращает текстовый формат флага -c
        '''
        return self.__cookie

    def get_timeout_flag(self):
        '''
        :return: возвращает текстовый формат флага -t
        '''
        return self.__timeout

    def get_save_in_file_flag(self):
        '''
        :return: возвращает текстовый формат флага -sf
        '''
        return self.__save_in_file

    def get_body_flag(self):
        '''
        :return: возвращает текстовый формат флага -b
        '''
        return self.__body

    def get_help_flag(self):
        '''
        :return: возвращает текстовый формат флага -help
        '''
        return self.__help
