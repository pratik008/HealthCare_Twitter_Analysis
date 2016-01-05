DROP TABLE IF EXISTS ziplist5;
# import from ziplist5pop.csv ... modified from ziplist5.txt to include only preferred names
CREATE TABLE ziplist5(
zipcode         TEXT PRIMARY KEY,
city            TEXT, 
state           TEXT,
areacode        TEXT,
FIPS            TEXT,
county          TEXT,
Type	        TEXT,
Pop_2010        REAL,
Land_Sq_Mi      REAL
);