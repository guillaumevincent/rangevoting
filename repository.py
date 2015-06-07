from rangevoting import RangeVote, Vote
import factories


class MongoRepository:
    def __init__(self, db):
        self.rangevotes = db['rangevote']

    def save(self, rangevote):
        self.rangevotes.insert(rangevote.serialize())

    def get(self, uid):
        element = self.rangevotes.find_one({"id": str(uid)})
        return factories.RangeVoteFactory().create_rangevote(element)

    def update(self, _id, new_rangevote):
        element = self.rangevotes.find_one({"id": str(_id)})
        self.rangevotes.update({'_id': element['_id']}, new_rangevote.serialize())

    def find(self, count=20):
        rangevote_factory = factories.RangeVoteFactory()
        elements = []
        for element in self.rangevotes.find()[:count]:
            elements.append(rangevote_factory.create_rangevote(element))
        return elements


class MockRepository:
    def __init__(self):
        self.db = {}

    def save(self, element):
        self.db[element.uuid] = element

    def update(self, uuid, element):
        self.db[uuid] = element

    def get(self, uuid):
        element = self.db[uuid]
        return factories.RangeVoteFactory().create_rangevote(element)

    def find(self, count=20):
        rangevote_factory = factories.RangeVoteFactory()
        elements = []
        for element in list(self.db.values())[:count]:
            elements.append(rangevote_factory.create_rangevote(element))
        return elements
