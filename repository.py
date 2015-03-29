class MongoRepository():
    def __init__(self, db):
        self.db = db

    def save(self, rangevote):
        rangevotes = self.db[type(rangevote).__name__.lower()]
        rangevotes.insert(rangevote.serialize())


class MockRepository():
    def __init__(self):
        self.saved_called = False

    def save(self, aggregate):
        self.saved_called = True