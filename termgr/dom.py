# ./dom.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e0f2b2b6088681bd91db874b9eaa9b60ccb9bc46
# Generated 2017-09-08 11:44:53.068316 by PyXB version 1.2.6-DEV using Python 3.6.2.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:5d492f96-947a-11e7-988b-7427eaa9df7d')

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
                A list of terminal short info
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
                Basic terminal information
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Terminal')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 22, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element address uses Python identifier address
    __address = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'address'), 'address', '__httpxml_homeinfo_deschematerminallib_Terminal_address', False, pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 29, 12), )

    
    address = property(__address.value, __address.set, None, "\n                        The terminal's location\n                    ")

    
    # Attribute tid uses Python identifier tid
    __tid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'tid'), 'tid', '__httpxml_homeinfo_deschematerminallib_Terminal_tid', pyxb.binding.datatypes.integer, required=True)
    __tid._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 37, 8)
    __tid._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 37, 8)
    
    tid = property(__tid.value, __tid.set, None, '\n                    The terminal identifier\n                ')

    
    # Attribute cid uses Python identifier cid
    __cid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cid'), 'cid', '__httpxml_homeinfo_deschematerminallib_Terminal_cid', pyxb.binding.datatypes.integer, required=True)
    __cid._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 44, 8)
    __cid._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 44, 8)
    
    cid = property(__cid.value, __cid.set, None, '\n                    The customer identifier\n                ')

    
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
    
    annotation = property(__annotation.value, __annotation.set, None, '\n                   An optional annotation\n                ')

    _ElementMap.update({
        __address.name() : __address
    })
    _AttributeMap.update({
        __tid.name() : __tid,
        __cid.name() : __cid,
        __scheduled.name() : __scheduled,
        __deployed.name() : __deployed,
        __annotation.name() : __annotation
    })
_module_typeBindings.Terminal = Terminal
Namespace.addCategoryObject('typeBinding', 'Terminal', Terminal)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Address with content type EMPTY
class Address (pyxb.binding.basis.complexTypeDefinition):
    """
                Terminal address
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Address')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 75, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute street uses Python identifier street
    __street = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'street'), 'street', '__httpxml_homeinfo_deschematerminallib_Address_street', pyxb.binding.datatypes.string)
    __street._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 81, 8)
    __street._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 81, 8)
    
    street = property(__street.value, __street.set, None, None)

    
    # Attribute house_number uses Python identifier house_number
    __house_number = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'house_number'), 'house_number', '__httpxml_homeinfo_deschematerminallib_Address_house_number', pyxb.binding.datatypes.string)
    __house_number._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 82, 8)
    __house_number._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 82, 8)
    
    house_number = property(__house_number.value, __house_number.set, None, None)

    
    # Attribute city uses Python identifier city
    __city = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'city'), 'city', '__httpxml_homeinfo_deschematerminallib_Address_city', pyxb.binding.datatypes.string)
    __city._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 83, 8)
    __city._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 83, 8)
    
    city = property(__city.value, __city.set, None, None)

    
    # Attribute zip_code uses Python identifier zip_code
    __zip_code = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'zip_code'), 'zip_code', '__httpxml_homeinfo_deschematerminallib_Address_zip_code', pyxb.binding.datatypes.string)
    __zip_code._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 84, 8)
    __zip_code._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 84, 8)
    
    zip_code = property(__zip_code.value, __zip_code.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __street.name() : __street,
        __house_number.name() : __house_number,
        __city.name() : __city,
        __zip_code.name() : __zip_code
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




Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'address'), Address, scope=Terminal, documentation="\n                        The terminal's location\n                    ", location=pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 29, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 29, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'address')), pyxb.utils.utility.Location('/home/neumann/Projects/termgr/doc/terminals.xsd', 29, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Terminal._Automaton = _BuildAutomaton_()

