from rangevoting import RangeVoting


class CreateRangeVotingHandler():
    def __init__(self, rangevoting_repository):
        self.repository = rangevoting_repository

    def handle(self, command):
        rangevoting = RangeVoting(command.uuid, command.question, command.choices)
        self.repository.save(rangevoting)
