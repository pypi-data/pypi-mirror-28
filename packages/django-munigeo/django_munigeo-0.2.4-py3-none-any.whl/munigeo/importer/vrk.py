"""
munigeo importer for Väestörekisterikeskus data
"""

import os
import csv
import re
import requests
import yaml

from django import db
from datetime import datetime

from django.contrib.gis.gdal import DataSource, SpatialReference, CoordTransform
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Point
from django.contrib.gis import gdal

from munigeo.models import *
from munigeo.importer.sync import ModelSyncher
from munigeo import ocd

from munigeo.importer.base import Importer, register_importer

MUNI_URL = "http://tilastokeskus.fi/meta/luokitukset/kunta/001-2013/tekstitiedosto.txt"

# The Finnish national grid coordinates in TM35-FIN according to JHS-180
# specification. We use it as a bounding box.
FIN_GRID = [-548576, 6291456, 1548576, 8388608]
TM35_SRID = 3067

SERVICE_CATEGORY_MAP = {
    25480: ("library", "Library"),
    28148: ("swimming_pool", "Swimming pool"),
    25402: ("toilet", "Toilet"),
    25344: ("recycling", "Recycling point"),
    25664: ("park", "Park"),
}


TM35_SRID = 3067
TM35_SRS = SpatialReference(TM35_SRID)

coord_transform = None
if TM35_SRS.srid != PROJECTION_SRID:
    target_srs = SpatialReference(PROJECTION_SRID)
    coord_transform = CoordTransform(TM35_SRS, target_srs)


def convert_from_tm35(north, east):
    ps = "POINT (%f %f)" % (east, north)
    g = gdal.OGRGeometry(ps, TM35_SRS)
    if coord_transform:
        g.transform(coord_transform)
    return g

    # pnt = Point(east, north, srid=GK25_SRID)
    # if PROJECTION_SRID == GK25_SRID:
    #    return pnt
    # pnt.transform(coord_transform)
    # return pnt


@register_importer
class VRKImporter(Importer):
    name = "vrk"

    def __init__(self, *args, **kwargs):
        super(VRKImporter, self).__init__(*args, **kwargs)

    @db.transaction.atomic
    def import_addresses(self):
        path = '01osoitteet2016-08-15.OPT'
        FIELDS = [
            'building_id', 'muni_id', 'province_id', 'purpose_code', 'n', 'e', 'index',
            'street_fi', 'street_sv', 'street_number', 'post_code'
        ]
        STREET_NUMBER_RE = r'(?P<num>\d+)(?P<letter>[a-z]?)(?P<num2>-\d+)?'

        f = open(path, encoding='iso8859-1')
        reader = csv.DictReader(f, delimiter=';', fieldnames=FIELDS)

        muni_list = list(Municipality.objects.all().select_related('division'))
        muni_dict = {m.division.origin_id.zfill(3): m for m in muni_list}

        def make_addr_id(num, num_end, letter):
            if num_end is None:
                num_end = ''
            if letter is None:
                letter = ''
            return '%s-%s-%s' % (num, num_end, letter)

        for muni in muni_list:
            muni_dict[muni.name_fi] = muni

            self.logger.info('Loading existing data for %s' % muni)
            streets = Street.objects.filter(municipality=muni)
            muni.streets_by_name = {}
            muni.streets_by_id = {}
            for s in streets:
                muni.streets_by_name[s.name_fi] = s
                muni.streets_by_id[s.id] = s
                s.addrs = {}
                s._found = False

            addr_list = Address.objects.filter(street__municipality=muni)
            for a in addr_list:
                a._found = False
                street = muni.streets_by_id[a.street_id]
                street.addrs[make_addr_id(a.number, a.number_end, a.letter)] = a

        bulk_addr_list = []
        count = 0
        for idx, row in enumerate(reader):
            count += 1
            if count % 1000 == 0:
                print("%d processed" % count)

            street_name = row['street_fi'].strip()
            street_name_sv = row['street_sv'].strip()
            if not street_name:
                continue

            num = row['street_number'].strip()
            if not num:
                continue
            else:
                if num in ('0', '-'):
                    continue
            m = re.match(STREET_NUMBER_RE, num)
            if not m:
                continue
            num = m.group('num')
            num2 = m.group('num2')
            letter = m.group('letter')
            if not num2:
                num2 = ''
            else:
                num2 = num2.lstrip('-')
            if not letter:
                letter = ''

            coord_n = int(row['n'])
            coord_e = int(row['e'])

            muni = muni_dict[row['muni_id']]
            street = muni.streets_by_name.get(street_name, None)
            if not street:
                street = Street(name_fi=street_name, name=street_name, municipality=muni)
                street.name_sv = street_name_sv
                street.save()
                muni.streets_by_name[street_name] = street
                street.addrs = {}
            else:
                if not street.name_sv and street_name_sv:
                    # self.logger.warning("%s: %s -> %s" % (street, street.name_sv, street_name_sv))
                    street.name_sv = street_name_sv
                    street.save()
            street._found = True

            addr_id = make_addr_id(num, num2, letter)
            addr = street.addrs.get(addr_id, None)
            location = convert_from_tm35(coord_n, coord_e)
            if not addr:
                addr = Address(street=street, number=num, number_end=num2, letter=letter)
                addr.location = location.wkb
                # addr.save()
                bulk_addr_list.append(addr)
                street.addrs[addr_id] = addr
            else:
                if addr._found:
                    continue
                # if the location has changed for more than 10cm, save the new one.
                assert addr.location.srid == location.srid, "SRID changed"
                #if addr.location.distance(location) >= 0.10:
                #    self.logger.info("%s: Location changed" % addr)
                #    addr.location = location
                #    addr.save()
            addr._found = True

            #print "%s: %s %d%s N%d E%d (%f,%f)" % (muni_name, street, num, letter, coord_n, coord_e, pnt.y, pnt.x)

            if len(bulk_addr_list) >= 10000:
                print("Saving %d new addresses" % len(bulk_addr_list))

                Address.objects.bulk_create(bulk_addr_list)
                bulk_addr_list = []

                # Reset DB query store to free up memory
                db.reset_queries()

        if bulk_addr_list:
            print("Saving %d new addresses" % len(bulk_addr_list))
            Address.objects.bulk_create(bulk_addr_list)
            bulk_addr_list = []

        for muni in muni_list:
            for s in muni.streets_by_name.values():
                if not s._found:
                    print("Street %s removed" % s)
                    s.delete()
                    continue
                for a in s.addrs.values():
                    if not a._found:
                        print("%s removed" % a)
                        a.delete()

    def import_pois(self):
        URL_BASE = 'http://www.hel.fi/palvelukarttaws/rest/v2/unit/?service=%d'

        muni_dict = {}
        for muni in Municipality.objects.all():
            muni_dict[muni.name] = muni

        for srv_id in list(SERVICE_CATEGORY_MAP.keys()):
            cat_type, cat_desc = SERVICE_CATEGORY_MAP[srv_id]
            cat, c = POICategory.objects.get_or_create(type=cat_type, defaults={'description': cat_desc})

            print("\tImporting %s" % cat_type)
            ret = requests.get(URL_BASE % srv_id)
            for srv_info in ret.json():
                srv_id = str(srv_info['id'])
                try:
                    poi = POI.objects.get(origin_id=srv_id)
                except POI.DoesNotExist:
                    poi = POI(origin_id=srv_id)
                poi.name = srv_info['name_fi']
                poi.category = cat
                if not 'address_city_fi' in srv_info:
                    print("No city!")
                    print(srv_info)
                    continue
                city_name = srv_info['address_city_fi']
                if not city_name in muni_dict:
                    city_name = city_name.encode('utf8')
                    post_code = srv_info.get('address_zip', '')
                    if post_code.startswith('00'):
                        print("%s: %s (%s)" % (srv_info['id'], poi.name.encode('utf8'), city_name))
                        city_name = "Helsinki"
                    elif post_code.startswith('01'):
                        print("%s: %s (%s)" % (srv_info['id'], poi.name.encode('utf8'), city_name))
                        city_name = "Vantaa"
                    elif post_code in ('02700', '02701', '02760'):
                        print("%s: %s (%s)" % (srv_info['id'], poi.name.encode('utf8'), city_name))
                        city_name = "Kauniainen"
                    elif post_code.startswith('02'):
                        print("%s: %s (%s)" % (srv_info['id'], poi.name.encode('utf8'), city_name))
                        city_name = "Espoo"
                    else:
                        print(srv_info)
                poi.municipality = muni_dict[city_name]
                poi.street_address = srv_info.get('street_address_fi', None)
                poi.zip_code = srv_info.get('address_zip', None)
                if not 'northing_etrs_gk25' in srv_info:
                    print("No location!")
                    print(srv_info)
                    continue
                poi.location = convert_from_gk25(srv_info['northing_etrs_gk25'], srv_info['easting_etrs_gk25'])
                poi.save()
