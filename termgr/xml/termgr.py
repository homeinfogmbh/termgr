# ./termgr.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:d5297d54a5b0a5c243ac8f456d16d54e3b56338f
# Generated 2015-03-25 14:00:25.022295 by PyXB version 1.2.5-DEV using Python 3.4.3.final.0
# Namespace http://xml.homeinfo.de/schema/termgr

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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:e720f1c2-d2ee-11e4-986b-7427eaa9df7d')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.5-DEV'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://xml.homeinfo.de/schema/termgr', create_if_missing=True)
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


# Atomic simple type: {http://xml.homeinfo.de/schema/termgr}TerminalStatus
class TerminalStatus (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """
                The status of the terminal
            """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TerminalStatus')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 188, 4)
    _Documentation = '\n                The status of the terminal\n            '
TerminalStatus._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=TerminalStatus)
TerminalStatus.UP = TerminalStatus._CF_enumeration.addEnumeration(unicode_value='UP', tag='UP')
TerminalStatus.DOWN = TerminalStatus._CF_enumeration.addEnumeration(unicode_value='DOWN', tag='DOWN')
TerminalStatus._InitializeFacetMap(TerminalStatus._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'TerminalStatus', TerminalStatus)

# Atomic simple type: {http://xml.homeinfo.de/schema/termgr}IPv4Address
class IPv4Address (pyxb.binding.datatypes.string):

    """
                An IPv4 address
            """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IPv4Address')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 202, 4)
    _Documentation = '\n                An IPv4 address\n            '
IPv4Address._CF_pattern = pyxb.binding.facets.CF_pattern()
IPv4Address._CF_pattern.addPattern(pattern='(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])')
IPv4Address._InitializeFacetMap(IPv4Address._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'IPv4Address', IPv4Address)

# Complex type {http://xml.homeinfo.de/schema/termgr}TerminalManager with content type ELEMENT_ONLY
class TerminalManager (pyxb.binding.basis.complexTypeDefinition):
    """
                A terminal web API solution by HOMEINFO Digitale Informationssysteme GmbH
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TerminalManager')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 12, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element customer uses Python identifier customer
    __customer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'customer'), 'customer', '__httpxml_homeinfo_deschematermgr_TerminalManager_customer', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 19, 12), )

    
    customer = property(__customer.value, __customer.set, None, None)

    
    # Element terminal uses Python identifier terminal
    __terminal = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'terminal'), 'terminal', '__httpxml_homeinfo_deschematermgr_TerminalManager_terminal', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 20, 12), )

    
    terminal = property(__terminal.value, __terminal.set, None, None)

    
    # Element screenshot uses Python identifier screenshot
    __screenshot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'screenshot'), 'screenshot', '__httpxml_homeinfo_deschematermgr_TerminalManager_screenshot', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 21, 12), )

    
    screenshot = property(__screenshot.value, __screenshot.set, None, None)

    _ElementMap.update({
        __customer.name() : __customer,
        __terminal.name() : __terminal,
        __screenshot.name() : __screenshot
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'TerminalManager', TerminalManager)


# Complex type {http://xml.homeinfo.de/schema/termgr}Customer with content type ELEMENT_ONLY
class Customer (pyxb.binding.basis.complexTypeDefinition):
    """
                Terminal data for a certain customer
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Customer')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 27, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element terminal uses Python identifier terminal
    __terminal = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'terminal'), 'terminal', '__httpxml_homeinfo_deschematermgr_Customer_terminal', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 34, 12), )

    
    terminal = property(__terminal.value, __terminal.set, None, None)

    
    # Attribute cid uses Python identifier cid
    __cid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cid'), 'cid', '__httpxml_homeinfo_deschematermgr_Customer_cid', pyxb.binding.datatypes.integer, required=True)
    __cid._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 36, 8)
    __cid._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 36, 8)
    
    cid = property(__cid.value, __cid.set, None, '\n                    The customer identifier\n                ')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpxml_homeinfo_deschematermgr_Customer_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 43, 8)
    __name._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 43, 8)
    
    name = property(__name.value, __name.set, None, "\n                    The customer's full name\n                ")

    _ElementMap.update({
        __terminal.name() : __terminal
    })
    _AttributeMap.update({
        __cid.name() : __cid,
        __name.name() : __name
    })
Namespace.addCategoryObject('typeBinding', 'Customer', Customer)


# Complex type {http://xml.homeinfo.de/schema/termgr}Terminal with content type ELEMENT_ONLY
class Terminal (pyxb.binding.basis.complexTypeDefinition):
    """
                Terminal information
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Terminal')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 54, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element status uses Python identifier status
    __status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'status'), 'status', '__httpxml_homeinfo_deschematermgr_Terminal_status', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 61, 12), )

    
    status = property(__status.value, __status.set, None, None)

    
    # Element ipv4addr uses Python identifier ipv4addr
    __ipv4addr = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ipv4addr'), 'ipv4addr', '__httpxml_homeinfo_deschematermgr_Terminal_ipv4addr', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 62, 12), )

    
    ipv4addr = property(__ipv4addr.value, __ipv4addr.set, None, None)

    
    # Element uptime uses Python identifier uptime
    __uptime = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'uptime'), 'uptime', '__httpxml_homeinfo_deschematermgr_Terminal_uptime', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 63, 12), )

    
    uptime = property(__uptime.value, __uptime.set, None, None)

    
    # Element screenshot uses Python identifier screenshot
    __screenshot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'screenshot'), 'screenshot', '__httpxml_homeinfo_deschematermgr_Terminal_screenshot', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 64, 12), )

    
    screenshot = property(__screenshot.value, __screenshot.set, None, None)

    
    # Element touch_event uses Python identifier touch_event
    __touch_event = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'touch_event'), 'touch_event', '__httpxml_homeinfo_deschematermgr_Terminal_touch_event', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 65, 12), )

    
    touch_event = property(__touch_event.value, __touch_event.set, None, None)

    
    # Attribute tid uses Python identifier tid
    __tid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'tid'), 'tid', '__httpxml_homeinfo_deschematermgr_Terminal_tid', pyxb.binding.datatypes.integer, required=True)
    __tid._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 67, 8)
    __tid._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 67, 8)
    
    tid = property(__tid.value, __tid.set, None, '\n                    The terminal identifier\n                ')

    _ElementMap.update({
        __status.name() : __status,
        __ipv4addr.name() : __ipv4addr,
        __uptime.name() : __uptime,
        __screenshot.name() : __screenshot,
        __touch_event.name() : __touch_event
    })
    _AttributeMap.update({
        __tid.name() : __tid
    })
Namespace.addCategoryObject('typeBinding', 'Terminal', Terminal)


# Complex type {http://xml.homeinfo.de/schema/termgr}Screenshot with content type SIMPLE
class Screenshot (pyxb.binding.basis.complexTypeDefinition):
    """
                A screen shot of a terminal
            """
    _TypeDefinition = pyxb.binding.datatypes.base64Binary
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Screenshot')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 78, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.base64Binary
    
    # Attribute timestamp uses Python identifier timestamp
    __timestamp = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'timestamp'), 'timestamp', '__httpxml_homeinfo_deschematermgr_Screenshot_timestamp', pyxb.binding.datatypes.dateTime, required=True)
    __timestamp._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 86, 16)
    __timestamp._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 86, 16)
    
    timestamp = property(__timestamp.value, __timestamp.set, None, '\n                            The time, when the screenshot was taken\n                        ')

    
    # Attribute mimetype uses Python identifier mimetype
    __mimetype = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'mimetype'), 'mimetype', '__httpxml_homeinfo_deschematermgr_Screenshot_mimetype', pyxb.binding.datatypes.string, required=True)
    __mimetype._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 93, 16)
    __mimetype._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 93, 16)
    
    mimetype = property(__mimetype.value, __mimetype.set, None, "\n                            The screenshot picture's mime type\n                        ")

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __timestamp.name() : __timestamp,
        __mimetype.name() : __mimetype
    })
Namespace.addCategoryObject('typeBinding', 'Screenshot', Screenshot)


# Complex type {http://xml.homeinfo.de/schema/termgr}TouchEvent with content type SIMPLE
class TouchEvent (pyxb.binding.basis.complexTypeDefinition):
    """
                Touch input event
            """
    _TypeDefinition = pyxb.binding.datatypes.dateTime
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TouchEvent')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 106, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.dateTime
    
    # Attribute x uses Python identifier x
    __x = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'x'), 'x', '__httpxml_homeinfo_deschematermgr_TouchEvent_x', pyxb.binding.datatypes.integer, required=True)
    __x._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 114, 16)
    __x._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 114, 16)
    
    x = property(__x.value, __x.set, None, '\n                            The x-coordinate of the touch event\n                        ')

    
    # Attribute y uses Python identifier y
    __y = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'y'), 'y', '__httpxml_homeinfo_deschematermgr_TouchEvent_y', pyxb.binding.datatypes.integer, required=True)
    __y._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 121, 16)
    __y._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 121, 16)
    
    y = property(__y.value, __y.set, None, '\n                            The y-coordinate of the touch event\n                        ')

    
    # Attribute duration uses Python identifier duration
    __duration = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'duration'), 'duration', '__httpxml_homeinfo_deschematermgr_TouchEvent_duration', pyxb.binding.datatypes.integer)
    __duration._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 128, 16)
    __duration._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 128, 16)
    
    duration = property(__duration.value, __duration.set, None, '\n                            The duration of the touch event\n                        ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __x.name() : __x,
        __y.name() : __y,
        __duration.name() : __duration
    })
Namespace.addCategoryObject('typeBinding', 'TouchEvent', TouchEvent)


# Complex type {http://xml.homeinfo.de/schema/termgr}Message with content type ELEMENT_ONLY
class Message (pyxb.binding.basis.complexTypeDefinition):
    """
                Messages
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Message')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 141, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element text uses Python identifier text
    __text = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'text'), 'text', '__httpxml_homeinfo_deschematermgr_Message_text', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 148, 12), )

    
    text = property(__text.value, __text.set, None, "\n                        The messages' body or content\n                    ")

    
    # Attribute code uses Python identifier code
    __code = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'code'), 'code', '__httpxml_homeinfo_deschematermgr_Message_code', pyxb.binding.datatypes.integer, required=True)
    __code._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 156, 8)
    __code._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 156, 8)
    
    code = property(__code.value, __code.set, None, '\n                    A unique message code\n                ')

    _ElementMap.update({
        __text.name() : __text
    })
    _AttributeMap.update({
        __code.name() : __code
    })
Namespace.addCategoryObject('typeBinding', 'Message', Message)


# Complex type {http://xml.homeinfo.de/schema/termgr}Text with content type SIMPLE
class Text (pyxb.binding.basis.complexTypeDefinition):
    """
                Localized text string
            """
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Text')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 167, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'lang'), 'lang', '__httpxml_homeinfo_deschematermgr_Text_lang', pyxb.binding.datatypes.string, required=True)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 175, 16)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 175, 16)
    
    lang = property(__lang.value, __lang.set, None, '\n                            The language of the text\n                        ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
Namespace.addCategoryObject('typeBinding', 'Text', Text)


termgr = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'termgr'), TerminalManager, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 8, 4))
Namespace.addCategoryObject('elementBinding', termgr.name().localName(), termgr)



TerminalManager._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'customer'), Customer, scope=TerminalManager, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 19, 12)))

TerminalManager._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'terminal'), Terminal, scope=TerminalManager, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 20, 12)))

TerminalManager._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'screenshot'), Screenshot, scope=TerminalManager, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 21, 12)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TerminalManager._UseForTag(pyxb.namespace.ExpandedName(None, 'customer')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 19, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TerminalManager._UseForTag(pyxb.namespace.ExpandedName(None, 'terminal')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 20, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TerminalManager._UseForTag(pyxb.namespace.ExpandedName(None, 'screenshot')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 21, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
TerminalManager._Automaton = _BuildAutomaton()




Customer._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'terminal'), Terminal, scope=Customer, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 34, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Customer._UseForTag(pyxb.namespace.ExpandedName(None, 'terminal')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 34, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Customer._Automaton = _BuildAutomaton_()




Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'status'), TerminalStatus, scope=Terminal, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 61, 12)))

Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ipv4addr'), IPv4Address, scope=Terminal, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 62, 12)))

Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'uptime'), pyxb.binding.datatypes.unsignedLong, scope=Terminal, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 63, 12)))

Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'screenshot'), Screenshot, scope=Terminal, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 64, 12)))

Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'touch_event'), TouchEvent, scope=Terminal, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 65, 12)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 65, 12))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'status')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 61, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'ipv4addr')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 62, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'uptime')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 63, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'screenshot')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 64, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'touch_event')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 65, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
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
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Terminal._Automaton = _BuildAutomaton_2()




Message._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'text'), Text, scope=Message, documentation="\n                        The messages' body or content\n                    ", location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 148, 12)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Message._UseForTag(pyxb.namespace.ExpandedName(None, 'text')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/termgr/doc/termgr.xsd', 148, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Message._Automaton = _BuildAutomaton_3()

