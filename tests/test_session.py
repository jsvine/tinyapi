import tinyapi
from unittest import TestCase
from getpass import getpass
from nose.tools import raises
import os

DEFAULT_USERNAME = "tinyapi-test-account"
USERNAME = os.environ.get("TINYAPI_TEST_USERNAME") or DEFAULT_USERNAME
PASSWORD = os.environ.get("TINYAPI_TEST_PASSWORD") or getpass()

class TestMainInterface(TestCase):
    def test_login(self):
        tinyapi.login(USERNAME, PASSWORD)

class TestSession(TestCase):
    def setUp(self):
        self.session = tinyapi.Session(USERNAME, PASSWORD)

    def test_get_profile(self):
        profile = self.session.get_profile()
        assert(profile["username"] == USERNAME)

    def test_count_messages(self):
        assert(self.session.count_messages() > 0)

    def test_count_sent_messages(self):
        assert(self.session.count_sent_messages() > 0)

    def test_get_messages(self):
        msgs = self.session.get_messages()
        assert(len(msgs) > 0)

    def test_get_sent_messages(self):
        msgs = self.session.get_sent_messages()
        assert(len(msgs) > 0)

    def test_get_message(self):
        msg = self.session.get_messages(count=1)[-1]
        sub = self.session.get_message(msg["id"])
        assert(type(sub["stats"]["total_opens"]) == int)

        msg = self.session.get_messages(count=1, content=True)[-1]
        sub = self.session.get_message(msg["id"])
        assert(len(sub["content"]["html"]) > 0)

    def test_get_drafts(self):
        drafts = self.session.get_drafts()
        assert(type(drafts) == list)

    def test_count_urls(self):
        assert(self.session.count_urls() > 0)

    def test_get_urls(self):
        assert(len(self.session.get_urls()) > 0)

    def test_get_message_urls(self):
        message = self.session.get_messages()[-1]
        urls = self.session.get_message_urls(message["id"])
        assert(len(urls) > 0)

    def test_count_subscribers(self):
        assert(self.session.count_subscribers() > 0)

    def test_get_subscribers(self):
        assert(len(self.session.get_subscribers()) > 0)

    def test_get_subscriber(self):
        subscriber = self.session.get_subscribers()[-1]
        sub = self.session.get_subscriber(subscriber["id"])
        assert(type(sub["stats"]["last_sent_at"]) == int)

class TestBadLogin(TestCase):
    @raises(Exception)
    def test_get_profile(self):
        session = tinyapi.Session(USERNAME, "incorrect-password")
