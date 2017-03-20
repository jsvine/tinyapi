"""
The :class:`.Session` class provides TinyAPI's core functionality. It manages the authentication cookies and token for all requests to TinyLetter's undocumented API.
"""

import requests
import re
import json
from .draft import Draft

URL = "https://app.tinyletter.com/__svcbus__/"


DEFAULT_MESSAGE_STATUSES = [
    "sent",
    "sending",
]

token_pat = re.compile(r'csrf_token="([^"]+)"')

def get_cookies_and_token():
    res = requests.get("https://app.tinyletter.com/")
    token = re.search(token_pat, res.content.decode("utf-8")).group(1)
    return (res.cookies, token)

def create_payload(service, data, token):
    return json.dumps([[[service, data]], [], token])

def fmt_paging(offset, count):
    if offset == None and count == None:
        return None
    return "{0}, {1}".format(offset or 0, count)

class Session(object):
    """An authenticated tinyletter.com session."""

    def __init__(self, username, password=False):
        """Returns a logged-in session."""
        self.username = username
        self.cookies, self.token = get_cookies_and_token()
        self._login(password)

    def _request(self, service, data):
        payload = create_payload(service, data, self.token)
        res = requests.post(URL,
            cookies=self.cookies,
            data=payload,
            headers={'Content-Type': 'application/octet-stream'})
        self.cookies = res.cookies
        return res
    
    def request(self, service, data):
        """
        Makes a call to TinyLetter's __svcbus__ endpoint.
        """
        _res = self._request(service, data)
        res = _res.json()[0][0]
        if res["success"] == True:
            return res["result"]
        else:
            err_msg = res["errmsg"]
            raise Exception("Request not successful: '{0}'".format(err_msg))
    
    def _login(self, password):
        req_data = [self.username, password, None, None, None, None ]
        try:
            self.request("service:User.loginService", req_data)
        except:
            raise Exception("Login not successful.")
    
    def get_profile(self):
        return self.request("service:User.currentUser", [])
    
    def count_messages(self, statuses=DEFAULT_MESSAGE_STATUSES):
        """Returns the number of messages your account has sent.
        
        ``DEFAULT_MESSAGE_STATUSES`` is set to ``[ "sent", "sending" ]``.

        Other possible statuses include "draft", "failed_review", "failed_disabled", and "failed_schedule".
        """
        return self.request("count:Message", [{"status": statuses}])

    def get_messages(self,
            statuses=DEFAULT_MESSAGE_STATUSES,
            order="sent_at desc",
            offset=None,
            count=None,
            content=False):
        """Returns a list of messages your account sent.
        
        Messages are sorted by ``order``, starting at an optional integer ``offset``, and optionally limited to the first ``count`` items (in sorted order).

        Returned data includes various statistics about each message, e.g., ``total_opens``, ``open_rate``, ``total_clicks``, ``unsubs``, ``soft_bounces``. If ``content=True``, the returned data will also include HTML content of each message.
        """

        req_data = [ { "status": statuses }, order, fmt_paging(offset, count) ]
        service = "query:Message.stats"
        if content: service += ", Message.content"
        return self.request(service, req_data)

    def get_drafts(self, **kwargs):
        """Same as Session.get_messages, but where ``statuses=["draft"]``."""
        default_kwargs = { "order": "updated_at desc" }
        default_kwargs.update(kwargs)
        return self.get_messages(statuses=["draft"], **default_kwargs)

    def get_message(self, message_id):
        """Return stats *and* message content for a given message."""
        req_data = [ str(message_id) ]
        return self.request("find:Message.stats, Message.content", req_data)

    def count_urls(self):
        """Returns the total number of URLs included in your messages"""
        return self.request("count:Message_Url", [ None ])
    
    def get_urls(self, order="total_clicks desc", offset=None, count=None):
        """Returns a list of URLs you've included in messages.

        List is sorted by ``total_clicks``, starting at an optional integer ``offset``, and optionally limited to the first ``count`` items.
        """
        req_data = [ None, order, fmt_paging(offset, count) ]
        return self.request("query:Message_Url", req_data)
        
    def get_message_urls(self, message_id, order="total_clicks desc"):
        """Returns a list of URLs you've included in a specific message.

        List is sorted by ``total_clicks``, starting at an optional integer ``offset``, and optionally limited to the first ``count`` items.
        """
        req_data = [ { "message_id": str(message_id) }, order, None ]
        return self.request("query:Message_Url", req_data)
        
    def count_subscribers(self):
        """Returns your newsletter's number of subscribers."""
        return self.request("count:Contact", [ None ])
    
    def get_subscribers(self, 
            order="created_at desc",
            offset=None,
            count=None):
        """Returns a list of subscribers.
        
        List is sorted by most-recent-to-subsribe, starting at an optional integer ``offset``, and optionally limited to the first ``count`` items (in sorted order).

        Returned data includes various statistics about each subscriber, e.g., ``total_sent``, ``total_opens``, ``total_clicks``.
        """
        req_data = [ None, order, fmt_paging(offset, count)]
        return self.request("query:Contact.stats", req_data)
    
    def get_subscriber(self, subscriber_id):
        """Returns data corresponding to a specific subcriber."""
        req_data = [ str(subscriber_id) ]
        return self.request("find:Contact.stats", req_data)

    def create_draft(self):
        """Create a new draft message."""
        return Draft(self)

    def edit_draft(self, message_id):
        """Fetch a specific draft to be edited."""
        return Draft(self, message_id).fetch()
