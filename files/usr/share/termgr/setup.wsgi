#! /usr/bin/env python3
"""Terminal setup interface

XXX: Please note:

    * This web service must be run as a special user,
      allowed to create and read OpenVPN certs.
      (Do NOT run this as root!)

    * This web service must be HTTPS-Password
      protected by the web server, since it does
      not provide authentication by itself
"""

from termgr.controllers.setup import SetupController

__date__ = "25.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"

application = SetupController()
