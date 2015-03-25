from rangevoting import RangeVote


class CreateRangeVoteHandler():
    def __init__(self, rangevote_repository):
        self.repository = rangevote_repository

    def handle(self, command):
        rangevote = RangeVote(command.uuid, command.question, command.choices)
        self.repository.save(rangevote)
