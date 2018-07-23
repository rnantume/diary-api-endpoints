import unittest
import json
import pprint
from BaseTest import BaseTest


class TestClass(BaseTest):

    def test_create_entry(self):
        """Test API can create an entry """
        res = self.client().post('/api/v1/entries',
                                 content_type='application/json',
                                 data=json.dumps(self.entry_body))
        print(res)
        self.assertEqual(res.status_code, 201)

    def test_get_all_entries(self):
        """Test API can view all entries."""
        res = self.client().post('/api/v1/entries/',
                                 content_type='application/json',
                                 data=json.dumps(self.entry_body))
        print(res)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/entries')
        print(res)
        self.assertEqual(res.status_code, 200)

    def test_fetch_single_entry(self):
        """Test API can view single entry."""
        resp = self.client().get('/api/v1/entry/<int:id>',
                                 content_type='application/json',
                                 data=json.dumps(self.entry_body))
        reply = resp.data
        self.assertEqual(len(reply.entry_body), 1)
self.assertEqual(resp.status_code, 200)