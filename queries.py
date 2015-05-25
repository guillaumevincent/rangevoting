class RangeVoteQuery:
    def __init__(self, uuid):
        self.uuid = uuid


class GetRangeVoteQuery(RangeVoteQuery):
    pass


class GetRangeVoteResultsQuery(RangeVoteQuery):
    pass
