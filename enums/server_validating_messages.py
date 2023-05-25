import enum


class ServerValidatingMessages(enum.Enum):
    incorrect_url = 'Вы не ввели url-адрес'
    incorrect_type_request = 'Вы не ввели тип запроса'
    incorrect_format_cookie = 'Неверный формат cookie: объект хранящий cookie должен быть словарем'
    incorrect_format_headers = 'Неверный формат заголовков: объект хранящий заголовки должен быть словарем'
    incorrect_body_type = 'Неверный формат тела запроса: объект хранящий тело запроса должен быть строкой'
    is_validated = 'Параметры являются валидными'
