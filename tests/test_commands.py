import unittest


class CreateRangeVotingCommand():
    def __init__(self, question, choices):
        self.question = question
        self.choices = choices


class CreateRangeVotingCommandTestCase(unittest.TestCase):
    def test_has_choices_and_question(self):
        question = 'Question ?'
        choices = ['a', 'b']
        create_rangevoting_command = CreateRangeVotingCommand(question, choices)
        self.assertEqual(question, create_rangevoting_command.question)
        self.assertEqual(choices, create_rangevoting_command.choices)


if __name__ == '__main__':
    unittest.main()
