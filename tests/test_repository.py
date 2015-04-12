import unittest
import uuid

import mongomock

from rangevoting import RangeVote
from repository import MongoRepository


class MongoRepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.database = mongomock.Connection().db
        self.repository = MongoRepository(self.database)

    def test_repository_save(self):
        rangevote = RangeVote(uuid.uuid4(), '?', ['c1', 'c2'])
        self.repository.save(rangevote)

        element = self.database.rangevote.find_one()

        self.assertEqual(rangevote.question, element['question'])
        self.assertEqual(rangevote.choices, element['choices'])

    def test_repository_get(self):
        rangevote_id = uuid.uuid4()
        rangevote = RangeVote(rangevote_id, '?', ['c1', 'c2'])
        self.repository.save(rangevote)

        element = self.repository.get(rangevote_id)

        self.assertEqual(rangevote.question, element['question'])
        self.assertEqual(rangevote.choices, element['choices'])
