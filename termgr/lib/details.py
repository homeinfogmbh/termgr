"""Library for terminal data"""

from datetime import datetime
from homeinfolib.mime import mimetype

__date__ = "17.04.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['TerminalDetails']


class TerminalDetails():
    """Terminal details wrapper"""

    @classmethod
    def mockup(cls, screenshot_data=None):
        """Mockup for testing"""
        if screenshot_data is None:
            with open('/home/rne/asdm04.jpg', 'rb') as f:
                screenshot_data = f.read()
        status = 'UP'
        uptime = 10000
        screenshot = (datetime.now(), mimetype(screenshot_data),
                      screenshot_data)
        touch_events = [(datetime.now(), 0, 1, 3),
                        (datetime.now(), 123, 423, 54)]
        return cls(status, uptime, screenshot, touch_events)

    def __init__(self, status, uptime, screenshot, touch_events):
        """Sets detail data"""
        self._status = status
        self._uptime = uptime
        self._screenshot = screenshot
        self._touch_events = touch_events

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
