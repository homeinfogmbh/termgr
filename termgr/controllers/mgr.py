"""Controller for terminal management management"""

from os import chdir
from datetime import datetime
from ipaddress import IPv4Address, AddressValueError
from homeinfolib.mime import mimetype
from homeinfolib.wsgi import WsgiController, Error, OK
from homeinfo.crm.address import Address
from terminallib.db import Terminal, Class, Domain
from terminallib.config import net, openvpn
from ..lib.db2xml import terminal2xml
from ..lib.termgr import termgr
from homeinfolib.system import run

__date__ = "25.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['TerminalManager']


class TerminalDetails():
    """Terminal details wrapper"""

    @classmethod
    def mockup(cls):
        """Mockup for testing"""
        with open('/home/rne/asdm04.jpg', 'rb') as f:
            data = f.read()
        status = 'UP'
        uptime = 10000
        screenshot = (datetime.now(), mimetype(data), data)
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


class TerminalManager(WsgiController):
    """Lists, adds and removes terminals

    The terminal manager is used for
    internal terminal management
    """

    DEBUG = True

    def _run(self):
        """Runs the terminal manager"""
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
        cls_id = self.qd.get('cls')
        if cls_id is not None:
            try:
                cls_id = int(cls_id)
            except (ValueError, TypeError):
                return Error('Invalid class ID', status=400)
        action = self.qd.get('action')
        if action is None:
            return Error('No action specified', status=400)
        elif action == 'list':
            return self._list_terminals(cid, cls_id)
        elif action == 'details':
            if cid is None:
                return Error('No customer ID specified')
            if tid is None:
                return Error('No terminal ID specified')
            return self._details(cid, tid)
        elif action == 'add':
            if cid is None:
                return Error('No customer ID specified')
            if tid is None:
                return Error('No terminal ID specified')
            street = self.qd.get('street')
            if street is None:
                return Error('No street specified')
            house_number = self.qd.get('house_number')
            if house_number is None:
                return Error('No house number specified')
            zip_code = self.qd.get('zip_code')
            if zip_code is None:
                return Error('No zip code specified')
            city = self.qd.get('city')
            if city is None:
                return Error('No city specified')
            cls_name = self.qd.get('cls_name')
            touch = self.qd.get('touch')
            if cls_id is None and (cls_name is None or touch is None):
                return Error('Must either specify terminal class'
                             ' id or class name and touch flag')
            domain = self.qd.get('domain')
            if domain is None:
                return Error('No domain specified', status=400)
            ipv4addr = self.qd.get('ipv4addr')
            if ipv4addr is not None:
                try:
                    ipv4addr = IPv4Address(ipv4addr)
                except AddressValueError:
                    return Error('Invalid IPv4 address', status=400)
            virtual_display = self.qd.get('virtual_display')
            display = self._add(cid, tid, street, house_number, zip_code, city,
                                cls_id=cls_id, cls_name=cls_name, touch=touch,
                                domain=domain, ipv4addr=ipv4addr,
                                virtual_display=virtual_display)
            return display
        else:
            return Error('Invalid action', status=400)

    def _list_terminals(self, cid=None, cls=None):
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
            xml_data = terminal2xml(terminal, cid=True)
            result.terminal.append(xml_data)
        return OK(result, content_type='application/xml')

    def _details(self, cid, tid):
        """Get details of a certain terminal"""
        result = termgr()
        if cid is None or tid is None:
            return result  # TODO: handle error
        else:
            terminal = Terminal.iget(   # @UndefinedVariable
                (Terminal.customer == cid)
                & (Terminal.tid == tid))
            details = TerminalDetails.mockup()  # XXX: Testing
            terminal_detail = terminal2xml(terminal, cid=True, details=details)
            result.terminal_detail = terminal_detail
            return OK(result, content_type='application/xml')

    def _gen_ip_addr(self):
        """Generates a unique IPv4 address for the terminal"""
        net_base = net['IPV4NET']
        ipv4addr_base = IPv4Address(net_base)
        # Skip *.0 (network) and *.1 (server)
        ipv4addr = ipv4addr_base + 2
        while ipv4addr in Terminal.used_ipv4addr:
            ipv4addr += 1
        return ipv4addr

    def _get_ipv4addr(self, ipv4addr):
        """Gets a valid, unused IPv4 address for a terminal"""
        try:
            ipv4addr = IPv4Address(ipv4addr)
        except AddressValueError:
            return self._gen_ip_addr()
        else:
            if ipv4addr not in Terminal.used_ipv4addr:
                return ipv4addr
            else:
                return self._gen_ip_addr()

    def _add_addr(self, street, house_number, zip_code, city):
        """Adds an address record to the database"""
        addr = Address.iselect(  # @UndefinedVariable
            (Address.street == street) &
            (Address.house_number == house_number) &
            (Address.zip_code == zip_code) &
            (Address.city == city))
        if addr is None:
            addr = Address()
            addr.street = street
            addr.house_number = house_number
            addr.zip_code = zip_code
            addr.city = city
            addr.isave()
        return addr

    def _add_cls(self, cls_id, cls_name, touch):
        """Adds a terminal class"""
        if cls_id is not None:
            return cls_id
        else:
            cls = Class.iget(  # @UndefinedVariable
                (Class.name == cls_name) & (Class.touch == touch))
            if cls is None:
                cls = Class()
                cls.name = cls_name
                cls.touch = True if touch else False
                cls.isave()
            return cls

    def _add_domain(self, fqdn):
        """Adds a domain with a certain FQDN"""
        domain = Domain.iget(Domain._fqdn == fqdn)  # @UndefinedVariable
        if domain is None:
            domain = Domain
            domain.fqdn = fqdn
            domain.isave()
        return domain

    def _get_tid(self, cid, tid):
        """Gets a unique terminal ID for the customer"""
        if tid is None:
            return self._gen_tid(cid)
        else:
            if tid in Terminal.used_tids(cid):
                return self._gen_tid(cid)
            else:
                return tid

    def _gen_tid(self, cid):
        """Generates a unique terminal identifier for a customer"""
        tid = 1
        while tid in Terminal.used_tids(cid):
            tid += 1
        return tid

    def _gen_vpn(self, cid, tid):
        """Generates an OpenVPN key pair for the terminal"""
        rsa_dir = openvpn['EASY_RSA_DIR']
        build_script = openvpn['BUILD_SCRIPT']
        name = '.'.join([str(tid), str(cid)])
        chdir(rsa_dir)
        pr = run([build_script, name])
        return str(pr)

    def _add(self, cid, tid, street, house_number, zip_code, city, cls_id,
             cls_name=None, touch=None, domain=None, ipv4addr=None,
             virtual_display=None):
        """Adds a terminal with the specified configuration"""
        term = Terminal.by_ids(cid, tid)
        if term is None:
            term = Terminal()
            term.customer = cid
            term.tid = self._get_tid(tid)
            term.ipv4addr = self._get_ipv4addr(ipv4addr)
            term._location = self._add_addr(street, house_number, zip_code)
            term._cls = self._add_cls(cls_id, cls_name, touch)
            term._domain = self._add_domain(domain)
            term.virtual_display = virtual_display
            self._gen_vpn(cid, tid)
            try:
                term.isave()
            except:
                return Error('Could not save display', status=500)
            else:
                try:
                    xml_data = terminal2xml(term, cid=True)
                except:
                    return Error('Could not convert terminal data to XML',
                                 status=500)
                else:
                    return OK(xml_data, content_type='application/xml')
        else:
            return Error('Terminal already exists', status=400)
