import unittest

from commands import CreateRangeVotingCommand


class CreateRangeVotingCommandTestCase(unittest.TestCase):
    def test_has_choices_and_question(self):
        question = 'Question ?'
        choices = ['a', 'b']
        create_rangevoting_command = CreateRangeVotingCommand(question, choices)
        self.assertEqual(question, create_rangevoting_command.question)
        self.assertEqual(choices, create_rangevoting_command.choices)