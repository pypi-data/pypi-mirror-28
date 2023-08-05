AdsML - Python implementation of the AdsML standard
===================================================

AdsML is a suite of business-to-business electronic commerce standards intended to
support the exchange of advertising business messages and content delivery using
XML. Typical users include newspapers, advertising agencies, broadcasters and
others who buy or sell advertising.

This module is a part-implementation of the protocol in Python. Currently it
implements part of the AdsML-Bookings component of the standard.

Currently built for Python 3 only - please let me know if you require Python 2 support.

Installation
------------

Installing from PyPI::

    pip install adsml

Usage
-----

Example::

    import adsml

    parser = AdsMLParser("adsml-file.txt")

    # process the header
    header = parser.get_header()
    order = parser.get_order()

    print ("Order: {}: (buyers ref {})".format(order, order.buyers_reference))
    print ("Booking party: {}".format(order.booking_party))
    print ("Selling party: {}".format(order.selling_party))
    print ("Campaign: {}".format(order.campaign))
    print ("Payer information: {}".format(order.payer_information))
    print ("Placement: {}".format(order.placement))
    print ("Notes: {})".format(order.notes))

Release notes
-------------

* 0.1 - First working release, pinned to Python 3 only (use pip >9.0 to ensure pip Python version requirement works properly)
