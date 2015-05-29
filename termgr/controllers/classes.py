"""Controller for terminal class management"""

from peewee import DoesNotExist
from homeinfo.lib.wsgi import WsgiController, Error, OK
from homeinfo.terminals.lib.db import Class, Administrator

__all__ = ['TerminalManager']


class ClassManager(WsgiController):
    """Lists, adds and removes terminal classes"""

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
            class_id = self.qd.get('id')
            if class_id is not None:
                try:
                    class_id = int(class_id)
                except (TypeError, ValueError):
                    return Error('Invalid class ID', status=400)
            action = self.qd.get('action')
            if action is None:
                return Error('No action specified', status=400)
            elif action == 'list':
                return self._list()
            elif action == 'add':
                name = self.qd.get('name')
                if name is None:
                    return Error('No name specified', status=400)
                touch = self.qd.get('touch')
                return self._add(name, touch)
            elif action == 'modify':
                if class_id is None:
                    return Error('No class ID specified', status=400)
                else:
                    name = self.qd.get('name')
                    if name is None:
                        return Error('No name specified', status=400)
                    touch = self.qd.get('touch')
                    return self._modify(class_id, name, touch)
            elif action == 'delete':
                if class_id is None:
                    return Error('No class ID specified', status=400)
                else:
                    return self._delete(class_id)
            else:
                return Error('Invalid action', status=400)
        else:
            return Error('Invalid credentials', status=401)

    def _list(self):
        """Lists all available classes"""
        for class_ in Class.select().where(True):
            # TODO: Implement
            class_
            pass

    def _add(self, name, touch):
        """Adds entities"""
        try:
            class_ = Class.get((Class.name == name) & (Class.touch == touch))
        except DoesNotExist:
            class_ = Class()
            class_.name = name
            class_.touch = touch
            class_.save()
        return OK(str(class_.id))

    def _modify(self, class_id, name=None, touch=None):
        """Modifies the class with class_id"""
        try:
            class_ = Class.get((Class.id == class_id))
        except DoesNotExist:
            return Error('No such class', status=400)
        else:
            if name is not None:
                class_.name = name
            if touch is not None:
                class_.touch = touch
            class_.save()
            return OK(str(class_.id))

    def _delete(self, class_id):
        """Removes the class with class_id"""
        try:
            class_ = Class.get((Class.id == class_id))
        except DoesNotExist:
            return Error('No such class', status=400)
        else:
            class_.delete_instance()
            return OK('deleted')
