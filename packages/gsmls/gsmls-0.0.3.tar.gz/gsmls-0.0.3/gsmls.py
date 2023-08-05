#!/usr/bin/env python3

import re
import requests
import logging
import lxml.html, lxml.etree
from typing import List
from itertools import chain

__version__ = '0.0.3'

class GSMLSException(Exception):
    pass

# https://forms.gsmls.com/TownCodes.pdf

counties = {
    "Atlantic": 10,
    "Bergen": 11,
    "Burlington": 12,
    "Camden": 13,
    "CapeMay": 14,
    "Cumberland": 15,
    "Essex": 16,
    "Gloucester": 17,
    "Hudson": 18,
    "Hunterdon": 19,
    "Mercer": 20,
    "Middlesex": 21,
    "Monmouth": 22,
    "Morris": 23,
    "Ocean": 24,
    "Passaic": 25,
    "Salem": 26,
    "Somerset": 27,
    "Sussex": 28,
    "Union": 29,
    "Warren": 30,
}

def get_towns(county):
    payload = {
        "idxId": "",
        "token": "",
        "transactionsought": "purchase",
        "propertytype": "RES",
        "town": "ALL",
        "Continue": "Continue",
        "countycode": counties[county],
        "countyname": county}
    response = requests.post("https://www2.gsmls.com/publicsite/propsearch.do?method=getpropertysearch", data=payload)
    doc = lxml.html.fromstring(response.content)
    sttowns = doc.cssselect('form[name="propsearch"] input[name="sttowns"]')[0].get('value')
    return sttowns.split(',')

def get_listings_inner(county, towns, min_list_price='', max_list_price='', min_bedrooms='', min_bathrooms=''):
    payload = {
        'idxId': '',
        'token': '',
        'minlistprice': min_list_price,
        'maxlistprice': max_list_price,
        'minbedrooms': min_bedrooms,
        'minbaths': min_bathrooms,
        'minacres': '',
        'maxacres': '',
        'lotdesc': '',
        'Search': 'Search',
        'countycode': counties[county],
        'countyname': county,
        'propertytype': 'RES',
        'propertytypedesc': 'Residential',
        'transactionsought': 'purchase',
        'sttowns': ','.join(towns),
    }
    logging.debug(f"get listings with: {payload}")
    response = requests.post("https://www2.gsmls.com/publicsite/propsearch.do?method=getpropertydetails", data=payload)
    if "which is over the limit of 250" in response.text:
        raise GSMLSException(f"more than 250 listings returned in {county} with payload {payload}")
    if "Your search returned no records." in response.text:
        raise GSMLSException(f"your search returned no records in {county} with payload {payload}")
    doc = lxml.html.fromstring(response.content)
    stmlsnums = doc.cssselect('form[name="propsearch"] input[name="stmlsnums"]')[0].get('value')
    return stmlsnums.split(',')

def get_listing_detail(sysid: str): # mlsnums
    payload = {
        'idxId': '',
        'token': '',
        'propertytype': 'RES',
        'propertytypedesc': 'Residential',
        'transactionsought': 'purchase',
        'listpricesel': '',
        'sortorder': '',
        'noresultsflag': '',
        'openmap': 'true',
        'mailto': '',
        'subject': '',
        'mailbody': '',
        'pubid': '',
        'mlsnum': '',
        'stmlsnums': sysid, #','.join(mlsnums),
    }
    response = requests.post(f"https://www2.gsmls.com/publicsite/propsearch.do?method=moredetails&sysid={sysid}", data=payload)
    return response

def get_listings_summary(mlsnums: List[str]):
    payload = {
        'idxId': '',
        'token': '',
        'propertytype': 'RES',
        'propertytypedesc': 'Residential',
        'transactionsought': 'purchase',
        'listpricesel': '',
        'sortorder': '',
        'noresultsflag': '',
        'openmap': 'true',
        'mailto': '',
        'subject': '',
        'mailbody': '',
        'pubid': '',
        'mlsnum': '',
        'stmlsnums': ','.join(mlsnums),
        'selmlsnums': mlsnums,
    }
    response = requests.post(f"https://www2.gsmls.com/publicsite/propsearch.do?method=printablereport", data=payload)

    def get(listing, selector, name, fn):
        try:
            return [fn(x) for x in listing.cssselect(selector) if x.text == name][0]
        except IndexError:
            return None

    def parse_int(x):
        if x is not None:
            try:
                return int(x.replace(',', ''))
            except ValueError:
                pass
        return x

    def parse_money(x):
        if x is not None:
            return parse_int(x.strip().replace('$', '').replace(',', ''))
        return x

    def parse_float(x):
        if x is not None:
            try:
                return float(x)
            except ValueError:
                pass
        return x

    def parse_str(x):
        if x is not None:
            return re.sub(r'\s+', ' ', x.strip())
        return x

    def parse_lot(a):
        try:
            x, y = a.split('X')
            return int(x) * int(y)
        except Exception as e:
            return None

    doc = lxml.html.fromstring(response.content)
    listings = []
    for i, row in enumerate(doc.cssselect('table')):
        # TODO: add the following attributes
        # YB/Desc
        # Remarks
        # Listing Office
        # Office Phone
        # Listing Agent
        listing = {
            "id": get(row, 'b u', "MLS#", lambda x: x.getparent().getnext()).text,
            "price": parse_money(get(row, 'b u', "MLS#", lambda x: x.getparent().getparent().getprevious()).text),
            "address": parse_str(get(row, 'b', 'Address:', lambda x: x.tail)),
            "county": get(row, 'b u', 'County:', lambda x: x.getparent().getnext()).text,
            "city": get(row, 'b u', 'Cities/Towns:', lambda x: x.getparent().getnext()).text,
            "style": get(row, 'b u', 'Style:', lambda x: x.getparent().getnext()).text,
            "rooms": parse_int(get(row, 'b u', 'Rooms:', lambda x: x.getparent().getnext()).text),
            "bedrooms": parse_int(get(row, 'b u', 'Bedrooms:', lambda x: x.getparent().getnext()).text),
            "baths_full": parse_int(get(row, 'b u', 'Full Baths:', lambda x: x.getparent().getnext()).text),
            "baths_part": parse_int(get(row, 'b u', 'Half Baths:', lambda x: x.getparent().getnext()).text),
            "baths_total": parse_float(get(row, 'b u', 'Total Baths:', lambda x: x.getparent().getnext()).text),
            "sqft": parse_int(get(row, 'b u', 'Sq Ft:', lambda x: x.getparent().getnext()).text),
            "lot": parse_lot(get(row, 'b u', 'Lot Size:', lambda x: x.getparent().getnext()).text),
            "tax": parse_int(get(row, 'b u', 'Tax Amount:', lambda x: x.getparent().getnext()).text),
            "tax_year": parse_int(get(row, 'b u', 'Tax Year:', lambda x: x.getparent().getnext()).text),
            "heat_source": parse_str(get(row, 'b u', 'Heat Source:', lambda x: x.getparent().getnext()).text),
            "heat_system": parse_str(get(row, 'b u', 'Heat System:', lambda x: x.getparent().getnext()).text),
            "cool_system": parse_str(get(row, 'b u', 'Cool System:', lambda x: x.getparent().getnext()).text),
            "water": parse_str(get(row, 'b u', 'Water:', lambda x: x.getparent().getnext()).text),
            "sewer": parse_str(get(row, 'b u', 'Sewer:', lambda x: x.getparent().getnext()).text),
            "utilities": parse_str(get(row, 'b u', 'Utilities:', lambda x: x.getparent().getnext()).text),
        }
        listings.append(listing)
    return listings

def get_listings(county, **kwargs):
    mytowns = get_towns(county)
    mlsnums = get_listings_inner(county, mytowns, **kwargs)
    # NOTE: if mlsnums is empty it looks like we just return every listing?
    listings = get_listings_summary(mlsnums)
    return listings

def get_listing_media_link(mlsid):
    return f'https://www2.gsmls.com/publicsite/propsearch.do?method=getmedia&mlsnum={mlsid}&lstngsysid=0&imagecount=50&openhousesysid='

def get_listing_detail_preview(mlsid):

    def remove_node(x):
        y = x.getparent()
        y.remove(x)

    def stringify_children(node):
        parts = ([node.text] +
                list(chain(*([c.text, lxml.html.tostring(c).decode('utf-8'), c.tail] for c in node.getchildren()))) +
                [node.tail])
        # filter removes possible Nones in texts and tails
        return ''.join(filter(None, parts))

    doc = lxml.html.fromstring(get_listing_detail(mlsid).content)
    content = doc.cssselect('#content .bufer')[0]
    remove_node(content.cssselect('input[title="Select this property"]')[0].getnext())
    remove_node(content.cssselect('input[title="Select this property"]')[0])
    remove_node(content.cssselect('#footer')[0])
    remove_node(content.cssselect('img[alt="More Media"]')[0])
    remove_node(content.cssselect('a[title="Open media link"]')[0])
    img_src = content.cssselect('a[title="Open media link"] img')[0].get('src')
    remove_node(content.cssselect('a[title="Open media link"]')[0])

    media_url = get_listing_media_link(mlsid)
    media_atag = f"<a href='{media_url}'><img src='{img_src}'></a>"    
    html = media_atag + "\n" + lxml.html.tostring(content).decode('utf-8')
    return html

def get_listing_media_preview(mlsid):
    media_url = get_listing_media_link(mlsid)
    return requests.get(media_url).text
