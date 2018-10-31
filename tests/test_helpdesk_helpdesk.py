"""

import unittest
from mock import MagicMock, patch
from partenon.helpdesk import HelpDesk, HelpDeskUser


class TestHelpDesk(unittest.TestCase):

    @patch('partenon.helpdesk.helpdesk.APIClient')
    def test_create_user(self, mock_api_client):
        mock_object = MagicMock()
        mock_object.get.return_values = dict()
        mock_api_client.return_values = mock_object

        help_desk = HelpDesk()
        kwargs = {'email': 'test', 'first_name': "", 'last_name': ""}
        user = help_desk.create_user(**kwargs)

        self.assertIsInstance(user, HelpDeskUser)
        self.assertTrue(hasattr(user, 'test'))
"""
