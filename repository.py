class MongoRepository():
    def __init__(self, db):
        self.db = db

    def save(self, rangevote):
        rangevotes = self.db[type(rangevote).__name__.lower()]
        rangevotes.insert(rangevote.serialize())

    def get(self, type, id):
        rangevotes = self.db[type]
        return rangevotes.find_one({"id": str(id)})


class MockRepository():
    def __init__(self):
        self.saved_called = False

    def save(self, aggregate):
        self.saved_called = True