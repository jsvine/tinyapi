# tinyapi

`tinyapi` is a Python wrapper around [TinyLetter](https://tinyletter.com/)'s publicly accessible — but undocumented — API. Built and maintained by the author of [Data Is Plural](https://tinyletter.com/data-is-plural), a weekly newsletter of interesting/curious datasets.

__See also__: [`tinystats`](https://github.com/jsvine/tinystats), a command-line tool for fetching data from the TinyLetter API. No programming knowledge required.

## Warning

It's probably unwise to depend on `tinyapi` for anything important. The library's functionality depends on an undocumented API. If that API changes, `tinyapi` will likely break.

## Installation

```
pip install tinyapi
```

Note: `tinyapi` has been tested on Python 2.7, 3.1, 3.4, and 3.5.

## Example Usage

```python
import tinyapi
from getpass import getpass

session = tinyapi.Session("my-username", getpass())

# Print data about your most-clicked URL:
print(session.get_urls(count=1))
print("\n---\n")

# Print the open rates of your 5 most recent letters:
messages = session.get_messages(count=5)
for m in messages:
    print(m["stub"] + ": " + m["stats"]["open_rate"])
```

## Detailed Usage

#### `tinyapi.Session(username, password)`

Returns a logged-in session, which you'll use for the rest of the API calls.

---
#### `session.get_profile()`

Returns a dictionary containing your account's profile information.

---
#### `session.count_messages(statuses=DEFAULT_MESSAGE_STATUSES)`

Returns an integer representing the number of messages your account has attempted to send. `DEFAULT_MESSAGE_STATUSES` is set to `[ "sent", "sending", "failed_review", "failed_disabled", "failed_schedule" ]`.

---
#### `session.count_sent_messages()`

Same as above, but with `statuses=["sent"]`. Ignores pending and failed messages.

---
#### `session.get_messages(statuses=DEFAULT_MESSAGE_STATUSES, order="sent_at desc", offset=None, count=None, content=False)`

Returns a list of messages your account has attempted to send, sorted by `order`, starting at an optional integer `offset`, and optionally limited to the first `offset` items (in sorted order).

Returned data includes various statistics about each message, e.g., `total_opens`, `open_rate`, `total_clicks`, `unsubs`, `soft_bounces`. If `content=True`, the returned data will also include HTML content of each message.

---
#### `session.get_sent_messages(order="sent_at desc", offset=None, count=None, content=False)`

Same as above, but with `statuses=["sent"]`. Ignores pending and failed messages.

---
#### `session.get_drafts(order="updated_at desc", offset=None, count=None, content=False)`

Same as above, but returns a list of draft messages.

---
#### `session.count_urls()`

Returns an integer representing the total number of URLs included in your messages.

---
#### `session.get_urls(self, order="total_clicks desc", offset=None, count=None)`

Returns a list of URLs you've included in messages, sorted by `total_clicks`, starting at an optional integer `offset`, and optionally limited to the first `offset` items (in sorted order).

---
#### `session.get_message_urls(message_id, order="total_clicks desc")`

Same as above, but for a single message. 

You can get the `message_id` from the `get_messages`/`get_sent_messages` methods above.

---
#### `session.count_subscribers()`

Returns an integer representing your newsletter's number of subscribers.

---
#### `session.get_subscribers(order="created_at desc", offset=None, count=None)`

Returns a list of subscribers, sorted by most recent, starting at an optional integer `offset`, and optionally limited to the first `offset` items (in sorted order).

Returned data includes various statistics about each subscriber, e.g., `total_sent`, `total_opens`, `total_clicks`.

## Feedback / Improvements?

[I'm all ears](https://github.com/jsvine/tinyapi/issues/).
