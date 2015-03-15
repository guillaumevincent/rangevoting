from flask import Flask


class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.app.add_url_rule('/', 'index', self.index)

    @staticmethod
    def index():
        return "Hello World!"