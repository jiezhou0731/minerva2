# -*- coding: UTF-8 -*-
#!/usr/bin/python

import re
import json
import requests
from requests.auth import HTTPBasicAuth
from urlparse import urlparse
from urlparse import urljoin
import urllib
import os.path
import socket

error_doc_number = 0
doc_total_number = 0

entities = {}

f = open('analyse.txt','w')
for fileNumber in range (0,10): #1727):
    with open("dump/"+str(fileNumber)+".json") as json_file:
        json_data = json.load(json_file)
        docCount=0
        

        # For each document in the json file
        for doc in json_data["hits"]["hits"]:
            print  "Complete: "+"%.2f" % (doc_total_number/17270.0) +" Error rate: "+  "%.2f" % (100.0*error_doc_number*0.1/(1.0*(doc_total_number+1.0))) +" Total: " + str(doc_total_number) +" Error: " + str(error_doc_number)

            doc_total_number = doc_total_number + 1
            #if not ("crawl_data" in doc["_source"] and ("crawl_data" in doc["_source"])):
            #    continue

            # d is what will be transfered to solr system
            if ( "crawl_data" in doc["_source"] and not bool(doc["_source"]["crawl_data"]) ):
            	for k,v in doc["_source"]["crawl_data"] :
            		if ("model" in v):
            			if v.model in entities:
            				entities[v.model] = entities[v.model]+1
            			else:
            				entities[v.model] = 1

for k,v in entities.items():
    print k, ' : ', v 
f.close()


'''
data = {"title": "python python python python"}

req = urllib2.Request('http://localhost:3000/crimeWarning')
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))
'''