from rangevoting import RangeVote


class RangeVoteHandler():
    def __init__(self, rangevote_repository):
        self.repository = rangevote_repository


class CreateRangeVoteHandler(RangeVoteHandler):
    def handle(self, command):
        rangevote = RangeVote(command.uuid, command.question, command.choices)
        self.repository.save(rangevote)


class GetRangeVoteHandler(RangeVoteHandler):
    def handle(self, query):
        return self.repository.get(query.uuid)


class UpdateRangeVoteHandler(RangeVoteHandler):
    def handle(self, command):
        rangevote = RangeVote(command.uuid, command.question, command.choices)
        self.repository.update(command.uuid, rangevote)
