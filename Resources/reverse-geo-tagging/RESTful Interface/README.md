Healthcare Twitter Analysis website
===================================

This is a single-page web app which provides internet access to the MongoDB database for the Healthcare Twitter Analysis project. ~5 million geo-tagged twitter json documents are available via the web page and via the RESTful interface.

bottle_server.py is the HTTP server at the center
----------------
- it talks to MongoDB on the server-side using Pymongo
- it sends out the initial web page to the client browser
- it implements a RESTful interface for the web page and any other users

\views\index.tpl is the main HTML shell
----------------

The \views folder contains web-page templates. The 'index.tpl' shell is filled in using '% include()' template commands for each interior section of the webpage, pulling in each section in order. This allows an increasingly-large SPA to be managed in smaller functional sections.

On the client-side the main technologies are jQuery and D3.js; on the server-side, Bottle, Python and MongoDB. A Python HTTP server was chosen because of the ongoing need to do analytical programming as part of the RESTful interface.