"""Controller for terminal setup management"""

from .abc import Controller

__date__ = "10.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['SetupController']


class SetupController(Controller):
    """Controller for terminal setup automation"""

    def __init__(self):
        """Initialize request path"""
        super().__init__('setup')

    def _run(self, qd):
        """Interpret query dictionary"""
        pass

    def _crate(self, cid, tid):
        """Create or get data for a
        terminal <tid> of customer <cid>
        """
