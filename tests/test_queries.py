import unittest

import queries


class QueriesTestCase(unittest.TestCase):
    def test_get_rangevote_query(self):
        uuid = 1

        get_rangevote_query = queries.GetRangeVoteQuery(uuid)

        self.assertEqual(uuid, get_rangevote_query.uuid)

    def test_get_rangevote_results_query(self):
        uuid = 1

        get_rangevote_results_query = queries.GetRangeVoteResultsQuery(uuid)

        self.assertEqual(uuid, get_rangevote_results_query.uuid)

    def test_get_rangevotes_query(self):

        get_rangevote_results_query = queries.GetRangeVotesQuery()

        self.assertEqual(20, get_rangevote_results_query.count)
