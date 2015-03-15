import unittest

from flask import Flask


class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.app.add_url_rule('/', 'index', self.index)

    @staticmethod
    def index():
        return "Hello World!"


class ServerTestCase(unittest.TestCase):
    def test_server_respond_200_ok_on_index(self):
        serveur = Server()
        serveur.app.config['TESTING'] = True
        self.app = serveur.app.test_client()
        self.assertEqual(200, self.app.get('/').status_code)


if __name__ == '__main__':
    unittest.main()
