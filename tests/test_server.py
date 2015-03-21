import unittest

from server import Server


class ServerTestCase(unittest.TestCase):
    def test_server_respond_200_ok_on_index(self):
        serveur = Server()
        serveur.app.config['TESTING'] = True
        self.app = serveur.app.test_client()
        self.assertEqual(200, self.app.get('/').status_code)