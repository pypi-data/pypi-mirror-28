#!/usr/bin/env python

import xml.etree.ElementTree as etree
from .core import ADSML_NS
from .party import AdsMLParty


class AdsMLHeader(object):
    transmission_from = None
    transmission_to = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.transmission_from = AdsMLParty(xmlelement.find(ADSML_NS+'TransmissionFrom'))
            self.transmission_to = AdsMLParty(xmlelement.find(ADSML_NS+'TransmissionTo'))
        elif kwargs:
            if 'transmission_from' in kwargs:
                self.set_transmission_from(kwargs['transmission_from'])
            if 'transmission_to' in kwargs:
                self.set_transmission_to(kwargs['transmission_to'])

    def set_transmission_from(self, from_party):
        self.transmission_from = from_party

    def set_transmission_to(self, to_party):
        self.transmission_to = to_party

    def __str__(self):
        return (
            '<AdsMLHeader from ' +
            str(self.transmission_from) +
            ' to ' +
            str(self.transmission_to) +
            '>'
        )

    def to_xml(self):
        xml_object = etree.Element(ADSML_NS+'Header')
        xml_object.append(self.transmission_from.to_xml(element_name='TransmissionFrom'))
        xml_object.append(self.transmission_to.to_xml(element_name='TransmissionTo'))
        return xml_object
