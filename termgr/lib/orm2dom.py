"""Converts ORM models to DOM"""

from homeinfo.crm import Address, Customer

from .dom import TerminalInfo, TerminalDetails, Class, Domain, Screenshot
from homeinfo.lib.mime import mimetype
from datetime import datetime

__all__ = ['class2dom', 'domain2dom', 'address2dom', 'terminal_info2dom',
           'screenshot2dom', 'customer2dom', 'terminal_details2dom']


def class2dom(class_orm):
    """Converts the ORM of a terminal class to a DOM"""
    dom = Class(class_orm.name)
    dom.id = class_orm.id
    dom.full_name = class_orm.full_name
    dom.touch = class_orm.touch
    return dom


def domain2dom(domain_orm):
    """Converts the ORM of a terminal's domain into a DOM"""
    dom = Domain(domain_orm.fqdn)
    dom.id = domain_orm.id
    return dom


def address2dom(address_orm):
    """Converts an address ORM into a DOM"""
    dom = Address()
    dom.street = address_orm.street
    dom.house_number = address_orm.house_number
    dom.city = address_orm.city
    dom.zip_code = address_orm.zip_code
    dom.id = address_orm.id


def terminal_info2dom(terminal_orm):
    """Converts the ORM of a terminal into a short info DOM"""
    dom = TerminalInfo()
    dom.cid = terminal_orm.customer.id
    if terminal_orm.address:
        dom.location = address2dom(terminal_orm.address)
    dom.class_ = terminal_orm.class_.dom
    dom.domain = terminal_orm.domain.dom
    dom.id = terminal_orm.id
    dom.tid = terminal_orm.tid
    dom.deleted = terminal_orm.deleted
    dom.status = True  # self.status
    dom.ipv4addr = str(terminal_orm.ipv4addr)
    return dom


def screenshot2dom(data, time=None):
    """Creates a screenshot DOM from respective data"""
    dom = Screenshot(data)
    dom.mimetype = mimetype(data)
    dom.timestamp = time or datetime.now()
    return dom


def customer2dom(customer_orm):
    """Creates a customer DOM from a customer ORM"""
    dom = Customer(customer_orm.name)
    dom.id = customer_orm.id
    return dom


def terminal_details2dom(terminal_orm, screenshot_data=None):
    """Converts the ORM of a terminal into a full info DOM"""
    dom = TerminalDetails()
    if terminal_orm.customer:
        dom.customer = customer2dom(terminal_orm.customer)
    dom.uptime = 0
    if terminal_orm.virtual_display:
        dom.virtual_display = terminal_orm.virtual_display
    if screenshot_data is not None:
        dom.screenshot = screenshot2dom(screenshot_data)
    if terminal_orm.address:
        dom.location = address2dom(terminal_orm.address)
    dom.class_ = terminal_orm.class_.dom
    dom.domain = terminal_orm.domain.dom
    dom.id = terminal_orm.id
    dom.tid = terminal_orm.tid
    dom.deleted = terminal_orm.deleted
    dom.status = True  # self.status
    dom.ipv4addr = str(terminal_orm.ipv4addr)
    return dom
