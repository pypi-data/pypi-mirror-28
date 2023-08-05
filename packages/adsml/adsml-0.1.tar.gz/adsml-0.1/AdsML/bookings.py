#!/usr/bin/env python

import xml.etree.ElementTree as etree
import sys
import io

from .core import ADSML_NS, ADSMLBOOKINGS_NS, ADSMLBOOKINGS_NS_RAW
from .order import AdsMLOrder
from .header import AdsMLHeader


class AdsMLBooking(object):
    transmission_id = None
    systems_id = None
    administrative_response_required = None
    send_count = None
    transmission_sequence = None
    transmission_status = None
    transmission_date_time = None
    first_transmission_date_time = None
    schema_version = None
    header = None
    order = None

    def __init__(self, xmlelement=None, **kwargs):
        self.header = AdsMLHeader()
        self.order = AdsMLOrder()
        if kwargs:
            if 'transmissionID' in kwargs:
                self.transmission_id = kwargs['transmissionID']
            if 'systemsID' in kwargs:
                self.systems_id = kwargs['systemsID']
            if 'administrativeResponseRequired' in kwargs:
                self.administrative_response_required = kwargs['administrativeResponseRequired']
            if 'sendCount' in kwargs:
                self.send_count = kwargs['sendCount']
            if 'transmissionSequence' in kwargs:
                self.transmission_sequence = kwargs['transmissionSequence']
            if 'transmissionStatus' in kwargs:
                self.transmission_status = kwargs['transmissionStatus']
            if 'transmissionDateTime' in kwargs:
                self.transmission_date_time = kwargs['transmissionDateTime']
            if 'firstTransmissionDateTime' in kwargs:
                self.first_transmission_date_time = kwargs['firstTransmissionDateTime']
            if 'schemaVersion' in kwargs:
                self.schema_version = kwargs['schemaVersion']
        
    def __str__(self):
        return str(self.order)

    def to_xml(self):
        xml_object = etree.Element(ADSMLBOOKINGS_NS+'AdsMLBookings')

        if self.transmission_id:
            xml_object.attrib[ADSML_NS+'transmissionID'] = self.transmission_id
        if self.systems_id:
            xml_object.attrib[ADSML_NS+'systemsID'] = self.systems_id
        if self.administrative_response_required:
            xml_object.attrib[ADSML_NS+'administrativeResponseRequired'] = 'true' if self.administrative_response_required else 'false'
        if self.send_count:
            xml_object.attrib[ADSML_NS+'sendCount'] = str(self.send_count)
        if self.transmission_sequence:
            xml_object.attrib[ADSML_NS+'transmissionSequence'] = str(self.transmission_sequence)
        if self.transmission_status:
            xml_object.attrib[ADSML_NS+'transmissionStatus'] = self.transmission_status
        if self.transmission_date_time:
            xml_object.attrib[ADSML_NS+'transmissionDateTime'] = self.transmission_date_time.isoformat()
        if self.first_transmission_date_time:
            xml_object.attrib[ADSML_NS+'firstTransmissionDateTime'] = self.first_transmission_date_time.isoformat()
        if self.schema_version:
            xml_object.attrib[ADSML_NS+'schemaVersion'] = self.schema_version

        xml_object.append(self.header.to_xml())
        xml_object.append(self.order.to_xml())
        tree = etree.ElementTree(xml_object)
        output_string = io.StringIO()
        tree.write(
            output_string,
            xml_declaration=True,
            # write to stdout doesn't work without this...
            # I had to read the Python source code to work it out!
            encoding='unicode',
            method='xml',
            default_namespace=ADSMLBOOKINGS_NS_RAW
        )
        return output_string.getvalue()

    def set_order(self, order):
        self.order = order

    def set_header(self, header):
        self.header = header
