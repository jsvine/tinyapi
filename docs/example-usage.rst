=============
Example Usage
=============

Fetching message data
---------------------

.. code-block:: python

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


Creating and sending a draft
----------------------------

.. code-block:: python

    import tinyapi
    from getpass import getpass

    session = tinyapi.Session("my-username", getpass())

    draft = session.create_draft()

    draft.subject = "Testing TinyAPI"
    draft.body = "Just a test."
    draft.save()

    draft.send_preview()
