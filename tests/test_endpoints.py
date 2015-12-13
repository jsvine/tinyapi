from unittest import TestCase
import tinyapi
from getpass import getpass

USERNAME = "tinyapi-test-account"
session = tinyapi.Session(USERNAME, getpass())

class TestSession(TestCase):
    def test_get_profile(self):
        profile = session.get_profile()
        assert(profile["username"] == USERNAME)

    def test_count_messages(self):
        assert(session.count_messages() > 0)

    def test_get_messages(self):
        msgs = session.get_messages()
        assert(len(msgs) > 0)

    def test_get_message(self):
        msg = session.get_messages(count=1)[-1]
        sub = session.get_message(msg["id"])
        assert(type(sub["stats"]["total_opens"]) == int)

        msg = session.get_messages(count=1, content=True)[-1]
        sub = session.get_message(msg["id"])
        assert(len(sub["content"]["html"]) > 0)

    def test_get_drafts(self):
        drafts = session.get_drafts()
        assert(type(drafts) == list)

    def test_count_urls(self):
        assert(session.count_urls() > 0)

    def test_get_urls(self):
        assert(len(session.get_urls()) > 0)

    def test_get_message_urls(self):
        message = session.get_messages()[-1]
        urls = session.get_message_urls(message["id"])
        assert(len(urls) > 0)

    def test_count_subscribers(self):
        assert(session.count_subscribers() > 0)

    def test_get_subscribers(self):
        assert(len(session.get_subscribers()) > 0)

    def test_get_subscriber(self):
        subscriber = session.get_subscribers()[-1]
        sub = session.get_subscriber(subscriber["id"])
        assert(type(sub["stats"]["last_sent_at"]) == int)
