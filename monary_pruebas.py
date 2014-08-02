from monary import Monary
import numpy

with Monary("127.0.0.1") as monary:
    arrays = monary.query(
                          "HealthCare_Twitter_Analysis",                         # database name
                          "tweets",                   # collection name
                          {},                             # query spec
                          ["n-grams.text"], # field names (in Mongo record)
                          ["float64"]                # Monary field types (see below)
                          )

print arrays[0]