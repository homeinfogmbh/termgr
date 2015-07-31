"""Converts ORM models to DOM"""

from .dom import TerminalInfo, TerminalDetails, Class, Domain


def class_(class_orm):
    """Converts the class to a DOM"""
    dom = Class(class_orm.name)
    dom.id = class_orm.id
    dom.full_name = class_orm.full_name
    dom.touch = class_orm.touch
    return dom
