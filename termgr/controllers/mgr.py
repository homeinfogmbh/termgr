"""Controller for terminal management management"""

from homeinfolib.wsgi import WsgiController
from terminallib.db import Terminal
from ..lib.db2xml import terminal2xml
from ..lib.termgr import termgr

__date__ = "25.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = []


class TerminalManager(WsgiController):
    """Manages terminals"""

    def _list_terminals(self):
        """Lists available terminals"""
        cid = self._query_dict.get('cid')
        cls = self._query_dict.get('cls')
        if cid is None:
            if cls is None:
                terminals = Terminal.iselect(True)  # @UndefinedVariable
            else:
                cls = int(cls)
                terminals = Terminal.iselect(   # @UndefinedVariable
                    Terminal._cls == cls)
        else:
            cid = int(cid)
            if cls is None:
                terminals = Terminal.iselect(  # @UndefinedVariable
                    Terminal.customer == cid)
            else:
                cls = int(cls)
                terminals = Terminal.iselect(  # @UndefinedVariable
                    (Terminal.customer == cid) & (Terminal._cls == cls))
        result = termgr()
        for terminal in terminals:
            xml_data = terminal2xml(terminal)
            result.terminal.append(xml_data)
        return result
