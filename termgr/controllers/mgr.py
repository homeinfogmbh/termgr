"""Controller for terminal management"""

from ipaddress import IPv4Address, AddressValueError
from peewee import DoesNotExist
from homeinfolib.wsgi import WsgiController, Error, OK
from homeinfo.crm.address import Address
from terminallib.db import Terminal, Class, Domain, Administrator
from terminallib.remotectrl import RemoteController
from ..lib.db2xml import terminal2xml
from ..lib.termgr import termgr
from ..lib.details import TerminalDetails

__date__ = "25.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['TerminalManager']


class TerminalManager(WsgiController):
    """Lists, adds and removes terminals

    The terminal manager is used for
    internal terminal management
    """

    DEBUG = True

    def _run(self):
        """Runs the terminal manager"""
        user_name = self.qd.get('user_name')
        if not user_name:
            return Error('No user name specified', status=400)
        passwd = self.qd.get('passwd')
        if not passwd:
            return Error('No password specified', status=400)
        administrator = Administrator.authenticate(user_name, passwd)
        if administrator:
            cid = self.qd.get('cid')
            if cid is not None:
                try:
                    cid = int(cid)
                except (TypeError, ValueError):
                    return Error('Invalid customer ID', status=400)
            tid = self.qd.get('tid')
            if tid is not None:
                try:
                    tid = int(tid)
                except (TypeError, ValueError):
                    return Error('Invalid terminal ID', status=400)
            class_id = self.qd.get('class_id')
            if class_id is not None:
                try:
                    class_id = int(class_id)
                except (ValueError, TypeError):
                    return Error('Invalid class ID', status=400)
            action = self.qd.get('action')
            if action is None:
                return Error('No action specified', status=400)
            elif action == 'list':
                return self._list_terminals(cid, class_id=class_id)
            elif action == 'details':
                if cid is None:
                    return Error('No customer ID specified', status=400)
                elif tid is None:
                    return Error('No terminal ID specified', status=400)
                else:
                    if self.qd.get('thumbnail') is None:
                        thumbnail = False
                    else:
                        thumbnail = True
                    return self._details(cid, tid, thumbnail=thumbnail)
            elif action == 'add':
                return self._add(cid, tid)
            else:
                return Error('Invalid action', status=400)
        else:
            return Error('Invalid credentials', status=401)

    def _add(self, cid, tid):
        """Adds entities"""
        target = self.qd.get('object')
        if target == 'terminal':
            if cid is None:
                return Error('No customer ID specified', status=400)
            if tid is None:
                return Error('No terminal ID specified', status=400)
            location_id = self.qd.get('location')
            if location_id is None:
                return Error('No location specified', status=400)
            else:
                try:
                    location_id = int(location_id)
                except ValueError:
                    Error('location must be an integer', status=400)
            class_id = self.qd.get('class')
            if class_id is None:
                return Error('No class specified', status=400)
            else:
                try:
                    class_id = int(class_id)
                except ValueError:
                    Error('class must be an integer', status=400)
            domain_id = self.qd.get('domain_id')
            if domain_id is None:
                return Error('No domain specified', status=400)
            else:
                try:
                    domain_id = int(domain_id)
                except ValueError:
                    Error('domain must be an integer', status=400)
            ipv4addr = self.qd.get('ipv4addr')
            if ipv4addr is not None:
                try:
                    ipv4addr = IPv4Address(ipv4addr)
                except AddressValueError:
                    return Error('Invalid IPv4 address', status=400)
            virtual_display = self.qd.get('virtual_display')
            display = self._add(cid, tid, location_id, class_id,
                                domain_id, ipv4addr=ipv4addr,
                                virtual_display=virtual_display)
            return display
        else:
            return Error('Invalid target', status=400)

    def _list_terminals(self, cid=None, class_id=None):
        """Lists available terminals"""
        if cid is None:
            if class_id is None:
                terminals = Terminal.iselect(True)  # @UndefinedVariable
            else:
                terminals = Terminal.iselect(   # @UndefinedVariable
                    Terminal._cls == class_id)
        else:
            if class_id is None:
                terminals = Terminal.iselect(  # @UndefinedVariable
                    Terminal.customer == cid)
            else:
                terminals = Terminal.iselect(  # @UndefinedVariable
                    (Terminal.customer == cid) & (Terminal._cls == class_id))
        result = termgr()
        for terminal in terminals:
            xml_data = terminal2xml(terminal, cid=True)
            result.terminal.append(xml_data)
        return OK(result, content_type='application/xml')

    def _details(self, cid, tid, thumbnail=False):
        """Get details of a certain terminal"""
        result = termgr()
        if cid is None or tid is None:
            return Error('No terminal ID or customer ID specified', status=400)
        else:
            try:
                terminal = Terminal.iget(   # @UndefinedVariable
                    (Terminal.customer == cid)
                    & (Terminal.tid == tid))
            except DoesNotExist:
                return Error('No such terminal', status=400)
            else:
                if thumbnail:
                    screenshot = RemoteController(terminal).thumbnail
                else:
                    screenshot = RemoteController(terminal).screenshot
                details = TerminalDetails(status=True,  # TODO: Evaluate this!
                                          uptime=None,  # TODO: Evaluate this!
                                          screenshot=screenshot,
                                          # TODO: Evaluate this!
                                          touch_events=None)
                terminal_detail = terminal2xml(terminal, cid=True,
                                               details=details)
                result.terminal_detail = terminal_detail
                return OK(result, content_type='application/xml')

    def _add_terminal(self, cid, tid, location_id, class_id, domain_id,
                      ipv4addr=None, virtual_display=None):
        """Adds a terminal with the specified configuration"""
        term = Terminal.by_ids(cid, tid)
        if term is None:
            term = Terminal()
            term.customer = cid
            term.tid = Terminal.gen_tid(cid, desired=tid)
            term.ipv4addr = Terminal.gen_ipv4addr(desired=ipv4addr)
            try:
                location = Address.iget(  # @UndefinedVariable
                    Address.id == location_id)  # @UndefinedVariable
            except DoesNotExist:
                return Error('No such location', status=400)
            term._location = location
            try:
                class_ = Class.iget(  # @UndefinedVariable
                    Class.id == class_id)  # @UndefinedVariable
            except DoesNotExist:
                return Error('No such class', status=400)
            term._cls = class_
            try:
                domain = Domain.iget(  # @UndefinedVariable
                    Domain.id == domain_id)  # @UndefinedVariable
            except DoesNotExist:
                return Error('No such class', status=400)
            term._domain = domain
            term.virtual_display = virtual_display
            vpn_gen = term.gen_vpn_keys()
            if vpn_gen:
                term.isave()
                xml_data = termgr()
                xml_data.terminal = [terminal2xml(term, cid=True)]
                return OK(xml_data, content_type='application/xml')
            else:
                Error('Could not generate OpenVPN keys', status=500)
        else:
            return Error('Terminal already exists', status=400)
