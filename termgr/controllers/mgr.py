"""Controller for terminal management"""

from threading import Thread

from peewee import DoesNotExist

from homeinfo.crm import Customer
from homeinfo.lib.wsgi import WsgiApp, Error, OK
from homeinfo.terminals.orm import Terminal, Class

from ..lib import dom
from ..lib.orm2dom import customer2dom, terminal_info2dom, terminal_details2dom
from ..orm import User

__all__ = ['TerminalManager']


class TerminalManager(WsgiApp):
    """Lists, adds and removes terminals

    The terminal manager is used for
    internal terminal management
    """

    DEBUG = True

    def __init__(self):
        """Initialize with CORS enabled"""
        super().__init__(cors=True)

    def get(self, environ):
        """Runs the terminal manager"""
        query_string = self.query_string(environ)
        qd = self.qd(query_string)
        auth = False
        user_name = qd.get('user_name')

        if not user_name:
            return Error('No user name specified', status=400)
        else:
            passwd = qd.get('passwd')

            if not user_name:
                return Error('No password', status=400)
            else:
                auth = User.authenticate(user_name, passwd)

        if auth:
            cid = qd.get('cid')

            if cid is not None:
                try:
                    cid = int(cid)
                except (TypeError, ValueError):
                    return Error('Invalid customer ID', status=400)

            tid = qd.get('tid')

            if tid is not None:
                try:
                    tid = int(tid)
                except (TypeError, ValueError):
                    return Error('Invalid terminal ID', status=400)

            class_id_or_name = qd.get('class')

            try:
                class_id = int(class_id_or_name)
            except (TypeError, ValueError):
                class_id = None
                class_name = class_id_or_name
            else:
                class_name = None

            action = qd.get('action')

            if action is None:
                return Error('No action specified', status=400)
            elif action == 'terminals':
                deleted = True if qd.get('deleted') else False
                deployed = True if qd.get('deployed') else False

                return self._list_terminals(
                    cid, class_id=class_id, class_name=class_name,
                    deleted=deleted, deployed=deployed)
            elif action == 'customers':
                return self._list_customers()
            elif action == 'classes':
                return self._list_classes(cid)
            elif action == 'details':
                if cid is None:
                    return Error('No customer ID specified', status=400)
                elif tid is None:
                    return Error('No terminal ID specified', status=400)
                else:
                    thumbnail = qd.get('thumbnail')
                    try:
                        thumbnail = int(thumbnail)
                    except (ValueError, TypeError):
                        thumbnail = False

                    return self._details(cid, tid, thumbnail=thumbnail)
            else:
                return Error('Invalid action', status=400)
        else:
            return Error('Not authenticated', status=403)

    def _list_customers(self):
        """Lists all customers"""
        result = dom.terminals()

        for customer in Customer:
            c = customer2dom(customer.name)
            c.id = customer.id
            result.customer.append(c)

        return OK(result, content_type='application/xml')

    def _list_classes(self, cid):
        """Lists all customers"""
        result = dom.terminals()
        classes = {}

        if cid:
            for terminal in Terminal.select().where(
                    Terminal.customer == cid):
                if terminal.class_.id not in classes:
                    classes[terminal.class_.id] = (terminal.class_, 1)
                else:
                    c, n = classes[terminal.class_.id]
                    classes[terminal.class_.id] = (c, n+1)
        else:
            for class_ in Class:
                classes[class_.id] = class_
        for ident in classes:
            class_ = classes[ident]

            try:
                class_, n = class_
            except TypeError:
                n = None

            c = dom.Class(class_.name)
            c.full_name = class_.full_name
            c.touch = class_.touch
            c.id = class_.id

            if n is not None:
                c.amount = n

            result.class_.append(c)

        return OK(result, content_type='application/xml')

    def _list_terminals(self, cid, class_id=None, class_name=None,
                        deleted=None, deployed=None):
        """Lists available terminals
        XXX: <deployed> is not yet implemented
        """
        if cid is None:
            if class_id is not None:
                if deleted is None:
                    terminals = Terminal.select().where(
                        Terminal.class_ == class_id)
                elif deleted:
                    terminals = Terminal.select().where(
                        (Terminal.class_ == class_id) &
                        (~(Terminal.deleted >> None)))
                else:
                    terminals = Terminal.select().where(
                        (Terminal.class_ == class_id) &
                        (Terminal.deleted >> None))
            elif class_name is not None:
                if deleted is None:
                    terminals = Terminal.select().where(
                        Terminal.class_.name == class_name)
                elif deleted:
                    terminals = Terminal.select().where(
                        (Terminal.class_.name == class_name) &
                        (~(Terminal.deleted >> None)))
                else:
                    terminals = Terminal.select().where(
                        (Terminal.class_.name == class_name) &
                        (Terminal.deleted >> None))
            else:
                if deleted is None:
                    terminals = Terminal.select().where(True)
                elif deleted:
                    terminals = Terminal.select().where(
                        ~(Terminal.deleted >> None))
                else:
                    terminals = Terminal.select().where(
                        Terminal.deleted >> None)
        else:
            if class_id is not None:
                if deleted is None:
                    terminals = Terminal.select().where(
                        (Terminal.customer == cid) &
                        (Terminal.class_ == class_id))
                elif deleted:
                    terminals = Terminal.select().where(
                        (Terminal.customer == cid) &
                        (Terminal.class_ == class_id) &
                        (~(Terminal.deleted >> None)))
                else:
                    terminals = Terminal.select().where(
                        (Terminal.customer == cid) &
                        (Terminal.class_ == class_id) &
                        (Terminal.deleted >> None))
            elif class_name is not None:
                if deleted is None:
                    terminals = Terminal.select().where(
                        (Terminal.customer == cid) &
                        (Terminal.class_.name == class_name))
                elif deleted:
                    terminals = Terminal.select().where(
                        (Terminal.customer == cid) &
                        (Terminal.class_.name == class_name) &
                        (~(Terminal.deleted >> None)))
                else:
                    terminals = Terminal.select().where(
                        (Terminal.customer == cid) &
                        (Terminal.class_.name == class_name) &
                        (Terminal.deleted >> None))
            else:
                if deleted is None:
                    terminals = Terminal.select().where(
                        Terminal.customer == cid)
                elif deleted:
                    terminals = Terminal.select().where(
                        (Terminal.customer == cid) &
                        (~(Terminal.deleted >> None)))
                else:
                    terminals = Terminal.select().where(
                        (Terminal.customer == cid) &
                        (Terminal.deleted >> None))

        result = dom.terminals()
        processed_terminals = []
        threads = []

        for terminal in terminals:
            thread = Thread(
                target=self._process_terminal,
                args=[terminal, processed_terminals])
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        for processed_terminal in processed_terminals:
            result.terminal.append(processed_terminal)

        return OK(result, content_type='application/xml')

    def _process_terminal(self, terminal, processed_terminals):
        """Load status of a terminal"""
        processed_terminal = terminal_info2dom(terminal)
        processed_terminals.append(processed_terminal)

    def _details(self, cid, tid, thumbnail=False):
        """Get details of a certain terminal"""
        result = dom.terminals()

        if cid is None or tid is None:
            return Error('No terminal ID or customer ID specified', status=400)
        else:
            try:
                terminal = Terminal.get(
                    (Terminal.customer == cid) &
                    (Terminal.tid == tid))
            except DoesNotExist:
                return Error('No such terminal', status=400)
            else:
                if terminal.status:
                    if thumbnail:
                        raise NotImplementedError()
                    else:
                        raise NotImplementedError()
                else:
                    screenshot = None

                details = terminal_details2dom(
                    terminal, screenshot_data=screenshot)
                result.details = details

                return OK(result, content_type='application/xml')
