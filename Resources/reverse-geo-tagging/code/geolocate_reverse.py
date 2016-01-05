def geolocate_reverse(latlon):
    """
    given (lat, lon) returns reverse geo location information
    
import json
from geolocate_reverse import geolocate_reverse
result = geolocate_reverse((40.733104,-73.998458))
print json.dumps(result,indent=4)
{
    "areacode": "212", 
    "Land_Sq_Mi": 0.323, 
    "county": "New York", 
    "FIPS": "36061", 
    "state_abbr": "NY", 
    "country_code": "US", 
    "Type": "", 
    "city": "New York", 
    "country": "United States", 
    "zipcode": "10012", 
    "state": "New York", 
    "Pop_2010": 24090.0
}
    """
    import json
    import random
    from geolocate_world import *
    from geolocate_US import GeoLocation
    import sqlite3
    
    lat, lon = latlon
    lat = float(lat)
    lon = float(lon)
    
    reverse = {"country_code": "", 
               "country": "",
               "zipcode": "",
               "city": "",
               "state": "",
               "state_abbr": "",
               "areacode": "",
               "FIPS": "",
               "county": "",
               "Type": "",
               "Pop_2010": "",
               "Land_Sq_Mi": ""}
    
    US_geoinfo    = {}
    # get the world info
    world_geoinfo = get((lat,lon))
    
    if world_geoinfo:
        reverse["country"]      = world_geoinfo["country"]
        reverse["country_code"] = world_geoinfo["country_code"]
        reverse["city"]         = world_geoinfo["city"]
        if world_geoinfo['country_code'] == 'US':
            # if US, get US_geoinfo
            gl         = GeoLocation()
            US_geoinfo = gl.locate_by_latlon((str(lat),str(lon)))
            if US_geoinfo is None: 
                # if nothing, try by city name
                city_name  = world_geoinfo['city']
                US_geoinfo = gl.search_database(city=city_name)
                if US_geoinfo is None: 
                    US_geoinfo = {}
                else:
                    index = random.randint(0,len(US_geoinfo)-1)
                    US_geoinfo = US_geoinfo[index]
            else:
                index = random.randint(0,len(US_geoinfo)-1)
                US_geoinfo = US_geoinfo[index]
    else:
        world_geoinfo = {}
        
    # get the better info from my sqlite database with the FIPS codes and census data
    if US_geoinfo:
        con = None
        try:
            con = sqlite3.connect('/home/ubuntu/geocoding/ziplist5/ziplist5.sqlite')   
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        
        zipcode = US_geoinfo['postal_code']
        with con:    
            cur = con.cursor()    
            SQL = 'SELECT * FROM ziplist5 WHERE zipcode="' + zipcode + '"'
            cur.execute(SQL)
            rows = cur.fetchall()
            if rows:
                for row in rows: pass
                reverse["state"]      = US_geoinfo["province"]
                reverse["zipcode"]    = row[0]
                reverse["city"]       = row[1]
                reverse["state_abbr"] = row[2]
                reverse["areacode"]   = row[3]
                reverse["FIPS"]       = row[4]
                reverse["county"]     = row[5]
                reverse["Type"]       = row[6]
                reverse["Pop_2010"]   = row[7]
                reverse["Land_Sq_Mi"] = row[8]
            
        if con: con.close()    
            
    return reverse