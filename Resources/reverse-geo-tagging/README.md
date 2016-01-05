Healthcare Twitter Analysis  
===========================  

#### The use of social media data and data science to gain insights into health care and medicine. 

The current **status report** is in the main folder and you would do well to start by at least skimming it. 

[![DOI](https://zenodo.org/badge/5738/grfiv/healthcare_twitter_analysis.png)](http://dx.doi.org/10.5281/zenodo.11426)

-------------------------------
####RESTful interface to the MongoDB database

Under the `RESTful Interface` folder you will find the entire file structure required to run a Chrome web browser app that makes queries to a MongoDB database with all of the project's ~4 million json documents.

The instructions for running the project after you have installed the files  are under the `Instructions` tab of the main web page `HTAinterface.html` which you can simply load into your Chrome browser (Ctrl+o). The most-current instructions are contained here and will be updated as the project evolves.

The Status Report has a section with some of the technical details of Bottle, jQuery and Ajax

-------------------------------
####The Status Report `Status Report.pdf` in the main folder
 
- a comprehensive explanation of the dataset  
- examples of analyses done with this dataset  
- a list of references to other healthcare-related Twitter analyses  
- instructions for using Amazon Web Services
- sample programs using this file with Python, R and MongoDB.
- technical details of the RESTful interface. 


-------------------------------
####Complete dataset of the tweets for this project

All of the tweets for this project have been processed and consolidated into a single file that can be downloaded with this link:

- https://s3-us-west-2.amazonaws.com/healthcare-twitter-analysis/HTA_noduplicates.gz  
1.85 Gb zipped / 15.80 Gb unzipped  


Each of the 4 million rows in this file is a tweet in json format.

* Every record contains the following information:
    - All the Twitter data in exactly the json format of the original  
    - Unix time stamp  
    - data from the original files:  
        - originating file name  
        - score  
        - author screen name  
        - URLs  


* In addition, 60% of the records have geographic information
    - Latitude & Longitude  
    - Country name & ISO2 country code  
    - City  
    - For country code "US"  
      - Zipcode  
      - Telephone area code  
      - Square miles inside the zipcode  
      - 2010 Census population of the zipcode  
      - County & FIPS code  
      - State name & USPS abbreviation   

The basic technique for using this file in Python is the following:


    import json
    
    with open("HTA_noduplicates.json", "r") as f:
        # convert each row in turn into json format and process
        for row in f:
            tweet = json.loads(row)
            text  = tweet["text"]      # text of original tweet
            ...                        # etc.
            

The Status Report includes instructions for loading the json text file into a MongoDB database collection; I keep mine on an external hard drive and I start the MongoDB server as follows:

    mongod --dbpath "E:\HTA"

The database is HTA and the collection is grf. In that case the Python code would look like this:

    import json
    from pymongo import MongoClient

    # start up MongoDB
    # ================
    client = MongoClient()  # assuming you have the MongoDB server running ...

    db     = client['HTA']   # reference the database
    tweets = db.grf          # reference the collection

    for tweet in tweets.find():
        text  = tweet["text"]
        if tweet['geo']:
            (...)

