import tinyapi
from unittest import TestCase
from getpass import getpass
from nose.tools import raises
import os

DEFAULT_USERNAME = "tinyapi-test-account"
USERNAME = os.environ.get("TINYAPI_TEST_USERNAME") or DEFAULT_USERNAME
PASSWORD = os.environ.get("TINYAPI_TEST_PASSWORD") or getpass()

class TestDraft(TestCase):
    def setUp(self):
        self.session = tinyapi.Session(USERNAME, PASSWORD)

    def test_basic(self):
        draft = self.session.create_draft()
        repr(draft)
        draft.subject = "testing"
        draft.body = "this is the body"
        draft.public_message = True
        message_id = draft.save().message_id
        fetched_draft = self.session.get_draft(message_id)
        assert(fetched_draft.message_id == draft.message_id)
        assert(fetched_draft.subject == draft.subject)
        assert(fetched_draft.body == draft.body)
        assert(fetched_draft.public_message == draft.public_message)
        fetched_draft.delete()

    @raises(Exception)
    def test_bad_id(self):
        draft = self.session.get_draft(1)
        draft.fetch()

    @raises(Exception)
    def test_unsaved_fetch(self):
        draft = self.session.create_draft()
        draft.fetch()

    @raises(Exception)
    def test_bad_public_value(self):
        draft = self.session.create_draft()
        draft.public_message = "a string"
