"""DB -> XML conversion"""

from .termgr import Class, Address, Terminal, TerminalDetail

__date__ = "08.04.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['terminal2xml']


def cls2xml(cls):
    """Converts a terminal class record to an XML class binding"""
    result = Class()
    result.name = cls.name
    result.touch = True if cls.touch else False
    return result


def location2xml(location):
    """Converts a terminal location record into an XML class binding"""
    result = Address()
    result.street = location.street
    result.house_number = location.house_number
    result.city = location.city
    result.zip = location.zip
    return result


def terminal2xml(terminal, cid=False, details=None):
    """Converts a terminal record into an XML class binding"""
    if details is None:
        result = Terminal()
    else:
        result = TerminalDetail()
        result.status = details.status
        result.uptime = details.uptime
        result.screenshot = details.screenshot
        result.touch_event = [e for e in details.touch_events]
    """Sets basic terminal data"""
    if cid:
        result.cid = terminal.cid
    result.tid = terminal.tid
    result.cls = cls2xml(terminal.cls)
    result.domain = terminal.domain.name
    result.ipv4addr = str(terminal.ipv4addr)
    result.virtual_display = terminal.virtual_display
    result.location = location2xml(terminal.location)
    return result
