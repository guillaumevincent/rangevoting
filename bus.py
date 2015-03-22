class Bus():
    def __init__(self):
        self.handlers = {}

    def register(self, command, handler):
        self.handlers[command] = handler

    def send(self, command):
        command_type = type(command)
        if command_type not in self.handlers:
            raise (Exception('No handler for command ' + str(command_type) + ' found'))
        self.handlers[command_type].handle(command)