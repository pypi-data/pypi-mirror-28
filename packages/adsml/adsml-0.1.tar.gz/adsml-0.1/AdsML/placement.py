#!/usr/bin/env python

import xml.etree.ElementTree as etree
from .core import ADSMLBOOKINGS_NS, ADSML_NS, ADSMLMA_NS
from .party import AdsMLParty
from .materials import AdsMLAdContent, AdsMLMaterialsExpectations


class AdsMLPlacement(object):
    placement_identifier = None
    is_standalone = None
    # <!-- Ad pattern (Interactive= Digital, Display = Display, Classified = Display -->
    ad_type_code = None
    advertiser_brand = None
    placement_price = None
    description_line = None
    publication = None
    insertion_period = None
    production_detail = None
    ad_content = None
    materials_expectations = None
               
    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.placement_identifier = xmlelement.findtext(ADSMLBOOKINGS_NS+'PlacementIdentifier')
            self.is_standalone = xmlelement.findtext(ADSMLBOOKINGS_NS+'IsStandAlone')
            ad_type_element = xmlelement.find(ADSML_NS+'AdType')
            if ad_type_element:
                self.ad_type_code = ad_type_element.findtext(ADSML_NS+'CodeValue')
            self.advertiser_brand = AdsMLAdvertiserBrand(xmlelement.find(ADSMLBOOKINGS_NS+'AdvertiserBrand'))
            self.placement_price = AdsMLPlacementPrice(xmlelement.find(ADSMLBOOKINGS_NS+'PlacementPrice'))
            self.description_line = xmlelement.find(ADSML_NS+'DescriptionLine')
            self.publication = AdsMLPublication(xmlelement.find(ADSMLBOOKINGS_NS+'Publication'))
            self.insertion_period = AdsMLPublication(xmlelement.find(ADSMLBOOKINGS_NS+'InsertionPeriod'))
            self.production_detail = AdsMLProductionDetailNewspaperMagazine(xmlelement.find(ADSMLBOOKINGS_NS+'ProductionDetail.NewspaperMagazine'))
            self.ad_content = AdsMLAdContent(xmlelement.find(ADSMLMA_NS+'AdContent'))
            self.materials_expectations = AdsMLMaterialsExpectations(
                xmlelement.find(ADSMLMA_NS+'MaterialsExpectations')
            )
        else:
            if 'placement_identifier' in kwargs:
                self.placement_identifier = kwargs['placement_identifier']
            if 'is_standalone' in kwargs:
                self.is_standalone = kwargs['is_standalone']
            if 'ad_type_code' in kwargs:
                self.ad_type_code = kwargs['ad_type_code']
            if 'advertiser_brand' in kwargs:
                self.advertiser_brand = kwargs['advertiser_brand']
            if 'placement_price' in kwargs:
                self.placement_price = kwargs['placement_price']
            if 'description_line' in kwargs:
                self.description_line = kwargs['description_line']
            if 'publication' in kwargs:
                self.publication = kwargs['publication']
            if 'insertion_period' in kwargs:
                self.insertion_period = kwargs['insertion_period']
            if 'production_detail' in kwargs:
                self.production_detail = kwargs['production_detail']
            if 'ad_content' in kwargs:
                self.ad_content = kwargs['ad_content']
            if 'materials_expectations' in kwargs:
                self.materials_expectations = kwargs['materials_expectations']

    # default elementname to Newspaper one, but can support others too
    def to_xml(self, element_name='Placement.NewspaperMagazine'):
        xml_object = etree.Element(ADSMLBOOKINGS_NS+element_name)
        if self.placement_identifier:
            placement_identifier_object = etree.Element(ADSMLBOOKINGS_NS+'PlacementIdentifier')
            placement_identifier_object.text = self.placement_identifier
            xml_object.append(placement_identifier_object)
        if self.is_standalone:
            is_standalone_object = etree.Element(ADSMLBOOKINGS_NS+'IsStandAlone')
            is_standalone_object.text = 'true' if self.is_standalone else 'false'
            xml_object.append(is_standalone_object)
        if self.ad_type_code:
            ad_type_object = etree.Element(ADSMLBOOKINGS_NS+'AdType')
            code_value_object = etree.Element(ADSMLBOOKINGS_NS+'CodeValue')
            code_value_object.text = self.ad_type_code
            ad_type_object.append(code_value_object)
            xml_object.append(ad_type_object)
        if self.advertiser_brand:
            xml_object.append(self.advertiser_brand.to_xml())
        if self.placement_price:
            xml_object.append(self.placement_price.to_xml())
        if self.description_line:
            description_line_object = etree.Element(ADSML_NS+'DescriptionLine')
            description_line_object.text = self.description_line
            xml_object.append(description_line_object)
        if self.publication:
            xml_object.append(self.publication.to_xml())
        if self.insertion_period:
            xml_object.append(self.insertion_period.to_xml())
        if self.production_detail:
            xml_object.append(self.production_detail.to_xml())
        if self.ad_content:
            xml_object.append(self.ad_content.to_xml())
        if self.materials_expectations:
            xml_object.append(self.materials_expectations.to_xml())
        return xml_object
        
    def __str__(self):
        return '<AdsMLPlacement '+ str(self.placement_identifier) +'>'


class AdsMLAdvertiserBrand(object):
    advertiser = None
    brand_name = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.advertiser = AdsMLParty(xmlelement.find(ADSML_NS+'Advertiser'))
            brand_object = xmlelement.find(ADSMLBOOKINGS_NS+'Brand')
            if brand_object:
                brand_name_object = brand_object.find(ADSML_NS+'Name')
                if brand_name_object:
                    self.brand_name = brand_name_object.text
        elif kwargs:
            if 'advertiser' in kwargs:
                self.advertiser = kwargs['advertiser']
            if 'brand_name' in kwargs:
                self.brand_name = kwargs['brand_name']

    def to_xml(self):
        xml_object = etree.Element(ADSMLBOOKINGS_NS+'AdvertiserBrand')
        if self.advertiser:
            xml_object.append(self.advertiser.to_xml(element_name='Advertiser'))
        if self.brand_name:
            brand_object = etree.Element(ADSMLBOOKINGS_NS+'Brand')
            name_object = etree.Element(ADSML_NS+'Name')
            name_object.text = self.brand_name
            brand_object.append(name_object)
            xml_object.append(brand_object)
        return xml_object
        
    def __str__(self):
        return '<AdsMLAdvertiserBrand '+ str(self.brand_name) +'>'


class AdsMLPriceComponent(object):
    name_codevalue = None
    name_description = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            price_component_name = xmlelement.find(ADSML_NS+'PriceComponentName')
            if price_component_name:
                self.name_codevalue = price_component_name.find(ADSML_NS+'CodeValue')
                self.name_description = price_component_name.find(ADSML_NS+'Description')
            # <!-- net price of the ad -->
            self.amount = xmlelement.findtext(ADSML_NS+'Amount')

    def to_xml(self):
        return

    def __str__(self):
        return '<AdsMLPriceComponent ' + self.name_codevalue + '(' + self.amount + ')>'


class AdsMLPlacementPrice(object):
    total_price_amount = None
    price_components = {}

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            total_price = xmlelement.find(ADSML_NS+'TotalPrice')
            if total_price:
                self.total_price_amount = total_price.findtext(ADSML_NS+'Amount')
            # a sequence of "PriceComponent"s
            price_components_list = xmlelement.findall(ADSML_NS+'PriceComponent')
            for price_component in price_components_list:
                sequence_no = price_component.attrib[ADSML_NS+'sequenceNo']
                self.price_components[sequence_no] = AdsMLPriceComponent(price_component)
        elif kwargs:
            if 'total_price_amount' in kwargs:
                self.total_price_amount = kwargs['total_price_amount']

    def to_xml(self):
        xml_object = etree.Element(ADSMLBOOKINGS_NS+'PlacementPrice')
        total_price_object = etree.Element(ADSML_NS+'TotalPrice')
        amount_object = etree.Element(ADSML_NS+'Amount')
        amount_object.text = self.total_price_amount
        total_price_object.append(amount_object)
        xml_object.append(total_price_object)
        if self.price_components:
            xml_object.append(self.price_components.to_xml())
        return xml_object

    def __str__(self):
        return '<AdsMLPlacementPrice ' + self.total_price_amount + ')>'


class AdsMLPublication(object):
    publication_code = None
    publication_name = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            publication_code_element = xmlelement.find(ADSMLBOOKINGS_NS+'PublicationCode')
            if publication_code_element:
                self.publication_code = publication_code_element.findtext(ADSML_NS+'CodeValue')
            self.publication_name = xmlelement.find(ADSML_NS+'Name')
        elif kwargs:
            if 'publication_code' in kwargs:
                self.publication_code = kwargs['publication_code']
            if 'publication_name' in kwargs:
                self.publication_name = kwargs['publication_name']

    def to_xml(self):
        xml_object = etree.Element(ADSMLBOOKINGS_NS+'Publication')
        publication_code_object = etree.Element(ADSMLBOOKINGS_NS+'PublicationCode')
        code_value_object = etree.Element(ADSML_NS+'CodeValue')
        code_value_object.text = self.publication_code
        publication_code_object.append(code_value_object)
        xml_object.append(publication_code_object)
        if self.publication_name:
            publication_name_object = etree.Element(ADSML_NS+'Name')
            publication_name_object.text = self.publication_name
            xml_object.append(publication_name_object)
        return xml_object

    def __str__(self):
        return self.publication_name + ' (' + self.publication_code + ')'


class AdsMLInsertionPeriod(object):
    schedule_entry_identifier = None
    first_possible_time = None
    last_possible_time = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.schedule_entry_identifier = xmlelement.findtext(ADSMLBOOKINGS_NS+'ScheduleEntryIdentifier')
            self.first_possible_time = xmlelement.findtext(ADSMLBOOKINGS_NS+'FirstPossibleTime')
            self.last_possible_time = xmlelement.findtext(ADSMLBOOKINGS_NS+'LastPossibleTime')
        elif kwargs:
            if 'schedule_entry_identifier' in kwargs:
                self.schedule_entry_identifier = kwargs['schedule_entry_identifier']
            if 'first_possible_time' in kwargs:
                self.first_possible_time = kwargs['first_possible_time']
            if 'last_possible_time' in kwargs:
                self.last_possible_time = kwargs['last_possible_time']

    def to_xml(self):
        xml_object = etree.Element(ADSMLBOOKINGS_NS+'InsertionPeriod')
        if self.schedule_entry_identifier:
            schedule_entry_identifier_object = etree.Element(ADSMLBOOKINGS_NS+'ScheduleEntryIdentifier')
            schedule_entry_identifier_object.text = self.schedule_entry_identifier
            xml_object.append(schedule_entry_identifier_object)
        if self.first_possible_time:
            first_possible_time_object = etree.Element(ADSMLBOOKINGS_NS+'FirstPossibleTime')
            first_possible_time_object.text = self.first_possible_time
            xml_object.append(first_possible_time_object)
        if self.last_possible_time:
            last_possible_time_object = etree.Element(ADSMLBOOKINGS_NS+'LastPossibleTime')
            last_possible_time_object.text = self.last_possible_time
            xml_object.append(last_possible_time_object)
        return xml_object

    def __str__(self):
        return ('<AdsMLInsertionPeriod ' + self.schedule_entry_identifier
                + ' (' + self.first_possible_time + ' - ' + self.last_possible_time + ')'
                + '>')


class AdsMLSize(object):
    width = None
    height = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.width = AdsMLValueWithUnits(xmlelement.find(ADSMLBOOKINGS_NS+'Width'))
            self.height = AdsMLValueWithUnits(xmlelement.find(ADSMLBOOKINGS_NS+'Height'))
        elif kwargs:
            if 'width' in kwargs:
                self.width = kwargs['width']
            if 'height' in kwargs:
                self.height = kwargs['height']

    def to_xml(self):
        xml_object = etree.Element(ADSMLBOOKINGS_NS+'Size')
        if self.width:
            xml_object.append(self.width.to_xml(element_name='Width'))
        if self.height:
            xml_object.append(self.height.to_xml(element_name='Height'))
        return xml_object
        
    def __str__(self):
        # might need to change the order or style to account
        # for "25 x 4" which is actually height x width
        return self.width + 'x' + self.height


class AdsMLColors(object):
    color_type_code_value = None

    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.color_type_code_value = AdsMLCodeValue(xmlelement.find(ADSMLBOOKINGS_NS+'ColorType'))
        elif kwargs:
            if 'color_type' in kwargs:
                self.color_type_code_value = kwargs['color_type']

    def to_xml(self):
        xml_object = etree.Element(ADSMLBOOKINGS_NS+'Colors')
        color_type_object = etree.Element(ADSMLBOOKINGS_NS+'ColorType')
        color_type_object.append(self.color_type_code_value.to_xml())
        xml_object.append(color_type_object)
        return xml_object
        
    def __str__(self):
        return '<AdsMLColors ' + self.color_type.code_value + '>'


class AdsMLPositioning(object):
    section_code_value = None
    section_code_description = None
    position_code_value = None
    cuttable_position = None
   
    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            primary_positioning_element = xmlelement.find(ADSMLBOOKINGS_NS+'PrimaryPositioning')
            placement_in_book_element = primary_positioning_element.find(ADSMLBOOKINGS_NS+'PlacementInBook')
            section_code_element = placement_in_book_element.find(ADSMLBOOKINGS_NS+'SectionCode')
            self.section_code_value = section_code_element.findtext(ADSML_NS+'CodeValue')
            self.section_code_description = section_code_element.findtext(ADSML_NS+'Description')
            position_on_page_element = primary_positioning_element.find(ADSMLBOOKINGS_NS+'PositionOnPage')
            position_code_element = position_on_page_element.find(ADSML_NS+'Code')
            self.position_code_value = position_code_element.find(ADSML_NS+'CodeValue')
            self.cuttable_position = primary_positioning_element.findtext(ADSMLBOOKINGS_NS+'CuttablePosition')
        elif kwargs:
            if 'section_code_value' in kwargs:
                self.section_code_value = kwargs['section_code_value']
            if 'section_code_description' in kwargs:
                self.section_code_description = kwargs['section_code_description']
            if 'position_code_value' in kwargs:
                self.position_code_value = kwargs['position_code_value']
            if 'cuttable_position' in kwargs:
                self.cuttable_position = kwargs['cuttable_position']

    def to_xml(self):
        xml_object = etree.Element(ADSMLBOOKINGS_NS+'Positioning')
        primary_positioning_object = etree.Element(ADSMLBOOKINGS_NS+'PrimaryPositioning')
        if self.section_code_value:
            placement_in_book_object = etree.Element(ADSMLBOOKINGS_NS+'PlacementInBook')
            section_code_object = etree.Element(ADSMLBOOKINGS_NS+'SectionCode')
            section_code_value_object = etree.Element(ADSML_NS+'CodeValue')
            section_code_value_object.text = self.section_code_value
            section_code_object.append(section_code_value_object)
            section_code_description_object = etree.Element(ADSML_NS+'Description')
            section_code_description_object.text = self.section_code_description
            section_code_object.append(section_code_description_object)
            placement_in_book_object.append(section_code_object)
            primary_positioning_object.append(placement_in_book_object)
        if self.position_code_value:
            position_on_page_object = etree.Element(ADSMLBOOKINGS_NS+'PositionOnPage')
            position_on_page_code_object = etree.Element(ADSML_NS+'Code')
            position_on_page_code_value_object = etree.Element(ADSML_NS+'CodeValue')
            position_on_page_code_value_object.text = self.position_code_value
            position_on_page_code_object.append(position_on_page_code_value_object)
            position_on_page_object.append(position_on_page_code_object)
            primary_positioning_object.append(position_on_page_object)
        xml_object.append(primary_positioning_object)
        if self.cuttable_position is not None:
            cuttable_position_object = etree.Element(ADSMLBOOKINGS_NS+'CuttablePosition')
            cuttable_position_object.text = 'true' if self.cuttable_position else 'false'
            xml_object.append(cuttable_position_object)
        return xml_object

    def __str__(self):
        return (
            '<AdsMLPositioning '
            'section ' + self.section_code_description + '(' + self.section_code_value + ') '
            'position ' + self.position_code_value + 
            '>'
        )


class AdsMLProductionDetailNewspaperMagazine(object):
    size = None
    colors = None
    positioning = None
    
    def __init__(self, xmlelement=None, **kwargs):
        if type(xmlelement) == etree.Element:
            self.size = AdsMLSize(xmlelement.find(ADSMLBOOKINGS_NS+'Size'))
            self.colors = AdsMLColors(xmlelement.find(ADSMLBOOKINGS_NS+'Colors'))
            self.positioning = AdsMLPositioning(xmlelement.find(ADSMLBOOKINGS_NS+'Positioning'))
        elif kwargs:
            if 'size' in kwargs:
                self.size = kwargs['size']
            if 'colors' in kwargs:
                self.colors = kwargs['colors']
            if 'positioning' in kwargs:
                self.positioning = kwargs['positioning']

    def to_xml(self):
        xml_object = etree.Element(ADSMLBOOKINGS_NS+'ProductionDetail.NewspaperMagazine')
        if self.size:
            xml_object.append(self.size.to_xml())
        if self.colors:
            xml_object.append(self.colors.to_xml())
        if self.positioning:
            xml_object.append(self.positioning.to_xml())
        return xml_object

    def __str__(self):
        return (
            '<ProductionDetail.NewspaperMagazine: '
            'size ' + self.size +
            'colors ' + self.colors + 
            'positioning ' + self.positioning + 
            '>'
        )
