"""Terminal manager ORM"""

from datetime import datetime

from peewee import ForeignKeyField, IntegerField, CharField, BlobField,\
    DateTimeField

from homeinfo.peewee import create
from homeinfo.terminals.db import TerminalModel, Terminal

__all__ = ['Screenshot', 'ConsoleHistory']


@create
class Screenshot(TerminalModel):
    """Terminal screenshots"""

    terminal = ForeignKeyField(
        Terminal, db_column='terminal', related_name='screenshots')
    screenshot = BlobField()
    thumbnail = BlobField()
    date = DateTimeField(default=None)


@create
class ConsoleHistory(TerminalModel):
    """A physical terminal's virtual console's history"""

    class Meta:
        db_table = 'console_history'

    terminal = ForeignKeyField(
        Terminal, db_column='terminal', related_name='console_log'
    )
    timestamp = DateTimeField(default=datetime.now())
    command = CharField(255)
    stdout = BlobField()
    stderr = BlobField()
    exit_code = IntegerField()
