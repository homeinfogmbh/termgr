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

    def _run(self):
        """foo"""
        cid = self._query_dict.get('cid')
        if cid is not None:
            cid = int(cid)
        tid = self._query_dict.get('tid')
        if tid is not None:
            tid = int(tid)
        cls = self._query_dict.get('cls')
        if cls is not None:
            cls = int(cls)
        action = self._query_dict.get('action')
        if action == 'list':
            return self._list_terminals(cid, cls)
        elif action == 'details':
            return self._details(cid, tid)
        else:
            return None

    def _list_terminals(self, cid, cls):
        """Lists available terminals"""
        if cid is None:
            if cls is None:
                terminals = Terminal.iselect(True)  # @UndefinedVariable
            else:
                terminals = Terminal.iselect(   # @UndefinedVariable
                    Terminal._cls == cls)
        else:
            if cls is None:
                terminals = Terminal.iselect(  # @UndefinedVariable
                    Terminal.customer == cid)
            else:
                terminals = Terminal.iselect(  # @UndefinedVariable
                    (Terminal.customer == cid) & (Terminal._cls == cls))
        result = termgr()
        for terminal in terminals:
            xml_data = terminal2xml(terminal)
            result.terminal.append(xml_data)
        return result

    def _details(self, cid, tid):
        """Get details of a certain terminal"""
        if cid is None or tid is None:
            return None  # TODO: handle error
        else:
            terminal = Terminal.iget(   # @UndefinedVariable
                (Terminal.customer == cid)
                & (Terminal.tid == tid))
            result = termgr()
            terminal_detail = terminal2xml(terminal, cid=True, details=None)
            result.terminal_detail = terminal_detail
            return result
