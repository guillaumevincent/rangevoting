import unittest

from queries import GetRangeVoteQuery


class QueriesTestCase(unittest.TestCase):
    def test_get_rangevote_query(self):
        uuid = 1

        get_rangevote_query = GetRangeVoteQuery(uuid)

        self.assertEqual(uuid, get_rangevote_query.uuid)