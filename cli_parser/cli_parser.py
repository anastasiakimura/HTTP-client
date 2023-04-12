from cli_flags.cli_flags import CLIFlags


class CLIParser:
    def __init__(self, argv: list):
        argv.pop(0)

        self.__argv = argv
        self.__key = None

        self.__flags = CLIFlags()

        self.__url = False
        self.__port = 80
        self.__request = False
        self.__count_headers = 0
        self.__count_words_of_body = 0
        self.__count_cookies = 0

    def __validate(self, settings: dict) -> None:
        '''
        Внутренний метод, который проверяет, соответствует ли состояние словаря с настройками действительным параметрам
        :param settings: словарь с настройками
        :return: None
        '''

        if (self.__count_words_of_body != 0) & (
                settings[self.__flags.get_headers_flag()].get('Content-Length') is None):
            raise Exception(
                'Вы не указали заголовок Content-Length! \n'
                f'Для того, чтобы посмотреть справку'
                f' вызовите эту утилиту с флагом {self.__flags.get_help_flag()}'
            )

        if not self.__url:
            raise Exception(
                'Вы не указали url!\n'
                f'Для того, чтобы посмотреть справку'
                f' вызовите эту утилиту с флагом {self.__flags.get_help_flag()}'
            )

        if (self.__url is not None) & (settings.get(self.__flags.get_headers_flag()).get('Host') is None):
            raise Exception('Вы указали на какой url слать запрос, но не указали его в заголовках (заголовок "Host")\n')

        if not self.__request:
            raise Exception(
                'Вы не указали тип запроса!\n'
                f'Для того, чтобы посмотреть справку'
                f' вызовите эту утилиту с флагом {self.__flags.get_help_flag()}'
            )

        for key in settings.keys():
            if key not in self.__flags.get_accessed_flags():
                raise Exception(
                    'Вы указали не существующий флаг!\n'
                    f'Для того, чтобы посмотреть справку'
                    f' вызовите эту утилиту с флагом {self.__flags.get_help_flag()}'
                )

        if settings.get(self.__flags.get_request_flag()) not in self.__flags.get_accessed_requests_values():
            raise Exception(
                'Вы указали некорректное значение запроса!\n'
                f'Для того, чтобы посмотреть справку'
                f' вызовите эту утилиту с флагом {self.__flags.get_help_flag()}'
            )

    def __set_headers(self, settings: dict, index: int) -> int:
        '''
        Внутренний метод, который добавляет все заголовки в словарь с настройками запроса
        :param settings: словарь с настройками
        :param index: текущий индекс в массиве-параметров, на котором мы получили количество заголовков
        :return: новый индекс, на котором мы закончили получать заголовки
        '''
        j = index + 1

        while j <= (index + 2 * self.__count_headers):
            header = self.__argv[j]

            settings[self.__flags.get_headers_flag()][header] = self.__argv[j + 1]

            j += 2

        self.__key = None
        return j

    def __set_cookies(self, settings: dict, index: int) -> int:
        '''
        Внутренний метод, который добавляет все cookie в словарь с настройками запроса
        :param settings: словарь с настройками
        :param index: текущий индекс в массиве-параметров, на котором мы получили количество cookie
        :return: новый индекс, на котором мы закончили получать cookie
        '''
        j = index + 1

        while j <= (index + 2 * self.__count_cookies):
            cookie = self.__argv[j]

            settings[self.__flags.get_cookie_flag()][cookie] = self.__argv[j + 1]

            j += 2

        self.__key = None
        return j


    def __set_body(self, settings: dict, index: int) -> int:
        '''
        Внутренний метод, который добавляет все слова тела запроса в массив в словаре с настройками
        :param settings: словарь с настройками
        :param index: текущий индекс в массиве-параметров, на котором мы получили количество слов в теле запроса
        :return: новый индекс, на котором мы закончили получать слова для тела запроса
        '''
        j = index + 1

        while j <= (index + self.__count_words_of_body):
            word = self.__argv[j]

            settings[self.__flags.get_body_flag()].append(word)

            j += 1

        self.__key = None
        return j

    def parse(self) -> dict:
        '''
        Этот метод парсит массив параметров, переданный в параметре конструктора
        :return: возвращает словарь с настройками, который удалось вытащить из массива параметров
        '''
        settings = dict()

        if (len(self.__argv) == 1) & (self.__argv[0] == self.__flags.get_help_flag()):
            settings[self.__flags.get_help_flag()] = True

            return settings

        settings[self.__flags.get_help_flag()] = False
        settings[self.__flags.get_cookie_flag()] = False
        settings[self.__flags.get_headers_flag()] = dict()
        settings[self.__flags.get_cookie_flag()] = dict()
        settings[self.__flags.get_body_flag()] = []

        index = 0

        while index < len(self.__argv):
            item = self.__argv[index]

            if self.__key is None:
                index += 1
                self.__key = item
                continue

            if self.__key == self.__flags.get_url_flag():
                self.__url = True

            if self.__key == self.__flags.get_request_flag():
                self.__request = True

            if self.__key == self.__flags.get_headers_flag():
                self.__count_headers = int(item)
                index = self.__set_headers(settings, index)
                continue

            if self.__key == self.__flags.get_cookie_flag():
                self.__count_cookies = int(item)
                index = self.__set_cookies(settings, index)
                continue

            if self.__key == self.__flags.get_body_flag():
                self.__count_words_of_body = int(item)
                index = self.__set_body(settings, index)
                continue

            settings[self.__key] = item
            self.__key = None

            index += 1

        if settings.get(self.__flags.get_port_flag()) is None:
            settings[self.__flags.get_port_flag()] = self.__port
        else:
            settings[self.__flags.get_port_flag()] = int(settings.get(self.__flags.get_port_flag()))

        settings[self.__flags.get_body_flag()] = ' '.join(settings[self.__flags.get_body_flag()])

        self.__validate(settings)

        return settings