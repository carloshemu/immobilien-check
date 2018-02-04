from bs4 import BeautifulSoup
import urllib2
import csv
import re
import sys
from geopy.geocoders import Nominatim

reload(sys)
# sys.setdefaultencoding('utf-8')

csvfile_source = file('munich.csv', 'rb')
reader = csv.reader(csvfile_source)

csvfile = file('munich_extended.csv', 'ab+')
writer = csv.writer(csvfile)

geolocator = Nominatim()


for row in reader:

    print row
    addr = row[3]
    if len(addr.split(',')) > 2:
        region = addr.split(',')[-2][1:]
    else:
        region = addr.split(',')[-2]

    region_full = "%s, Muenchen" % region
    location = geolocator.geocode(region_full)

    if not location:
        raise RuntimeError("Cannot find geolocation!")

    print location.latitude, location.longitude

    data = [row[0], row[1], row[2], row[3], region, str(location.latitude), str(location.longitude)]
    print data

    writer.writerow(data)


csvfile_source.close()
csvfile.close()






