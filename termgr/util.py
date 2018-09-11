"""Termgr common utilities."""

from collections import namedtuple

__all__ = ['Addr', 'TerminalLine']


Addr = namedtuple('Addr', ('street', 'house_number', 'zip_code'))
TerminalLine = namedtuple('TerminalLine', ('city', 'addr', 'scheduled'))
