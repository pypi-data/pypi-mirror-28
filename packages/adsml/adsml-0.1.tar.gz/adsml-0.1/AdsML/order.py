#!/usr/bin/env python

import xml.etree.ElementTree as etree
from .core import ADSMLBOOKINGS_NS, ADSML_NS
from .party import AdsMLParty
from .placement import AdsMLPlacement


class AdsMLOrder(object):
    message_code = None
    message_id = None
    message_class = None
    message_assembled_time = None
    booking_identifier = None
    buyers_reference = None
    booking_party = None
    selling_party = None
    campaign = None
    payer_information = None
    placement_newspaper = None
    placement_interactive = None
    notes = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            if 'messageCode' in xmlelement.attrib:
                self.message_code = xmlelement.attrib['messageCode']
            if ADSML_NS+'messageID' in xmlelement.attrib:
                self.message_id = xmlelement.attrib[ADSML_NS+'messageID']
            if ADSML_NS+'messageClass' in xmlelement.attrib:
                self.message_class = xmlelement.attrib[ADSML_NS+'messageClass']
            if ADSML_NS+'messageAssembledTime' in xmlelement.attrib:
                self.message_assembled_time = xmlelement.attrib[ADSML_NS+'messageAssembledTime']
            self.booking_identifier = xmlelement.findtext(
                ADSMLBOOKINGS_NS+'BookingIdentifier'
            )
            auxiliary_booking_references_element = xmlelement.find(
                ADSMLBOOKINGS_NS+'AuxiliaryBookingReferences'
            )
            self.buyers_reference = auxiliary_booking_references_element.findtext(
                ADSML_NS+'BuyersReference'
            )
            self.booking_party = AdsMLParty(xmlelement.find(ADSML_NS+'BookingParty'))
            self.selling_party = AdsMLParty(xmlelement.find(ADSML_NS+'SellingParty'))
            self.campaign = AdsMLCampaign(xmlelement.find(ADSML_NS+'Campaign'))
            self.payer_information = AdsMLPayerInformation(xmlelement.find(ADSMLBOOKINGS_NS+'PayerInformation'))
            self.placement_newspaper = AdsMLPlacement(xmlelement.find(ADSMLBOOKINGS_NS+'Placement.NewspaperMagazine'))
            self.placement_interactive = AdsMLPlacement(xmlelement.find(ADSMLBOOKINGS_NS+'Placement.Interactive'))
            self.notes = AdsMLNotes(xmlelement.find(ADSML_NS+'Notes'))
        elif kwargs:
            if 'messageCode' in kwargs:
                self.message_code = kwargs['messageCode']
            if 'messageID' in kwargs:
                self.message_id = kwargs['messageID']
            if 'messageClass' in kwargs:
                self.message_class = kwargs['messageClass']
            if 'bookingIdentifier' in kwargs:
                self.booking_identifier = kwargs['bookingIdentifier']
            if 'buyersReference' in kwargs:
                self.buyers_reference = kwargs['buyersReference']

    def set_booking_party(self, booking_party):
        if type(booking_party) == AdsMLParty:
            self.booking_party = booking_party

    def set_selling_party(self, selling_party):
        if type(selling_party) == AdsMLParty:
            self.selling_party = selling_party

    def set_campaign(self, campaign):
        if type(campaign) == AdsMLCampaign:
            self.campaign = campaign
            
    def set_payer_information(self, payer_information):
        if type(payer_information) == AdsMLPayerInformation:
            self.payer_information = payer_information
            
    def set_placement_newspaper(self, placement_newspaper):
        if type(placement_newspaper) == AdsMLPlacement:
            self.placement_newspaper = placement_newspaper
            
    def set_placement_interactive(self, placement_interactive):
        if type(placement_interactive) == AdsMLPlacement:
            self.placement_interactive = placement_interactive
            
    def set_notes(self, notes):
        if type(notes) == AdsMLNotes:
            self.notes = notes
            
    def to_xml(self):
        xml_object = etree.Element(ADSMLBOOKINGS_NS+'AdOrder')
        if self.message_code:
            xml_object.attrib[ADSMLBOOKINGS_NS+'messageCode'] = self.message_code
        if self.message_id:
            xml_object.attrib[ADSML_NS+'messageID'] = self.message_id
        if self.message_class:
            xml_object.attrib[ADSML_NS+'messageClass'] = self.message_class
        if self.booking_identifier:
            booking_identifier_object = etree.Element(ADSMLBOOKINGS_NS+'BookingIdentifier')
            booking_identifier_object.text = self.booking_identifier
            xml_object.append(booking_identifier_object)
        if self.buyers_reference:
            auxiliary_booking_references_object = etree.Element(ADSMLBOOKINGS_NS+'AuxiliaryBookingReferences')
            buyers_reference_object = etree.Element(ADSML_NS+'BuyersReference')
            buyers_reference_object.text = self.buyers_reference
            auxiliary_booking_references_object.append(buyers_reference_object)
            xml_object.append(auxiliary_booking_references_object)
        if self.booking_party:
            xml_object.append(self.booking_party.to_xml(element_name='BookingParty'))
        if self.selling_party:
            xml_object.append(self.selling_party.to_xml(element_name='SellingParty'))
        if self.campaign:
            xml_object.append(self.campaign.to_xml())
        if self.payer_information:
            xml_object.append(self.payer_information.to_xml())
        if self.placement_newspaper:
            xml_object.append(self.placement_newspaper.to_xml(element_name='Placement.NewspaperMagazine'))
        if self.placement_interactive:
            xml_object.append(self.placement_interactive.to_xml(element_name='Placement.Interactive'))
        if self.notes:
            xml_object.append(self.notes.to_xml())
            
        return xml_object

    def __str__(self):
        return '<AdsMLOrder '+str(self.booking_identifier)+'>'


class AdsMLCampaign(object):
    campaign_code = None
    description = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.campaign_code = xmlelement.findtext(ADSML_NS+'CodeValue')
            description = xmlelement.findtext(ADSML_NS+'Description')
        elif kwargs:
            if 'code' in kwargs:
                self.campaign_code = kwargs['code']
            if 'description' in kwargs:
                self.description = kwargs['description']
        else:
            return

    def to_xml(self):
        campaign_object = etree.Element(ADSML_NS+'Campaign')
        code_value_object = etree.Element(ADSML_NS+'CodeValue')
        code_value_object.text = self.campaign_code
        campaign_object.append(code_value_object)
        if self.description:
            description_object = etree.Element(ADSML_NS+'Description')
            description_object.text = self.description
            campaign_object.append(description_object)
        return campaign_object
        
    def __str__(self):
        return '<AdsMLCampaign '+str(self.campaign_code)+'>'


class AdsMLPayerInformation(object):
    payer_party = None
    price_amount = None
    price_description = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.payer_party = AdsMLParty(xmlelement.find(
                ADSML_NS+'PayerParty'
            ))
            payers_price_details_element = xmlelement.find(
                ADSMLBOOKINGS_NS+'PayersPriceDetails'
            )
            if payers_price_details_element:
                total_price_element = payers_price_details_element.find(
                    ADSML_NS+'TotalPrice'
                )
                if total_price_element:
                    self.price_amount = total_price_element.findtext(
                        ADSML_NS+'Amount'
                    )
                    self.price_description = total_price_element.findtext(
                        ADSML_NS+'DescriptionLine'
                    )
        elif kwargs:
            if 'price_amount' in kwargs:
                self.price_amount = kwargs['price_amount']
            if 'price_description' in kwargs:
                self.price_description = kwargs['price_description']

    def set_payer_party(self, payer_party):
        self.payer_party = payer_party

    def to_xml(self):
        payer_information_object = etree.Element(ADSMLBOOKINGS_NS+'PayerInformation')
        payer_information_object.append(self.payer_party.to_xml(element_name="PayerParty"))
        payers_price_details_object = etree.Element(ADSMLBOOKINGS_NS+'PayersPriceDetails')
        total_price_object = etree.Element(ADSML_NS+'TotalPrice')
        amount_object = etree.Element(ADSML_NS+'Amount')
        amount_object.text = self.price_amount
        description_object = etree.Element(ADSML_NS+'DescriptionLine')
        description_object.text = self.price_description
        total_price_object.append(amount_object)
        total_price_object.append(description_object)
        payers_price_details_object.append(total_price_object)
        payer_information_object.append(payers_price_details_object)
        return payer_information_object
        
    def __str__(self):
        return (
                '<AdsMLPayerInformation ' +
                str(self.payer_party) + ', ' +
                str(self.price_amount) + ', ' +
                str(self.price_description) + '>'
        )


class AdsMLNotes(object):
    note_text = None
    note_time = None
    note_author = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            note_line = xmlelement.find(ADSML_NS+'NoteLine')
            self.note_text = note_line.text or ''
            self.note_time = note_line.attrib[ADSML_NS+'timeStamp']
            self.note_author = note_line.attrib[ADSML_NS+'author']
        elif kwargs:
            if 'note_text' in kwargs:
                self.note_text = kwargs['note_text']
            if 'note_time' in kwargs:
                self.note_time = kwargs['note_time']
            if 'note_author' in kwargs:
                self.note_author = kwargs['note_author']

    def to_xml(self):
        notes_object = etree.Element(ADSML_NS+'Notes')
        noteline_object = etree.Element(ADSML_NS+'NoteLine')
        noteline_object.text = self.note_text
        noteline_object.set(ADSML_NS+'timeStamp', self.note_time)
        noteline_object.set(ADSML_NS+'author', self.note_author)
        notes_object.append(noteline_object)
        return notes_object

    def __str__(self):
        return (
                '<AdsMLNotes ' +
                str(self.note_text) +' (' +
                str(self.note_author) + ', ' +
                str(self.note_time) + ')'
        )
