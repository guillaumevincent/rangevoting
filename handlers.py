from rangevoting import RangeVote


class CreateRangeVoteHandler():
    def __init__(self, rangevote_repository):
        self.repository = rangevote_repository

    def handle(self, command):
        rangevote = RangeVote(command.uuid, command.question, command.choices)
        self.repository.save(rangevote)


class GetRangeVoteHandler:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, query):
        return self.repository.get(query.uuid)