class RangeVotingHandler():
    def __init__(self, member_repository):
        self.repository = member_repository

    def handle(self, command):
        self.repository.save()