import unittest

import commands


class SpyValidator:
    def __init__(self):
        self.command = None
        self.validate_called = False

    def validate(self, command):
        self.validate_called = True
        self.command = command


class CommandsTestCase(unittest.TestCase):
    def test_rangevote_command_validator(self):
        command_validator = commands.RangeVoteCommandValidator({'question': 'Question', 'choices': ['c1', 'c2']})
        self.assertTrue(command_validator.is_valid())

        command_validator = commands.RangeVoteCommandValidator({})
        self.assertFalse(command_validator.is_valid())

        command_validator = commands.RangeVoteCommandValidator({'question': 'Question', 'choices': ['c1']})
        self.assertFalse(command_validator.is_valid())

    def test_create_rangevote_command(self):
        uid = 1
        question = 'Question ?'
        choices = ['a', 'b']

        create_rangevote_command = commands.CreateRangeVoteCommand(uid, question, choices)

        self.assertEqual(uid, create_rangevote_command.uuid)
        self.assertEqual(question, create_rangevote_command.question)
        self.assertEqual(choices, create_rangevote_command.choices)

    def test_update_rangevote_command(self):
        uid = 1
        question = 'Question ?'
        choices = ['a', 'b']

        update_rangevote_command = commands.UpdateRangeVoteCommand(uid, question, choices)

        self.assertEqual(uid, update_rangevote_command.uuid)
        self.assertEqual(question, update_rangevote_command.question)
        self.assertEqual(choices, update_rangevote_command.choices)

    def test_vote_command_validator(self):
        command_validator = commands.VoteCommandValidator({'elector': 'Guillaume Vincent', 'opinions': {}})
        self.assertTrue(command_validator.is_valid())

        command_validator = commands.VoteCommandValidator({})
        self.assertFalse(command_validator.is_valid())

    def test_create_vote_command(self):
        rangevote_id = 1
        elector = 'Guillaume Vincent'
        opinions = {'first opinion': 1, 'second opinion': -2}

        create_vote_command = commands.CreateVoteCommand(rangevote_id, elector, opinions)

        self.assertEqual(rangevote_id, create_vote_command.rangevote_id)
        self.assertEqual(elector, create_vote_command.elector)
        self.assertEqual(opinions, create_vote_command.opinions)
