"""
The :class:`.Draft` class is TinyAPI's interface for creating, editing, and sending messages.
"""

class Draft(object):
    """A draft message."""

    def __init__(self, session, message_id=None):
        """Initialize a draft.

        Specifying ``message_id`` means you're editing an existing draft, while omitting it means you're attempting to create a new draft.
        """
        self.session = session
        self.message_id = message_id 
        self.data = {
            "__model": "Message",
            "content": {
                "__model": "Message_Content"
            } 
        }
        
    def fetch(self):
        """Fetch data corresponding to this draft and store it as ``self.data``."""
        if self.message_id is None:
            raise Exception(".message_id not set.")
        response = self.session.request("find:Message.content", [ self.message_id ])
        if response == None:
            raise Exception("Message not found.")
        self.data = response
        return self
    
    def save(self):
        """Save current draft state."""
        response = self.session.request("save:Message", [ self.data ])
        self.data = response
        self.message_id = self.data["id"]
        return self
    
    @property
    def subject(self):
        """Get or set the subject line."""
        return self.data.get("subject")
    
    @subject.setter
    def subject(self, value):
        self.data["subject"] = value

    @property
    def body(self):
        """Get or set the draft's body. Expects HTML."""
        return self.data["content"].get("html")
    
    @body.setter
    def body(self, value):
        self.data["content"]["html"] = value

    @property
    def public_message(self):
        """Get or set whether this message should be listed publicly.

        Must be ``True`` or ``False``.
        """
        return self.data.get("public_message")
    
    @public_message.setter
    def public_message(self, value):
        if value not in [ True, False ]:
            raise Exception("Value must be `True` or `False`")
        self.data["public_message"] = value

    def send_preview(self): # pragma: no cover
        """Send a preview of this draft."""
        response = self.session.request("method:queuePreview", [ self.data ])
        self.data = response
        return self
    
    def send(self): # pragma: no cover
        """Send the draft."""
        response = self.session.request("method:queue", [ self.data ])
        self.data = response
        return self
    
    def delete(self):
        """Delete the draft."""
        response = self.session.request("delete:Message", [ self.message_id ])
        self.data = response
        return self
    
    def __repr__(self):
        _id = self.message_id or "{unregistered}"
        return "<Draft {0}>".format(_id)
