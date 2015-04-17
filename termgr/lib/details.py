"""Library for terminal data"""

from homeinfolib.mime import mimetype

__date__ = "17.04.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['TerminalDetails']


class TerminalDetails():
    """Terminal details wrapper"""

    def __init__(self, status=False, uptime=None, screenshot=None,
                 screenshot_data=None, touch_events=None):
        """Initializes the details"""
        self._status = 'UP' if status else 'DOWN'
        self._uptime = uptime or 0
        if screenshot:
            data, timestamp = screenshot
            mtype = mimetype(data)
            self._screenshot = (timestamp, mtype, data)
        else:
            self._screenshot = None
        self._touch_events = touch_events or []

    @property
    def status(self):
        """Returns the status"""
        return self._status

    @property
    def uptime(self):
        """Returns the uptime"""
        return self._uptime

    @property
    def screenshot(self):
        """Returns the screenshot"""
        return self._screenshot

    @property
    def touch_events(self):
        """Returns the touch events"""
        return self._touch_events
