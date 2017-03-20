=========
Changelog
=========

All notable changes to this project will be documented in this file. 

The format is based on `Keep a Changelog <http://keepachangelog.com/>`_.

0.1.0 — 2017-03-19
--------------------

**Added**

* Ability to create, edit, and send drafts
* Docstrings and full test coverage
* Proper documentation via Sphinx

**Changed**

* `DEFAULT_MESSAGE_STATUSES` is now just `[ "sent", "sending" ]` and no longer includes failed-to-send messages.

**Deprecated**

* Removed `Session.count_sent_messages` and `Session.get_sent_messages`, since the change to `DEFAULT_MESSAGE_STATUSES` makes them redundant.

0.0.0 — 2015-12-13
--------------------

Initial release.
