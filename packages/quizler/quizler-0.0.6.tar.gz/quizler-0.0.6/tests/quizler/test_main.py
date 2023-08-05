# pylint: disable=no-self-use,missing-docstring,invalid-name

import unittest
from unittest import mock

from quizler.main import create_parser, main
from tests.utils import mock_envs, mock_argv


class TestCreateParser(unittest.TestCase):

    def setUp(self):
        self.parser = create_parser()

    def test_with_empty_args(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

    def test_unknown_command(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['ping'])

    def test_common_command(self):
        args = self.parser.parse_args(['common'])
        self.assertEqual(args.command, 'common')

    def test_sets_command(self):
        args = self.parser.parse_args(['sets'])
        self.assertEqual(args.command, 'sets')


@mock_envs(CLIENT_ID='client_id', USER_ID='user_id')
class TestMain(unittest.TestCase):

    @mock.patch('quizler.main.print_common_terms')
    @mock.patch('quizler.main.get_common_terms')
    @mock_argv('common')
    def test_common(self, mock_get_common_terms, mock_print_common_terms):
        main()
        mock_get_common_terms.assert_called_once_with('client_id', 'user_id')
        mock_print_common_terms.assert_called_once_with(mock.ANY)

    @mock.patch('quizler.main.get_user_sets')
    @mock_argv('sets')
    def test_sets(self, mock_get_user_sets):
        main()
        mock_get_user_sets.assert_called_once_with('client_id', 'user_id')
