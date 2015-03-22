class MockRepository():
    def __init__(self):
        self.saved_called = False

    def save(self, aggregate):
        self.saved_called = True