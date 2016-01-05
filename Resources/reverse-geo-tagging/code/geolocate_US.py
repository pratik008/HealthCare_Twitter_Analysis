#!/usr/bin/env python
#
#       geolocate - python module and cli utility
#       
#       Copyright 2009 Matthew Brush < mbrush AT leftclick DOT ca >
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
       
# called by geolocate_reverse.py

# requires local database
# #######################
# pcdata.db
"""
import json
from geolocate_US import GeoLocation 
gl = GeoLocation()

results = gl.locate_by_latlon(('42.376582', '-71.061648'))
print json.dumps(results,indent=4)

results = gl.locate_by_postal_code('18940')
print json.dumps(results,indent=4)

city_name = 'Pasadena'
results   = gl.search_database(city=city_name)
print "number of results for %s: %d"%(city_name,len(results))
print json.dumps(results,indent=4)
"""

import os
import sqlite3 as sqlite
from optparse import OptionParser

class GeoLocation:
        
    def __init__(self, dbfile='/home/ubuntu/geocoding/pcdata.db'):
        self.dbfile = dbfile
        pass
    
    @staticmethod
    def _create_db(filename, delete=False):
        """ Creates the SQLite datbase and Postal Code table """
        if os.path.isfile(filename) and delete:
            print "database exists, deleting first"
            os.remove(filename)
            
        conn = sqlite.connect(filename)
        cursor = conn.cursor()
        cursor.execute("""create table postal_codes(
            id              INTEGER PRIMARY KEY,
            postal_code     TEXT, 
            region          TEXT,
            province        TEXT,
            province_code   TEXT,
            city_type       TEXT, 
            latitude        REAL,
            longitude       REAL)
        """)
        conn.commit()
        conn.close()
        print "database and table created"
    
    @staticmethod
    def _import_data(infile, dbfile, sep='|'):
        """ 
        Reads data from the infile and inserts it into the SQLite Postal
        code table.  Data must be in the format below (can use different separator).
        POSTAL_CODE_ID|PostalCode|City|Province|ProvinceCode|CityType|Latitude|Longitude
        """
        GeoLocation._create_db(dbfile, True)
        
        conn = sqlite.connect(dbfile)
        cursor = conn.cursor()
        f = open(infile)
        skip_count = 0
        line_count = 0
        print "importing data..."
        
        for line in f:
            try:
                fields = line.split(sep)
                id = int(fields[0].strip())
                pc = fields[1].strip().upper().replace(' ', '')
                region = fields[2].strip()
                province = fields[3].strip()
                prov_code = fields[4].strip().upper()
                city_type = fields[5].strip().upper()
                latitude = float(fields[6].strip())
                longitude = float(fields[7].strip())
                params = (id, pc, region, province, prov_code, city_type, latitude, longitude)
                cursor.execute('insert into postal_codes values (?,?,?,?,?,?,?,?)', params)
                line_count = line_count + 1
            except ValueError:
                skip_count = skip_count + 1
                continue
                
        print "skipped " + str(skip_count) + " lines"
        print "imported " + str(line_count) + " lines"
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def _print_data(dbfile):
        """ Prints every row from the database (for testing/debugging) """
        conn = sqlite.connect(dbfile)
        cursor = conn.cursor()
        cursor.execute('select * from postal_codes order by id')
        for row in cursor:
            print row
        conn.close()

    
    def locate_by_postal_code(self, pc):
        """ Returns location information for the given Postal Code or None """
        conn = sqlite.connect(self.dbfile)
        c = conn.cursor()
        pc = pc.strip().upper().replace(' ', '')
        c.execute('select * from postal_codes where postal_code like "%' + pc + '%"')
        results = []
        for row in c:
            row_dict = {
                'id':row[0],
                'postal_code':row[1],
                'city':row[2],
                'province':row[3],
                'province_code':row[4],
                'city_type':row[5],
                'latitude':row[6],
                'longitude':row[7],
                'country':row[8],
                'county':row[9]
                }
            results.append(row_dict)
        conn.close()
        if len(results) > 0:
            return results
        else:
            return None
    
    def locate_by_latlon(self, latlon, decpts=2):
        """ Returns location information for the given latitude/longitude pair """
        conn = sqlite.connect(self.dbfile)
        c = conn.cursor()
        (lat, lon) = latlon
        lat_dec = len(str(lat).split('.')[1])
        lon_dec = len(str(lon).split('.')[1])
        if lat_dec <= lon_dec: ll_dec = lat_dec
        else: ll_dec = lon_dec
        if ll_dec < decpts: decpts = ll_dec
        (lat, lon) = (round(float(lat), int(decpts)), round(float(lon), int(decpts)))
        c.execute('select * from postal_codes')
        results = []
        for row in c:
            (db_lat, db_lon) = (round(float(row[6]),int(decpts)), 
                                round(float(row[7]),int(decpts)))
            if db_lat == lat and db_lon == lon:
                row_dict = {
                    'id':row[0],
                    'postal_code':row[1],
                    'city':row[2],
                    'province':row[3],
                    'province_code':row[4],
                    'city_type':row[5],
                    'latitude':row[6],
                    'longitude':row[7],
                    'country':row[8],
                    'county':row[9]
                    }
                results.append(row_dict)
        conn.close()
        if len(results) > 0:
            return results
        else:
            return None
    
    def search_database(self, city=None, province=None):
        """ Returns location information for the given City and/or Province """
        conn = sqlite.connect(self.dbfile)
        c = conn.cursor()
        
        province_code = None
        
        if province and len(province.strip()) == 2:
            province_code = province.strip().upper()
        
        cmd = 'select * from postal_codes where '
        
        if province_code:
            cmd += 'province_code like "%' + province_code + '%" '
        elif province:
            cmd += 'province like "%' + province + '%" '
        
        if city and (province or province_code):
            cmd += 'and region like "%' + city + '%" '
        elif city:
            cmd += 'region like "%' + city + '%" '
            
        c.execute(cmd)
        results = []
        for row in c:
            row_dict = {
                'id':row[0],
                'postal_code':row[1],
                'city':row[2],
                'province':row[3],
                'province_code':row[4],
                'city_type':row[5],
                'latitude':row[6],
                'longitude':row[7],
                'country':row[8],
                'county':row[9]
                }
            results.append(row_dict)
        conn.close()
        if len(results) > 0:
            return results
        else:
            return None
    
    def dump_to_file(self, filename, sep='|'):
        """ 
        Retrieves all the rows from the Postal Code table and writes them
        to a text file, delimited by 'sep'
        """
        raise NotImplementedError('dump_to_file is not yet implemented')


def print_text_output(data):
    """ Outputs the results in data as plain text on standard output """
    if not data:
        print 'no matches'
        return None
    counter = 0
    msg = ''
    for result in data:
        print """result %s
    id            :%s
    postal_code   :%s
    city          :%s
    city_type     :%s
    province      :%s
    province_code :%s
    longitude     :%4.16f
    latitude      :%4.16f
""" % (
        counter, result['id'], result['postal_code'], result['city'],
        result['city_type'], result['province'], result['province_code'],
        result['latitude'], result['longitude']
        )
        counter = counter + 1
    print 'found %s results' % len(data)
    return True

def print_xml_output(data):
    """ Output th results in data as XML on standard output """
    if not data:
        print 'no matches'
        return None
    counter = 0
    print """<?xml version="1.0" ?>
<results count="%s">""" % len(data)
    for result in data:
        print """
    <result id="%s">
        <id>%s</id>
        <postal_code>%s</postal_code>
        <city type="%s">%s</city>
        <province code="%s">%s</province>
        <latitude>%4.16f</latitude>
        <longitude>%4.16f</longitude>
    </result>""" % (
            counter, result['id'], result['postal_code'], 
            result['city_type'], result['city'], result['province_code'],
            result['province'], result['latitude'], result['longitude']
            )
        counter = counter + 1
    
    print '\n</results>'
    return True

def main():
    
    try:
    
        gloc = GeoLocation()
        
        desc = ('Look up geo. details about a postal code, city, ' +
            'province, or coordinate')
        
        epilog = ('If -a precision is greater than -r (lat/lon) precision, ' +
            'it will be set to the lesser of the lat/lon precisions. ' +
            'Currently only has infromation for Canadian postal codes.')
        
        version = '%prog version 1.0 by Matthew Brush'
        print desc
        print epilog
        print version
        
        parser = OptionParser(description=desc, version=version, epilog=epilog)
        
        parser.add_option('-d', dest='database_file', metavar='FILE',
            help='the filename of the database containing geolocation data',
            default='pcdata.db')
        parser.add_option('-p', dest='postal_code', metavar='PC',
            help='the postal code string to locate (may be partial)')
        parser.add_option('-c', dest='city', metavar='CITY',
            help='the city name to search for')
        parser.add_option('-P', dest='province', metavar='PROV',
            help='the province name or code to search for')
        parser.add_option('-r', dest='reverse', metavar='LATLON',
            help='perform a reverse lookup based on supplied lat/lon')
        parser.add_option('-a', dest='accuracy', metavar='DECPTS', type='int',
            default=2, help='lat/lon accuracy (precision) to match, default 2')
        parser.add_option('-x', dest='xml', action='store_true', default=False, 
            help='output results as XML (can be piped into an XML file).')
        
        (opts, args) = parser.parse_args()
        
        if not opts.reverse and opts.postal_code and opts.city and opts.province:
            parser.error('at least one of options -r, -c, -p, or -P is required')
        
        if opts.reverse and (opts.postal_code or opts.city or opts.province):
            parser.error('option -r cannot be used with options -p, -P, or -c')
        
        if opts.postal_code:
            results = gloc.locate_by_postal_code(opts.postal_code)
        elif opts.city or opts.province:
            results = gloc.search_database(city=opts.city, province=opts.province)
        elif opts.reverse:
            latlon = opts.reverse.split(',')
            results = gloc.locate_by_latlon(latlon, opts.accuracy)
        
        if opts.xml:
            print_xml_output(results)
        else:
            print_text_output(results)       
    except KeyboardInterrupt:
        print "caught interrupt, closing"

    return 0

if __name__ == '__main__': main()