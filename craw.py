from bs4 import BeautifulSoup
import urllib2
import csv
import re
import sys
reload(sys)
# sys.setdefaultencoding('utf-8')


def process_one_page(url):
    req = urllib2.Request(url)

    csvfile = file('munich.csv', 'ab+')
    writer = csv.writer(csvfile)
    response = urllib2.urlopen(req)
    the_page = response.read()
    soup = BeautifulSoup(the_page, 'lxml')

    data = []

    for tag in soup.find_all(name="li", attrs={"class": re.compile("result-list__listing ")}):

        d = []

        # Rent and Area
        result = tag.find_all(name="dd", attrs={"class": re.compile("font-nowrap font-line-xs")})
        
        if len(result) != 3:
            continue

        for tagg, key in zip(result, ["Rent", "Area", "Rooms"]):

            if key == "Rooms":
                taggg = tagg.find(name="span", attrs={"class": re.compile("onlyLarge")})
                # print key, taggg.string
                d.append(taggg.string)
                continue

            # print key, tagg.string
            d.append(tagg.string)

        tagg = tag.find(name="a", attrs={
            "class": re.compile("result-list-entry__map-link font-ellipsis font-line font link-underline")})
        # print "Address", tagg.string
        d.append(tagg.string)

        # print d
        # Rent
        rent_raw = d[0].split(' ')[0]
        rent_split = rent_raw.split('.')
        rent = "".join(rent_split)
        d[0] = rent.encode('utf-8')

        # Area
        area_raw = d[1].split(' ')[0]
        area_split = area_raw.split(',')
        area = ".".join(area_split)
        d[1] = area.encode('utf-8')

        # Rooms
        room_raw = d[2].split(' ')[0]
        room_split = room_raw.split(',')
        room = ".".join(room_split)
        d[2] = room.encode('utf-8')

        # Address
        d[3] = d[3].encode('utf-8')

        print d

        data.append(d)

    writer.writerows(data)
    csvfile.close()


for page in range(1, 10):
    if page == 1:
        url = "https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Bayern/Muenchen-Kreis"
    else:
        url = "https://www.immobilienscout24.de/Suche/S-T/P-%d/Wohnung-Miete/Bayern/Muenchen-Kreis" % page

    process_one_page(url)
    print "page %d scanned." % page




