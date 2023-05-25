import enum


class ServerValidatingMessages(enum.Enum):
    incorrect_url = '�� �� ����� url-�����'
    incorrect_type_request = '�� �� ����� ��� �������'
    incorrect_format_cookie = '�������� ������ cookie: ������ �������� cookie ������ ���� ��������'
    incorrect_format_headers = '�������� ������ ����������: ������ �������� ��������� ������ ���� ��������'
    incorrect_body_type = '�������� ������ ���� �������: ������ �������� ���� ������� ������ ���� �������'
    is_validated = '��������� �������� ���������'
