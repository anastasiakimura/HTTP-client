import enum


class ServerValidatingMessages(enum.Enum):
    incorrect_url = 'You did not write URL-address'
    incorrect_type_request = 'You did not write type of request'
    incorrect_format_cookie = 'Incorrect format cookie: type of object which takes cookie must be dictionary'
    incorrect_format_headers = 'Incorrect format headers: type of object which takes headers must be dictionary'
    incorrect_body_type = 'Incorrect format of body: type of object which takes body is string'
    is_validated = 'All parameters is valid'
