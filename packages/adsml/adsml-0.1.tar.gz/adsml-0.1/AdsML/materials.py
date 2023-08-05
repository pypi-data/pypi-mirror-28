#!/usr/bin/env python

import xml.etree.ElementTree as etree
from .core import ADSML_NS, ADSMLMA_NS
from .party import AdsMLParty


class AdsMLAdContent(object):
    materials_identifier = None
    description_line = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.materials_identifier = xmlelement.findtext(ADSMLMA_NS+'MaterialsIdentifier')
            self.description_line = xmlelement.findtext(ADSML_NS+'DescriptionLine')

    def to_xml(self):
        xml_object = etree.Element(ADSMLMA_NS+'AdContent')
        return xml_object

    def __str__(self):
        return '<AdsMLAdContent '+self.materials_identifier+' ('+self.description_line+')>'


class AdsMLMaterialsExpectations(object):
    materials_provider_party = None
    
    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.materials_identifier_party = AdsMLParty(
                xmlelement.find(ADSMLMA_NS+'MaterialsProviderParty')
            )

    def to_xml(self):
        xml_object = etree.Element(ADSMLMA_NS+'MaterialsExpectations')
        return xml_object

    def __str__(self):
        return '<AdsMLMaterialsExpectations ' + self.materials_provider_party + ')>'
