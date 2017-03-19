class Draft(object):
    def __init__(self, session, message_id=None):
        self.session = session
        self.message_id = message_id 
        self.data = {
            "__model": "Message",
            "content": {
                "__model": "Message_Content"
            } 
        }
        
    def fetch(self):
        if self.message_id is None:
            raise Exception(".message_id not set.")
        response = self.session.request("find:Message.content", [ self.message_id ])
        if response == None:
            raise Exception("Message not found.")
        self.data = response
        return self
    
    def save(self):
        response = self.session.request("save:Message", [ self.data ])
        self.data = response
        self.message_id = self.data["id"]
        return self
    
    @property
    def subject(self):
        return self.data.get("subject")
    
    @subject.setter
    def subject(self, value):
        self.data["subject"] = value

    @property
    def body(self):
        return self.data["content"].get("html")
    
    @body.setter
    def body(self, value):
        self.data["content"]["html"] = value

    @property
    def public_message(self):
        return self.data.get("public_message")
    
    @public_message.setter
    def public_message(self, value):
        if value not in [ True, False ]:
            raise Exception("Value must be `True` or `False`")
        self.data["public_message"] = value

    def send_preview(self): # pragma: no cover
        response = self.session.request("method:queuePreview", [ self.data ])
        self.data = response
        return self
    
    def send(self): # pragma: no cover
        response = self.session.request("method:queue", [ self.data ])
        self.data = response
        return self
    
    def delete(self):
        response = self.session.request("delete:Message", [ self.message_id ])
        self.data = response
        return self
    
    def __repr__(self):
        _id = self.message_id or "{unregistered}"
        return "<Draft {0}>".format(_id)
