from bs4 import BeautifulSoup
import urllib2
import csv
import re
import pandas as pd
import locale
import os
from geopy.geocoders import Nominatim
import sys
reload(sys)
# sys.setdefaultencoding('utf-8')


geolocator = Nominatim(timeout=5)


def update_locale():
    locale.setlocale(locale.LC_ALL, 'deu_deu')


def get_geo_info(addr_str):

    if len(addr_str.split(',')) > 2:
        region = addr_str.split(',')[-2][1:]
    else:
        region = addr_str.split(',')[-2]

    region_full = "%s, Muenchen" % region
    location = geolocator.geocode(region_full)

    if not location:
        # Try with larger area
        region_full = "%s, Bayern" % region
        location = geolocator.geocode(region_full)

        if not location:
            raise RuntimeError("Error in finding GEO information of %s" % region_full)

    return region, str(location.latitude), str(location.longitude)


def get_one_page_soup(url):
    req = urllib2.Request(url)

    response = urllib2.urlopen(req)
    the_page = response.read()
    return BeautifulSoup(the_page, 'html.parser')


def process_one_page_rent(url, df):

    soup = get_one_page_soup(url)

    csvfile = file('munich_new.csv', 'ab+')
    writer = csv.writer(csvfile)

    data = []

    for tag in soup.find_all(name="li", attrs={"class": re.compile("result-list__listing")}):

        d = []

        # Rent and Area
        result = tag.find_all(name="dd", attrs={"class": re.compile("font-nowrap")})

        if len(result) != 3:
            continue

        for tagg, key in zip(result, ["Rent", "Area", "Rooms"]):

            if key == "Rooms":
                taggg = tagg.find(name="span", attrs={"class": re.compile("onlyLarge")})
                d.append(taggg.string)
                continue

            # print key, tagg.string
            d.append(tagg.string)

        tagg = tag.find(name="a", attrs={
            "class": re.compile("result-list-entry__map-link$")})
        # print "Address", tagg.string
        d.append(tagg.string)

        # print d
        # Rent
        rent_raw = d[0].split(' ')[0]
        rent = locale.atof(rent_raw)
        d[0] = int(rent)
        # d[0] = rent.encode('utf-8')

        # Area
        area_raw = d[1].split(' ')[0]
        area = locale.atof(area_raw)
        d[1] = area

        # Rooms
        room_raw = d[2].split(' ')[0]
        room = locale.atof(room_raw)
        d[2] = room

        # Address
        d[3] = d[3].encode('utf-8')

        # Rent/m2
        raw_str = "%.2f" % (d[0] / d[1])
        d.append(raw_str)

        # latitude and longitude
        (region, lat, lon) = get_geo_info(d[3])
        d.append(region)
        d.append(lat)
        d.append(lon)

        # Check if entry exists
        query_result = df[(df.rent == d[0]) & (df.area == d[1]) & (df.rooms == d[2])]
        if len(query_result) == 0:
            print "Add new entry: ", d
            data.append(d)

    writer.writerows(data)
    csvfile.close()


def load_previous_data(fname):
    df = pd.read_csv(fname, delimiter=",",
                     header=None,
                     names=["rent", "area", "rooms", "address"])
    return df


def get_page_num(url):

    soup = get_one_page_soup(url)

    page_tag = soup.find(name="div", attrs={"id": re.compile("pageSelection")})
    page_num = len(page_tag.find_all('option'))
    if page_num >= 1:
        return page_num
    else:
        raise RuntimeError("Error with getting page number.")


def add_new_data(main_url, fname):
    update_locale()

    if os.path.isfile(fname):
        df = load_previous_data(fname)
    else:
        df = None

    page_num = get_page_num(main_url)
    main_url_part = main_url.split('/')
    main_url_part.insert(5, 'P')

    for page in range(9, page_num + 1):
        main_url_part[5] = 'P-%d' % page
        url = '/'.join(main_url_part)
        # url = "https://www.immobilienscout24.de/Suche/S-T/P-%d/Wohnung-Miete/Bayern/Muenchen-Kreis" % page

        process_one_page_rent(url, df)
        print "page %d scanned." % page




# for page in range(1, 10):
#     if page == 1:
#         url = "https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Bayern/Muenchen-Kreis"
#     else:
#         url = "https://www.immobilienscout24.de/Suche/S-T/P-%d/Wohnung-Miete/Bayern/Muenchen-Kreis" % page
#
#     process_one_page_rent(url)
#     print "page %d scanned." % page




