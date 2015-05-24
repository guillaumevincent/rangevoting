from rangevoting import RangeVote, Vote


class MongoRepository:
    def __init__(self, db):
        self.rangevotes = db['rangevote']

    def save(self, rangevote):
        self.rangevotes.insert(rangevote.serialize())

    def get(self, uid):
        element = self.rangevotes.find_one({"id": str(uid)})
        rangevote = RangeVote(uuid=uid, question=element['question'], choices=element['choices'])
        rangevote.votes = [Vote(v['elector'], v['opinions']) for v in element['votes']]
        return rangevote

    def update(self, _id, new_rangevote):
        element = self.rangevotes.find_one({"id": str(_id)})
        self.rangevotes.update({'_id': element['_id']}, new_rangevote.serialize())


class MockRepository:
    def __init__(self):
        self.db = {}

    def save(self, element):
        self.db[element.uuid] = element

    def update(self, uuid, element):
        self.db[uuid] = element

    def get(self, uuid):
        return self.db[uuid]
