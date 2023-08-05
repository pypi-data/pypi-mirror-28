# -*- coding: utf-8 -*-
#
# Copyright (c), 2016-2017, SISSA (International School for Advanced Studies).
# All rights reserved.
# This file is distributed under the terms of the MIT License.
# See the file 'LICENSE' in the root directory of the present
# distribution, or http://opensource.org/licenses/MIT.
#
# @author Davide Brunato <brunato@sissa.it>
#
"""
This module contains classes for XML Schema elements, complex types and model groups.
"""
from collections import Sequence

from ..core import etree_element, ElementData
from ..exceptions import XMLSchemaValidationError, XMLSchemaAttributeError, XMLSchemaParseError
from ..qnames import (
    XSD_GROUP_TAG, XSD_SEQUENCE_TAG, XSD_ALL_TAG, XSD_CHOICE_TAG, XSD_ATTRIBUTE_GROUP_TAG,
    XSD_COMPLEX_TYPE_TAG, XSD_ELEMENT_TAG, get_qname, XSD_ANY_TYPE, XSD_SIMPLE_TYPE_TAG,
    local_name, reference_to_qname, XSD_UNIQUE_TAG, XSD_KEY_TAG, XSD_KEYREF_TAG
)
from ..xpath import XPathMixin
from ..utils import check_type
from ..xsdbase import (
    get_xsd_attribute, get_xsd_bool_attribute, get_xsd_derivation_attribute, ValidatorMixin
)
from .component import XsdAnnotated, ParticleMixin
from .simple_types import XsdSimpleType
from .complex_types import XsdComplexType
from .constraints import XsdUnique, XsdKey, XsdKeyref


XSD_MODEL_GROUP_TAGS = {XSD_GROUP_TAG, XSD_SEQUENCE_TAG, XSD_ALL_TAG, XSD_CHOICE_TAG}


class XsdElement(Sequence, XsdAnnotated, ValidatorMixin, ParticleMixin, XPathMixin):
    """
    Class for XSD 1.0 'element' declarations.
    
    <element
      abstract = boolean : false
      block = (#all | List of (extension | restriction | substitution))
      default = string
      final = (#all | List of (extension | restriction))
      fixed = string
      form = (qualified | unqualified)
      id = ID
      maxOccurs = (nonNegativeInteger | unbounded)  : 1
      minOccurs = nonNegativeInteger : 1
      name = NCName
      nillable = boolean : false
      ref = QName
      substitutionGroup = QName
      type = QName
      {any attributes with non-schema namespace . . .}>
      Content: (annotation?, ((simpleType | complexType)?, (unique | key | keyref)*))
    </element>
    """
    def __init__(self, elem, schema, name=None, is_global=False):
        super(XsdElement, self).__init__(elem, schema, name, is_global)
        if not hasattr(self, 'type'):
            raise XMLSchemaAttributeError("undefined 'type' attribute for %r." % self)
        if not hasattr(self, 'qualified'):
            raise XMLSchemaAttributeError("undefined 'qualified' attribute for %r." % self)

    def __getitem__(self, i):
        try:
            return self.type.content_type.elements[i]
        except (AttributeError, IndexError):
            raise IndexError('child index out of range')
        except TypeError:
            content_type = self.type.content_type
            content_type.elements = [e for e in content_type.iter_elements()]
            try:
                content_type.elements[i]
            except IndexError:
                raise IndexError('child index out of range')

    def __len__(self):
        try:
            return len(self.type.content_type.elements)
        except AttributeError:
            return 0
        except TypeError:
            content_type = self.type.content_type
            content_type.elements = [e for e in content_type.iter_elements()]

    def __setattr__(self, name, value):
        if name == "type":
            check_type(value, XsdSimpleType, XsdComplexType)
            try:
                self.attributes = value.attributes
            except AttributeError:
                self.attributes = self.BUILDERS.attribute_group_class(
                    etree_element(XSD_ATTRIBUTE_GROUP_TAG), schema=self.schema
                )
        super(XsdElement, self).__setattr__(name, value)

    def _parse(self):
        super(XsdElement, self)._parse()
        self._parse_particle()

        elem = self.elem
        self.name = None

        if self.default and self.fixed:
            self._parse_error("'default' and 'fixed' attributes are mutually exclusive", self)
        self._parse_properties('abstract', 'block', 'final', 'form', 'nillable')

        # Parse element attributes
        try:
            element_name = reference_to_qname(elem.attrib['ref'], self.namespaces)
        except KeyError:
            # No 'ref' attribute ==> 'name' attribute required.
            try:
                self.name = get_qname(self.target_namespace, elem.attrib['name'])
            except KeyError:
                self._parse_error("invalid element declaration in XSD schema", elem)
            self.qualified = self.elem.get('form', self.schema.element_form_default) == 'qualified'
            if self.is_global:
                if 'minOccurs' in elem.attrib:
                    self._parse_error(
                        "attribute 'minOccurs' not allowed for a global element", self
                    )
                if 'maxOccurs' in elem.attrib:
                    self._parse_error(
                        "attribute 'maxOccurs' not allowed for a global element", self
                    )
        else:
            # Reference to a global element
            if self.is_global:
                self._parse_error("an element reference can't be global", elem)
            msg = "attribute %r is not allowed when element reference is used"
            if 'name' in elem.attrib:
                self._parse_error(msg % 'name', elem)
            elif 'type' in elem.attrib:
                self._parse_error(msg % 'type', elem)
            xsd_element = self.maps.lookup_element(element_name)
            self.name = xsd_element.name
            self.type = xsd_element.type
            self.qualified = xsd_element.qualified

        skip = 0
        if self.ref:
            if self._parse_component(elem, required=False, strict=False) is not None:
                self._parse_error("element reference declaration can't has children", elem)
        elif 'type' in elem.attrib:
            type_qname = reference_to_qname(elem.attrib['type'], self.namespaces)
            try:
                self.type = self.maps.lookup_type(type_qname)
            except KeyError:
                self._parse_error('unknown type %r' % elem.attrib['type'], elem)
                self.type = self.maps.lookup_type(XSD_ANY_TYPE)
        else:
            child = self._parse_component(elem, required=False, strict=False)
            if child is not None:
                if child.tag == XSD_COMPLEX_TYPE_TAG:
                    self.type = self.BUILDERS.complex_type_class(child, self.schema)
                elif child.tag == XSD_SIMPLE_TYPE_TAG:
                    self.type = self.BUILDERS.simple_type_factory(child, self.schema)
                skip = 1
            else:
                self.type = self.maps.lookup_type(XSD_ANY_TYPE)

        self.constraints = {}
        for child in self._iterparse_components(elem, start=skip):
            if child.tag == XSD_UNIQUE_TAG:
                constraint = XsdUnique(child, self.schema, parent=self)
            elif child.tag == XSD_KEY_TAG:
                constraint = XsdKey(child, self.schema, parent=self)
            elif child.tag == XSD_KEYREF_TAG:
                constraint = XsdKeyref(child, self.schema, parent=self)
            else:
                raise XMLSchemaParseError(
                    "unexpected child element %r:" % child, self)

            try:
                if child != self.maps.constraints[constraint.name]:
                    self._parse_error("duplicated identity constraint %r:" % constraint.name, child)
            except KeyError:
                self.maps.constraints[constraint.name] = child
            finally:
                self.constraints[constraint.name] = constraint

        self._parse_substitution_group()

    def _parse_substitution_group(self):
        substitution_group = self.substitution_group
        if substitution_group is None:
            return

        if not self.is_global:
            self._parse_error("'substitutionGroup' attribute in a local element declaration")

        qname = reference_to_qname(substitution_group, self.namespaces)
        if qname[0] != '{':
            qname = get_qname(self.target_namespace, qname)
        try:
            head_element = self.maps.lookup_element(qname)
        except KeyError:
            self._parse_error("unknown substitutionGroup %r" % substitution_group)
        else:
            final = head_element.final
            if final is None:
                final = self.schema.final_default

            if final == '#all' or 'extension' in final and 'restriction' in final:
                self._parse_error("head element %r cannot be substituted." % head_element)
            elif self.type == head_element.type or self.type.name == XSD_ANY_TYPE:
                pass
            elif 'extension' in final and not self.type.is_derived(head_element.type, 'extension'):
                self._parse_error(
                    "%r type is not of the same or an extension of the head element %r type."
                    % (self, head_element)
                )
            elif 'restriction' in final and not self.type.is_derived(head_element.type, 'restriction'):
                self._parse_error(
                    "%r type is not of the same or a restriction of the head element %r type."
                    % (self, head_element)
                )
            elif not self.type.is_derived(head_element.type):
                self._parse_error(
                    "%r type is not of the same or a derivation of the head element %r type."
                    % (self, head_element)
                )

    @property
    def built(self):
        return self.type.is_global or self.type.built

    @property
    def validation_attempted(self):
        if self.built:
            return 'full'
        else:
            return self.type.validation_attempted

    @property
    def admitted_tags(self):
        return {XSD_ELEMENT_TAG}

    @property
    def ref(self):
        return self.elem.get('ref')

    @property
    def abstract(self):
        return get_xsd_bool_attribute(self.elem, 'abstract', default=False)

    @property
    def block(self):
        return get_xsd_derivation_attribute(self.elem, 'block', ('extension', 'restriction', 'substitution'))

    @property
    def default(self):
        return self.elem.get('default', '')

    @property
    def final(self):
        return get_xsd_derivation_attribute(self.elem, 'final', ('extension', 'restriction'))

    @property
    def fixed(self):
        return self.elem.get('fixed', '')

    @property
    def form(self):
        return get_xsd_attribute(self.elem, 'form', ('qualified', 'unqualified'), default=None)

    @property
    def nillable(self):
        return get_xsd_bool_attribute(self.elem, 'nillable', default=False)

    @property
    def substitution_group(self):
        return self.elem.get('substitutionGroup')

    def iter_components(self, xsd_classes=None):
        if xsd_classes is None:
            yield self
            for obj in self.constraints.values():
                yield obj
        else:
            if isinstance(self, xsd_classes):
                yield self
            for obj in self.constraints.values():
                if isinstance(obj, xsd_classes):
                    yield obj

        if self.ref is None and not self.type.is_global:
            for obj in self.type.iter_components(xsd_classes):
                yield obj

    def match(self, name):
        return self.name == name or (not self.qualified and local_name(self.name) == name)

    def iter_decode(self, elem, validation='lax', **kwargs):
        """
        Generator method for decoding elements. A data structure is returned, eventually
        preceded by a sequence of validation or decode errors.
        """
        element_decode_hook = kwargs.get('element_decode_hook')
        if element_decode_hook is None:
            element_decode_hook = self.schema.get_converter().element_decode
            kwargs['element_decode_hook'] = element_decode_hook
        use_defaults = kwargs.get('use_defaults', False)

        if self.type.is_complex():
            if use_defaults and self.type.has_simple_content():
                kwargs['default'] = self.default
            for result in self.type.iter_decode(elem, validation, **kwargs):
                if isinstance(result, XMLSchemaValidationError):
                    if result.schema_elem is None:
                        if self.type.name is not None and self.target_namespace == self.type.target_namespace:
                            result.schema_elem = self.type.elem
                        else:
                            result.schema_elem = self.elem
                    if result.elem is None:
                        result.elem = elem
                    yield result
                else:
                    yield element_decode_hook(ElementData(elem.tag, *result), self)
                    del result
        else:
            if elem.attrib:
                err = XMLSchemaValidationError(self, elem, "a simpleType element can't has attributes.")
                if validation == 'strict':
                    raise err
                yield err

            if len(elem):
                err = XMLSchemaValidationError(self, elem, "a simpleType element can't has child elements.")
                if validation == 'strict':
                    raise err
                yield err

            if elem.text is None:
                yield None
            else:
                text = elem.text or self.default if use_defaults else elem.text
                for result in self.type.iter_decode(text, validation, **kwargs):
                    if isinstance(result, XMLSchemaValidationError):
                        if result.schema_elem is None:
                            if self.type.name is not None and \
                                            self.target_namespace == self.type.target_namespace:
                                result.schema_elem = self.type.elem
                            else:
                                result.schema_elem = self.elem
                        if result.elem is None:
                            result.elem = elem
                        if validation == 'strict':
                            raise result
                        yield result
                    else:
                        yield element_decode_hook(ElementData(elem.tag, result, None, None), self)
                        del result

        if validation != 'skip':
            for constraint in self.constraints.values():
                for error in constraint(elem):
                    if validation == 'strict':
                        raise error
                    else:
                        yield error

    def iter_encode(self, data, validation='lax', **kwargs):
        element_encode_hook = kwargs.get('element_encode_hook')
        if element_encode_hook is None:
            element_encode_hook = self.schema.get_converter().element_encode
            kwargs['element_encode_hook'] = element_encode_hook
        _etree_element = kwargs.get('etree_element') or etree_element

        level = kwargs.pop('level', 0)
        indent = kwargs.get('indent', None)
        tail = (u'\n' + u' ' * indent * level) if indent is not None else None

        element_data, errors = element_encode_hook(data, self, validation)
        for e in errors:
            if validation == 'strict':
                raise e
            yield e

        if self.type.is_complex():
            for result in self.type.iter_encode(element_data, validation, level=level + 1, **kwargs):
                if isinstance(result, XMLSchemaValidationError):
                    if result.schema_elem is None:
                        result.obj, result.schema_elem = data, self.elem
                    if validation == 'strict':
                        raise result
                    yield result
                else:
                    elem = _etree_element(self.name, attrib=dict(result.attributes))
                    elem.text = result.text
                    elem.extend(result.content)
                    elem.tail = tail
                    yield elem
        else:
            # Encode a simpleType
            if element_data.attributes:
                err = XMLSchemaValidationError(self, data, "a simpleType element can't has attributes.")
                if validation == 'strict':
                    raise err
                yield err
            if element_data.content:
                err = XMLSchemaValidationError(self, data, "a simpleType element can't has child elements.")
                if validation == 'strict':
                    raise err
                yield err

            if element_data.text is None:
                elem = _etree_element(self.name, attrib={})
                elem.text = None
                elem.tail = tail
                yield elem
            else:
                for result in self.type.iter_encode(element_data.text, validation, **kwargs):
                    if isinstance(result, XMLSchemaValidationError):
                        if result.elem is None:
                            result.obj, result.schema_elem = data, self.elem
                        if validation == 'strict':
                            raise result
                        yield result
                    else:
                        elem = _etree_element(self.name, attrib={})
                        elem.text = result
                        elem.tail = tail
                        yield elem
                        break

        del element_data

    def iter_decode_children(self, elem, index=0):
        model_occurs = 0
        while True:
            try:
                qname = get_qname(self.target_namespace, elem[index].tag)
            except IndexError:
                if model_occurs == 0 and self.min_occurs > 0:
                    yield XMLSchemaValidationError(self, elem, "tag %r expected." % self.name)
                else:
                    yield index
                return
            else:
                if qname == self.name or self.is_global and \
                        self.name in self.maps.substitution_group and \
                        any([qname == e.name for e in self.maps.substitution_groups[self.name]]):
                    yield self, elem[index]
                else:
                    if model_occurs == 0 and self.min_occurs > 0:
                        yield XMLSchemaValidationError(self, elem, "tag %r expected." % self.name)
                    else:
                        yield index
                    return

            index += 1
            model_occurs += 1
            if self.max_occurs is not None and model_occurs >= self.max_occurs:
                yield index
                return

    def get_attribute(self, name):
        if name[0] != '{':
            return self.type.attributes[get_qname(self.type.target_namespace, name)]
        return self.type.attributes[name]

    def iter(self, tag=None):
        if tag is None or self.name == tag:
            yield self
        try:
            for xsd_element in self.type.content_type.iter_elements():
                if xsd_element.ref is None:
                    for e in xsd_element.iter(tag):
                        yield e
                elif tag is None or xsd_element.name == tag:
                    yield xsd_element
        except (TypeError, AttributeError):
            return

    def iterchildren(self, tag=None):
        try:
            for xsd_element in self.type.content_type.iter_elements():
                if tag is None or xsd_element.match(tag):
                    yield xsd_element
        except (TypeError, AttributeError):
            return


class Xsd11Element(XsdElement):
    """
    Class for XSD 1.1 'element' declarations.

    <element
      abstract = boolean : false
      block = (#all | List of (extension | restriction | substitution))
      default = string
      final = (#all | List of (extension | restriction))
      fixed = string
      form = (qualified | unqualified)
      id = ID
      maxOccurs = (nonNegativeInteger | unbounded)  : 1
      minOccurs = nonNegativeInteger : 1
      name = NCName
      nillable = boolean : false
      ref = QName
      substitutionGroup = List of QName
      targetNamespace = anyURI
      type = QName
      {any attributes with non-schema namespace . . .}>
      Content: (annotation?, ((simpleType | complexType)?, alternative*, (unique | key | keyref)*))
    </element>
    """
    pass
