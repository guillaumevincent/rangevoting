import unittest
import uuid

import mongomock

from rangevoting import RangeVote
from repository import MongoRepository


class MongoRepositoryTestCase(unittest.TestCase):
    def test_repository_save(self):
        database = mongomock.Connection().db
        repository = MongoRepository(database)
        rangevote = RangeVote(uuid.uuid4(), '?', ['c1', 'c2'])

        repository.save(rangevote)

        element = database.rangevote.find_one()
        self.assertEqual(rangevote.question, element['question'])
