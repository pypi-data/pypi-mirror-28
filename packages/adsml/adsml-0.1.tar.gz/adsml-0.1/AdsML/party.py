#!/usr/bin/env python

import xml.etree.ElementTree as etree
from .core import ADSML_NS

class AdsMLParty(object):
    name = None
    id_label = None
    id_value = None
    address = None
    contact = None
    xml_element = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.name = xmlelement.findtext(ADSML_NS+'Name')
            identifier_element = xmlelement.find(ADSML_NS+'Identifier')
            if identifier_element:
                self.read_identifier(identifier_element)
            party_address_element = xmlelement.find(ADSML_NS+'PartyAddress')
            if party_address_element:
                address = AdsMLPartyAddress(party_address_element)
            contact_element = xmlelement.find(ADSML_NS+'Contact')
            if contact_element:
                contact = AdsMLPartyAddress(contact_element)
        elif kwargs:
            if 'name' in kwargs:
                self.name = kwargs['name']
            if 'id_label' in kwargs:
                self.id_label = kwargs['id_label']
            if 'id_value' in kwargs:
                self.id_value = kwargs['id_value']
            if 'address' in kwargs:
                self.address = kwargs['address']
            if 'contact' in kwargs:
                self.contact = kwargs['contact']
            return
        
    def read_identifier(self, idelement):
        self.id_label = idelement.findtext(ADSML_NS+'IDLabel')
        self.id_value = idelement.findtext(ADSML_NS+'IDValue')

    def identifier_to_xml(self):
        identifier_object = etree.Element(ADSML_NS+'Identifier')
        id_label_object = etree.Element(ADSML_NS+'IDLabel')
        id_label_object.text = self.id_label
        id_value_object = etree.Element(ADSML_NS+'IDValue')
        id_value_object.text = self.id_value
        identifier_object.append(id_label_object)
        identifier_object.append(id_value_object)
        return identifier_object
       
    def to_xml(self, element_name='AdsMLParty'):
        xml_object = etree.Element(ADSML_NS+element_name)
        if self.id_label and self.id_value:
            xml_object.append(self.identifier_to_xml())
        if self.name:
            name_object = etree.Element(ADSML_NS+'Name')
            name_object.text = self.name
            xml_object.append(name_object)

        return xml_object

    def __str__(self):
        return '<AdsMLParty '+self.name+'>'


class AdsMLPartyAddress(object):
    physical_address = None
    street = None
    zip_postal_code = None
    city = None
    phone = None
    phone_type = None
    phone_number = None
    email = None
    email_address = None

    def __init__(self, xmlelement):
        self.physical_address = xmlelement.find(
            ADSML_NS+'CommunicationChannel.PhysicalAddress'
        )
        if self.physical_address:
            self.street = self.physical_address.findtext(
                ADSML_NS+'Street'
            )
            self.zip_postal_code = self.physical_address.findtext(
                ADSML_NS+'ZipPostalCode'
            )
            self.city = self.physical_address.findtext(
                ADSML_NS+'City'
            )
        self.phone = xmlelement.find(
            ADSML_NS+'CommunicationChannel.Phone'
        )
        if self.phone:
            self.phone_type = self.phone.findtext(
                ADSML_NS+'Type'
            )
            self.phone_number = self.phone.findtext(
                ADSML_NS+'PhoneNumber'
            )
        self.email = xmlelement.find(
            ADSML_NS+'CommunicationChannel.EMail'
        )
        if self.email:
            self.email_address = self.email.findtext(
                ADSML_NS+'EMailAddress'
            )
