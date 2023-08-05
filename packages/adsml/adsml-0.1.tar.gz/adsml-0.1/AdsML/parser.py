#!/usr/bin/env python

import xml.etree.ElementTree as etree

from .core import ADSMLBOOKINGS_NS, ADSML_NS
from .header import AdsMLHeader
from .order import AdsMLOrder

class AdsMLParser(object):
    _root_element = None
    header = None
    order = None

    def __init__(self, filename):
        if type(filename) == str:
            tree = etree.parse(filename)
            self._root_element = tree.getroot()
            self.header = AdsMLHeader(self._root_element.find(ADSML_NS+'Header'))
            self.order = AdsMLOrder(self._root_element.find(ADSMLBOOKINGS_NS+'AdOrder'))
        else:
            raise Exception("filename should be a string")

    def get_header(self):
        return self.header

    def get_order(self):
        return self.order
