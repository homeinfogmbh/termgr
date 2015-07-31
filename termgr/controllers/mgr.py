"""Controller for terminal management"""

from ipaddress import IPv4Address, AddressValueError

from peewee import DoesNotExist

from homeinfo.crm import Address, Customer
from homeinfo.lib.wsgi import WsgiController, Error, OK
from homeinfo.terminals import dom
from homeinfo.terminals.db import Terminal, Class, Domain, Administrator
from hipster.ctrl import TerminalController

__all__ = ['TerminalManager']


class TerminalManager(WsgiController):
    """Lists, adds and removes terminals

    The terminal manager is used for
    internal terminal management
    """

    DEBUG = True

    def _run(self):
        """Runs the terminal manager
        XXX: Authentication by htpasswd
        """
        user_name = self.qd.get('user_name')
        if not user_name:
            return Error('No user name specified', status=400)
        passwd = self.qd.get('passwd')
        if not user_name:
            return Error('No password', status=400)
        if Administrator.authenticate(user_name, passwd):
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
            elif action == 'terminals':
                return self._list_terminals(cid, class_id=class_id)
            elif action == 'customers':
                return self._list_customers()
            elif action == 'details':
                if cid is None:
                    return Error('No customer ID specified', status=400)
                elif tid is None:
                    return Error('No terminal ID specified', status=400)
                else:
                    thumbnail = self.qd.get('thumbnail')
                    try:
                        thumbnail = int(thumbnail)
                    except (ValueError, TypeError):
                        thumbnail = False
                    return self._details(cid, tid, thumbnail=thumbnail)
            # elif action == 'add':
            #     return self._add(cid, tid)
            # elif action == 'modify':
            #     return self._modify_terminal(cid, tid)
            # elif action == 'delete':
            #     return self._delete_terminal(cid, tid)
            else:
                return Error('Invalid action', status=400)
        else:
            return Error('Not authorized', status=403)

    def _add(self, cid, tid):
        """Adds entities"""
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
        return self._add(
            cid, tid, location_id, class_id,
            domain_id, ipv4addr=ipv4addr,
            virtual_display=virtual_display)

    def _modify(self, cid, tid):
        """Adds entities"""
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
        return self._modify_terminal(cid, tid, location_id, class_id,
                                     domain_id,
                                     virtual_display=virtual_display)

    def _delete(self, cid, tid):
        """Adds entities"""
        if cid is None:
            return Error('No customer ID specified', status=400)
        if tid is None:
            return Error('No terminal ID specified', status=400)
        revoke_vpn = self.qd.get('revoke_vpn')
        return self._delete_terminal(cid, tid, revoke_vpn)

    def _list_customers(self):
        """Lists all customers"""
        result = dom.terminals()
        for customer in Customer:
            c = dom.Customer(customer.name)
            c.id = customer.id
            result.customer.append(c)
        return result

    def _list_terminals(self, cid=None, class_id=None, deleted=None):
        """Lists available terminals"""
        if cid is None:
            if class_id is None:
                if deleted is None:
                    terminals = Terminal.select().where(True)
                elif deleted:
                    terminals = Terminal.select().where(
                        ~(Terminal.deleted >> None))
                else:
                    terminals = Terminal.select().where(
                        Terminal.deleted >> None)
            else:
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
        else:
            if class_id is None:
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
            else:
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
        result = dom.terminals()
        for terminal in terminals:
            result.terminal.append(terminal.dom(details=False))
        return OK(result, content_type='application/xml')

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
                        try:
                            screenshot = TerminalController(
                                terminal).screenshot(thumbnail=thumbnail)
                        except Exception as e:
                            return Error(str(e))
                    else:
                        try:
                            screenshot = TerminalController(
                                terminal).screenshot()
                        except Exception as e:
                            return Error(str(e))
                else:
                    screenshot = None
                details = terminal.dom(details=True, screenshot=screenshot)
                result.details = details
                return OK(result, content_type='application/xml')

    def _add_terminal(self, cid, tid, location_id, class_id, domain_id,
                      ipv4addr=None, virtual_display=None):
        """Adds a terminal with the specified configuration"""
        terminal = Terminal.by_ids(cid, tid)
        if terminal is None:
            terminal = Terminal()
            terminal.customer = cid
            terminal.tid = Terminal.gen_tid(cid, desired=tid)
            return self._set_terminal_data(
                terminal, location_id=location_id,
                class_id=class_id,
                domain_id=domain_id,
                ipv4addr=ipv4addr, vpn_gen=True,
                virtual_display=virtual_display)
        else:
            return Error('Terminal already exists', status=400)

    def _modify_terminal(self, cid, tid, location_id, class_id, domain_id,
                         virtual_display=None):
        """Modifies a terminal given by cid and tid"""
        if cid is None:
            return Error('No customer ID specified', status=400)
        elif tid is None:
            return Error('No terminal ID specified', status=400)
        else:
            terminal = Terminal.by_ids(cid, tid)
            if terminal is None:
                return Error('No such terminal', status=400)
            else:
                return self._set_terminal_data(
                    terminal,
                    location_id=location_id,
                    class_id=class_id,
                    domain_id=domain_id,
                    vpn_gen=False,
                    virtual_display=virtual_display)

    def _set_terminal_data(self, terminal, location_id=None, class_id=None,
                           domain_id=None, ipv4addr=None, vpn_gen=False,
                           virtual_display=None):
        """Sets data on a terminal instance"""
        if ipv4addr is not None:
            terminal.ipv4addr = Terminal.gen_ipv4addr(desired=ipv4addr)
        if location_id is not None:
            try:
                location = Address.get(Address.id == location_id)
            except DoesNotExist:
                return Error('No such location', status=400)
            terminal._location = location
        if class_id is not None:
            try:
                class_ = Class.get(Class.id == class_id)
            except DoesNotExist:
                return Error('No such class', status=400)
            Terminal.cls = class_
        if domain_id is not None:
            try:
                domain = Domain.get(Domain.id == domain_id)
            except DoesNotExist:
                return Error('No such domain', status=400)
            terminal._domain = domain
        if virtual_display is not None:
            terminal.virtual_display = virtual_display
        if vpn_gen:
            okay = terminal.gen_vpn_keys()
        else:
            okay = True
        try:
            terminal.save()
        except:
            return Error('Could not apply changes', status=500)
        else:
            xml_data = dom.terminals()
            xml_data.terminal = [terminal.todom()]
            if okay:
                return OK(xml_data, content_type='application/xml')
            else:
                return Error(
                    xml_data, content_type='application/xml', status=500)

    def _delete_terminal(self, cid, tid, revoke_vpn=True):
        """Delete a terminal from the terminals list"""
        terminal = Terminal.by_ids(cid, tid, deleted=True)
        if terminal:
            if terminal.deleted:
                return Error('Terminal already deleted', status=200)
            else:
                terminal.deleted = True
                terminal.save()
                return OK('Terminal deleted')
        else:
            return Error('No such terminal', status=400)
