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
import urllib2

error_doc_number = 0
doc_total_number = 0

entities = {}

f = open('analyse.txt','w')
for fileNumber in range (0,20): #1727):
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
            if (type(doc["_source"]["timestamp"]) is list):
                doc["_source"]['timestamp'] = doc["_source"]["timestamp"][0]
            else:
                doc["_source"]['timestamp'] = doc["_source"]["timestamp"]

            if ( "crawl_data" in doc["_source"] and  bool(doc["_source"]["crawl_data"]) ):
            	for v in doc["_source"]["crawl_data"]:
                    if ("model" in v):
                    	if v["model"] in entities:
                            duplicate = False
                            for i in entities[v["model"]]:
                                if i["_id"]==doc["_id"]:
                                    duplicate = True
                                    break
                            if duplicate == False:
                    		    entities[v["model"]].append(doc)
                    	else:
                            entities[v["model"]] = []
                            entities[v["model"]].append(doc)

entities = sorted(entities.items(), key=lambda x:len(x[1]), reverse=True)

i = 0
for k,v in entities:
    if (i==10):
        break
    i = i+1
    #f.write(k.encode('utf-8') +' '+json.dumps(v)+'\n' )
    minTimestamp = 400000000000000
    maxTimestamp = 0
    for doc in v :
        print doc["_id"]
        if doc["_source"]["timestamp"] < minTimestamp :
            minTimestamp = doc["_source"]["timestamp"]
        if doc["_source"]["timestamp"] > maxTimestamp :
            maxTimestamp = doc["_source"]["timestamp"]
    
    print maxTimestamp, ' - ', minTimestamp
    data = {"title": "Crime Warning","docs":v,"entity":k, "duration":maxTimestamp-minTimestamp}

    req = urllib2.Request('http://localhost:3000/crimeWarning')
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))
f.close()


