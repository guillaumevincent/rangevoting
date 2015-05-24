from rangevoting import RangeVote, Vote


class Handler:
    def __init__(self, rangevote_repository):
        self.repository = rangevote_repository


class CreateRangeVoteHandler(Handler):
    def handle(self, command):
        rangevote = RangeVote(command.uuid, command.question, command.choices)
        self.repository.save(rangevote)


class GetRangeVoteHandler(Handler):
    def handle(self, query):
        return self.repository.get(query.uuid)


class UpdateRangeVoteHandler(Handler):
    def handle(self, command):
        rangevote = RangeVote(command.uuid, command.question, command.choices)
        self.repository.update(command.uuid, rangevote)


class CreateVoteHandler(Handler):
    def handle(self, command):
        vote = Vote(command.elector, command.opinions)
        rangevote = self.repository.get(command.rangevote_id)
        rangevote.add_vote(vote)
        self.repository.update(command.rangevote_id, rangevote)
