"""Abstract base classes."""

from wsgilib import Error, RequestHandler

from termgr.orm import User

__all__ = ['UserAwareHandler']


class UserAwareHandler(RequestHandler):
    """User aware handler."""

    @property
    def user(self):
        """Returns the user."""
        try:
            user_name = self.query['user_name']
        except KeyError:
            raise Error('No user name specified.', status=400) from None

        try:
            passwd = self.query['passwd']
        except KeyError:
            raise Error('No password specified.', status=400) from None

        return User.authenticate(user_name, passwd)
