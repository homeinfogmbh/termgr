"""Main WSGI framework for the terminal manager"""

# TODO: Migrate to using HIS

from wsgilib import JSON

from termgr.orm import User


class TerminalManagerMessage(JSON):
    """Baic terminal Manager message"""

    def __init__(self, id, message, **kwargs):
        super().__init__({'id': id, 'message': message}, **kwargs)


class Errors():
    """Available error messages"""

    NO_USER_NAME_SPECIFIED = TerminalManagerMessage(
        11, 'No user name specified.', status=400)
    NO_PASSWORD_SPECIFIED = TerminalManagerMessage(
        12, 'No password specified.', status=400)
    NOT_AUTHENTICATED = TerminalManagerMessage(
        13, 'Not authenticated.', status=400)


class AuthenticatedResourceHandler():
    """A Resource handler that needs authentication"""

    def __call__(self):
        """Invokes super method iff authenticated"""
        if self.user:
            return super().__call__()
        else:
            raise Errors.NOT_AUTHENTICATED from None

    @property
    def user(self):
        """Authenticates the respective user"""
        try:
            name = self.query['user']
        except KeyError:
            raise Errors.NO_USER_NAME_SPECIFIED from None
        else:
            try:
                passwd = self.query['passwd']
            except KeyError:
                raise Errors.NO_PASSWORD_SPECIFIED from None
            else:
                return User.authenticate(name, passwd)
