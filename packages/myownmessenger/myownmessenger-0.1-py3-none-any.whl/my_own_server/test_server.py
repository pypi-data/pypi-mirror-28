import time
import json
import socket
from server import Handler


class TestHandler:
    def setup(self):
        self.s = Handler()

    def test_presence_response(self):
        # Нет ключа action
        assert self.s.presence_response({'one': 'two', 'time': time.time()})['response'] == 400
        # Нет ключа time
        assert self.s.presence_response({'action': 'presence'})['response'] == 400
        # Ключ не presence
        assert self.s.presence_response({'action': 'test_action', 'time': 1000.10})['response'] == 400
        # Кривое время
        assert self.s.presence_response({'action': 'presence', 'time': 'test_time'})['response'] == 400
        # Всё ок
        assert self.s.presence_response({'action': 'presence', 'time': 1000.10, 'account_name': 'leo'}) == {
            'response': 200}

    def test_read_requests(self, monkeypatch):
        monkeypatch.setattr("socket.socket", ClientSocket)
        r_clients = [socket.socket(), socket.socket()]
        all_clients = [socket.socket(), socket.socket(), socket.socket()]
        result = [
            {'test': 'test_message'},
            {'test': 'test_message'}
        ]
        print(self.s.read_requests(r_clients, all_clients))
        print(result)
        assert self.s.read_requests(r_clients, all_clients) == result


# ИНТЕГРАЦИОННЫЕ ТЕСТЫ
# Класс заглушка для сокета
class ClientSocket():
    """Класс-заглушка для операций с сокетом"""

    def __init__(self, sock_type=socket.AF_INET, sock_family=socket.SOCK_STREAM):
        pass

    def recv(self, n):
        message = {"test": "test_message"}
        jmessage = json.dumps(message)
        bmessage = jmessage.encode()
        return bmessage
