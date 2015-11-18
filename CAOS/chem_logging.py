"""Singleton logging for the language.

When verbose mode is enabled, logged messages are written to stdout or
stderr, depending on the type of message.  Otherwise they are ignored.
"""

from __future__ import print_function, division, unicode_literals, \
    absolute_import


class DummyLogger(object):
    """Fake logger I'm going to use for now.

    Will return something valid in all cases.
    """

    def __getattr__(self, name, default=None):
        """Return a function that can take anything as a parameter."""

        def _(*a, **kw):
            pass
        return _

logger = DummyLogger()