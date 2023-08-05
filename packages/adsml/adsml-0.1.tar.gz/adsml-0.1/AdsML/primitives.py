#!/usr/bin/env python

import xml.etree.ElementTree as etree
from AdsML import ADSML_NS, ADSMLBOOKINGS_NS


class AdsMLCodeValue(object):
    code_value = None
    # description = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.name_codevalue = xmlemement.find(ADSML_NS+'CodeValue')
            # self.name_description = xmlemement.find(ADSML_NS+'Description')
        elif kwargs:
            if 'code_value' in kwargs:
                self.code_value = kwargs['code_value']

    def to_xml(self):
        xml_object = etree.Element(ADSML_NS+'CodeValue')
        xml_object.text = self.code_value
        return xml_object
        
    def __str__(self):
        return '<AdsMLCodeValue '+ self.code_value + '>'


class AdsMLValueWithUnits(object):
    unit_of_measure = None
    value = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.unit_of_measure = AdsMLSize(xmlelement.find(ADSML_NS+'UnitOfMeasure'))
            self.value = AdsMLColors(xmlelement.find(ADSML_NS+'Value'))
        elif kwargs:
            if 'unit_of_measure' in kwargs:
                self.unit_of_measure = kwargs['unit_of_measure']
            if 'value' in kwargs:
                self.value = kwargs['value']

    def to_xml(self, element_name=None):
        xml_object = etree.Element(ADSMLBOOKINGS_NS+element_name)
        unit_of_measure_object = etree.Element(ADSML_NS+'UnitOfMeasure')
        unit_of_measure_object.text = self.unit_of_measure
        xml_object.append(unit_of_measure_object)
        value_object = etree.Element(ADSML_NS+'Value')
        value_object.text = self.value
        xml_object.append(value_object)
        return xml_object
        
    def __str__(self):
        return self.value + ' ' + self.unit_of_measure
