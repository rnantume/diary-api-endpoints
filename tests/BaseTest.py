import unittest
import json
import pprint
from app import create_app


class BaseTest (unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client

        self.entry_body =  {
        'entry_id': 1,
        'title': u'Upcoming interview at GTD.org',
        'entryContent': u'I would have to carry some business cards to give to GTD.org employees',
        'date': ''
    }

    def tearDown(self):
        pass


if __name__ == "__main__":
unittest.main()