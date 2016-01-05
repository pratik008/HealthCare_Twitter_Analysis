#!/usr/bin/env python
"""
Server for the RESTful interface to the MongoDB database
of tweets for the Healthcare Twitter Analysis project.
"""
import pymongo, bottle
from bottle import error, route, get, post, static_file, request, abort, response, template, hook
import os, json
#import cgi, re
#from urlparse import parse_qsl
from datetime import datetime
import bson.json_util

PATH           = os.path.dirname(__file__)

__author__     = 'George Fisher'
__copyright__  = "Copyright 2014, George Fisher Advisors LLC"
__credits__    = ["George Fisher"]
__license__    = "MIT"
__version__    = "0.1.0"
__maintainer__ = "George Fisher"
__email__      = "george@georgefisher.com"
__status__     = "Prototype"

# =======================
# for relative addressing
# =======================
@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')
    
@route('/js/:path#.+#', name='js')
def static(path):
    return static_file(path, root='js')
    
@route('/css/:path#.+#', name='css')
def static(path):
    return static_file(path, root='css')
    
@route('/img/:path#.+#', name='img')
def static(path):
    return static_file(path, root='img')
    
@route('/data/:path#.+#', name='data')
def data(path):
    return static_file(path, root='data')
  
# ==============  
# Error messages
# ==============
@error(404)
def error404(error):
    return "404 error: file not found %s"%error
    
# =================
# RESTful interface
# =================
"""
           url                           | verb   | action                                      | response                                    |
-----------------------------------------+--------+---------------------------------------------+---------------------------------------------+
http://localhost:8082/query/limit        | POST   | send in a query                             | a list of ids meeting the criteria, plus    |
                                                                                                |   the number of items in the list, and      |
                                                                                                |   the first full tweet meeting the criteria |
http://localhost:8082/findOne/id         | GET    | retrieve a single tweet by id               | a single tweet in json format               |       
http://localhost:8082/find/id_list       | GET    | retrieve a list of tweets for a list of ids | a list of tweets                            |
    
"""    
# allow Cross-Origin Resource Sharing
# see http://bottlepy.org/docs/dev/recipes.html#using-the-hooks-plugin
@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/query/<limit>', method="POST")
def query(limit): 
    # retrieve the json sent by browser
    data = request.json;
    
    # execute the MongoDB query, returning a list of the _id's that match
    if int(limit) <= 0:      # unlimited (limit = 0)
        id_list = [tweet for tweet in tweets.find(data,dict({"_id":1}))]
    else:                    # limited
        id_list = [tweet for tweet in tweets.find(data,dict({"_id":1})).limit(int(limit))]
        
    # how long is the list?
    num = len(id_list)
        
    # also include the first result
    example = tweets.find_one(data)
        
    # create the structure to return
    result            = dict()
    result['num']     = num
    result['id_list'] = id_list
    result['example'] = example
    
    # convert from MongoDB bson to strict json and return the result
    result = bson.json_util.dumps(result)
    return result
       
@route('/findone/<id>', method="GET")
def findOne(id):
    # convert id to MongoDB _id
    mongo_id = bson.objectid.ObjectId(id)
    
    # execute the query
    tweet    = tweets.find_one({'_id': mongo_id})
    
    # package the query response
    result                = dict()
    result['first_tweet'] = tweet
    
    # convert from MongoDB bson to strict json and return the result
    result   = bson.json_util.dumps(result)
    return result
    
@route('/find/<id_list>', method="GET")
def find(id_list):
    # convert comma-delimited string into list of MongoDB '_id's
    mongo_id_list = map(bson.objectid.ObjectId, id_list.split(','))

    # query MongoDB for the list of '_id's
    result = tweets.find({'_id': { '$in': mongo_id_list}})
    
    # convert from MongoDB bson to strict json and return
    return bson.json_util.dumps(result)
    
# =========================
# Choropleth REST interface
# =========================
@route('/choropleth/<search_term>', method="GET")
def choropleth(search_term):
    """                       
    In the $match step we filter down to what we want to aggregate:
       1. find only records containing the search_term (indexed)
       2.     in a record with country_code = "US"     (indexed)
       3.         with a non-empty FIPS field
       
    In the $group step 
      1. we GROUP BY each FIPS code
      2.     and count the number of each
    
    for a search_term of "cancer" ...
    search_results['result'][0]          == {u'_id': u'31137', u'count': 1}
    search_results['result'][0]['_id']   == u'31137'
    search_results['result'][0]['count'] == 1
    """
        
    search_results = tweets.aggregate( [
        { '$match': {'$text': {'$search': search_term}, "geo_reverse.country_code": "US", "geo_reverse.FIPS": {'$ne': ""}} },
        { '$group': { '_id': "$geo_reverse.FIPS", 'count': { '$sum': 1 } } }
      ] );
    returnedList = search_results['result']
    print  returnedList
    return bson.json_util.dumps(returnedList)

# ===============================
# Send files from the root
# ===============================
"""
Templates are stored in the views folder.
index.tpl is the html shell ... '% include' 
commands are used to pull in the various pieces
"""
@route('/')
def index():
    return template('index')
    
@route('/:path#.+#', name='root')
def static(path):
    return static_file(path, root=PATH)
    
    
# ===============================   
# Shutdown the MongoDB connection
# ===============================
@route('/exit')
def exit():
    connection.disconnect()
    return "MongoDB shut down"

# =================================== STARTUP OPERATIONS ==========================================    
    
# ========================================================     
# read the county id's from the json used to build the map
# ========================================================
f    = open("data/us.json")
line = f.readline()
f.close()
# build a set of all the county id's in the map
usjson         = json.loads(line)
countyGeomList = usjson["objects"]["counties"]['geometries']
mapIdSet = set()
for geom in countyGeomList:
    mapIdSet.add(geom['id'])
# in the choropleth REST interface we will use set operations
# to include any id's not returned from MongoDB, set to a count of zero
#
# from the documentation:
# https://docs.python.org/2/library/sets.html#set-objects
# s.difference(t)	s - t	new set with elements in s but not in t

# ===============================   
# Connect to the MongoDB database
# ===============================

connection_string = "mongodb://localhost"
connection        = pymongo.MongoClient(connection_string)

db     = connection.HTA
tweets = db.grf

# =======================   
# Connect to the Internet
# =======================

bottle.debug(True)
bottle.run(host='localhost', port=8082, reloader=True)