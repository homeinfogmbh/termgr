# ./dom.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e0f2b2b6088681bd91db874b9eaa9b60ccb9bc46
# Generated 2017-10-18 10:03:27.994297 by PyXB version 1.2.6-DEV using Python 3.6.2.final.0
# Namespace http://xml.homeinfo.de/schema/terminallib

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:d2d33cfa-b3da-11e7-9f72-7427eaa9df7d')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6-DEV'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://xml.homeinfo.de/schema/terminallib', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Complex type {http://xml.homeinfo.de/schema/terminallib}TerminalList with content type ELEMENT_ONLY
class TerminalList (pyxb.binding.basis.complexTypeDefinition):
    """
                A list of terminal short info.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TerminalList')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 10, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element terminal uses Python identifier terminal
    __terminal = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'terminal'), 'terminal', '__httpxml_homeinfo_deschematerminallib_TerminalList_terminal', True, pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 17, 12), )

    
    terminal = property(__terminal.value, __terminal.set, None, None)

    _ElementMap.update({
        __terminal.name() : __terminal
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.TerminalList = TerminalList
Namespace.addCategoryObject('typeBinding', 'TerminalList', TerminalList)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Terminal with content type ELEMENT_ONLY
class Terminal (pyxb.binding.basis.complexTypeDefinition):
    """
                Basic terminal information.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Terminal')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 22, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element tid uses Python identifier tid
    __tid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'tid'), 'tid', '__httpxml_homeinfo_deschematerminallib_Terminal_tid', False, pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 29, 12), )

    
    tid = property(__tid.value, __tid.set, None, '\n                        The terminal identifier.\n                    ')

    
    # Element cid uses Python identifier cid
    __cid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'cid'), 'cid', '__httpxml_homeinfo_deschematerminallib_Terminal_cid', False, pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 36, 12), )

    
    cid = property(__cid.value, __cid.set, None, '\n                        The customer identifier.\n                    ')

    
    # Element address uses Python identifier address
    __address = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'address'), 'address', '__httpxml_homeinfo_deschematerminallib_Terminal_address', False, pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 43, 12), )

    
    address = property(__address.value, __address.set, None, "\n                        The terminal's location.\n                    ")

    
    # Attribute scheduled uses Python identifier scheduled
    __scheduled = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'scheduled'), 'scheduled', '__httpxml_homeinfo_deschematerminallib_Terminal_scheduled', pyxb.binding.datatypes.dateTime)
    __scheduled._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 51, 8)
    __scheduled._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 51, 8)
    
    scheduled = property(__scheduled.value, __scheduled.set, None, '\n                    Date and time when the terminal is scheduled for delivery.\n                ')

    
    # Attribute deployed uses Python identifier deployed
    __deployed = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'deployed'), 'deployed', '__httpxml_homeinfo_deschematerminallib_Terminal_deployed', pyxb.binding.datatypes.dateTime)
    __deployed._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 58, 8)
    __deployed._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 58, 8)
    
    deployed = property(__deployed.value, __deployed.set, None, '\n                    Date and time when the terminal was deployed.\n                ')

    
    # Attribute annotation uses Python identifier annotation
    __annotation = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'annotation'), 'annotation', '__httpxml_homeinfo_deschematerminallib_Terminal_annotation', pyxb.binding.datatypes.string)
    __annotation._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 65, 8)
    __annotation._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 65, 8)
    
    annotation = property(__annotation.value, __annotation.set, None, '\n                   An optional annotation.\n                ')

    
    # Attribute serial_number uses Python identifier serial_number
    __serial_number = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'serial_number'), 'serial_number', '__httpxml_homeinfo_deschematerminallib_Terminal_serial_number', pyxb.binding.datatypes.string)
    __serial_number._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 72, 8)
    __serial_number._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 72, 8)
    
    serial_number = property(__serial_number.value, __serial_number.set, None, '\n                   An optional serial number of the respective device.\n                ')

    _ElementMap.update({
        __tid.name() : __tid,
        __cid.name() : __cid,
        __address.name() : __address
    })
    _AttributeMap.update({
        __scheduled.name() : __scheduled,
        __deployed.name() : __deployed,
        __annotation.name() : __annotation,
        __serial_number.name() : __serial_number
    })
_module_typeBindings.Terminal = Terminal
Namespace.addCategoryObject('typeBinding', 'Terminal', Terminal)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Address with content type ELEMENT_ONLY
class Address (pyxb.binding.basis.complexTypeDefinition):
    """
                A Terminal's address.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Address')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 82, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element street uses Python identifier street
    __street = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'street'), 'street', '__httpxml_homeinfo_deschematerminallib_Address_street', False, pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 89, 12), )

    
    street = property(__street.value, __street.set, None, None)

    
    # Element house_number uses Python identifier house_number
    __house_number = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'house_number'), 'house_number', '__httpxml_homeinfo_deschematerminallib_Address_house_number', False, pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 90, 12), )

    
    house_number = property(__house_number.value, __house_number.set, None, None)

    
    # Element city uses Python identifier city
    __city = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'city'), 'city', '__httpxml_homeinfo_deschematerminallib_Address_city', False, pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 91, 12), )

    
    city = property(__city.value, __city.set, None, None)

    
    # Element zip_code uses Python identifier zip_code
    __zip_code = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'zip_code'), 'zip_code', '__httpxml_homeinfo_deschematerminallib_Address_zip_code', False, pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 92, 12), )

    
    zip_code = property(__zip_code.value, __zip_code.set, None, None)

    
    # Attribute annotation uses Python identifier annotation
    __annotation = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'annotation'), 'annotation', '__httpxml_homeinfo_deschematerminallib_Address_annotation', pyxb.binding.datatypes.string)
    __annotation._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 94, 8)
    __annotation._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 94, 8)
    
    annotation = property(__annotation.value, __annotation.set, None, '\n                   An optional annotation.\n                ')

    _ElementMap.update({
        __street.name() : __street,
        __house_number.name() : __house_number,
        __city.name() : __city,
        __zip_code.name() : __zip_code
    })
    _AttributeMap.update({
        __annotation.name() : __annotation
    })
_module_typeBindings.Address = Address
Namespace.addCategoryObject('typeBinding', 'Address', Address)


terminals = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'terminals'), TerminalList, location=pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 7, 4))
Namespace.addCategoryObject('elementBinding', terminals.name().localName(), terminals)



TerminalList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'terminal'), Terminal, scope=TerminalList, location=pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 17, 12)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 17, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TerminalList._UseForTag(pyxb.namespace.ExpandedName(None, 'terminal')), pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 17, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
TerminalList._Automaton = _BuildAutomaton()




Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'tid'), pyxb.binding.datatypes.integer, scope=Terminal, documentation='\n                        The terminal identifier.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 29, 12)))

Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'cid'), pyxb.binding.datatypes.integer, scope=Terminal, documentation='\n                        The customer identifier.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 36, 12)))

Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'address'), Address, scope=Terminal, documentation="\n                        The terminal's location.\n                    ", location=pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 43, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 43, 12))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'tid')), pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 29, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'cid')), pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 36, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'address')), pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 43, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Terminal._Automaton = _BuildAutomaton_()




Address._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'street'), pyxb.binding.datatypes.string, scope=Address, location=pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 89, 12)))

Address._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'house_number'), pyxb.binding.datatypes.string, scope=Address, location=pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 90, 12)))

Address._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'city'), pyxb.binding.datatypes.string, scope=Address, location=pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 91, 12)))

Address._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'zip_code'), pyxb.binding.datatypes.string, scope=Address, location=pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 92, 12)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Address._UseForTag(pyxb.namespace.ExpandedName(None, 'street')), pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 89, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Address._UseForTag(pyxb.namespace.ExpandedName(None, 'house_number')), pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 90, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Address._UseForTag(pyxb.namespace.ExpandedName(None, 'city')), pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 91, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Address._UseForTag(pyxb.namespace.ExpandedName(None, 'zip_code')), pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 92, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Address._Automaton = _BuildAutomaton_2()

