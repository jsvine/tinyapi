import tinyapi
from getpass import getpass

session = tinyapi.Session("tinyapi-test-account", getpass())

# Print data about your most-clicked URL:
print(session.get_urls(count=1))
print("\n---\n")

# Print the open rates of your 5 most recent letters:
messages = session.get_messages(count=5)
for m in messages:
    print(m["stub"] + ": " + m["stats"]["open_rate"])
