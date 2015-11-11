# -*- coding: UTF-8 -*-
#!/usr/bin/python

from bs4 import BeautifulSoup
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
for fileNumber in range (0,100):
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
            d={"cdr_data":""}
            d['cdr_data'] = json.dumps(doc["_source"])
            d['_index'] = str(doc["_index"])
            d['_type'] = str(doc["_type"])
            d['id'] = str(doc["_id"])
            if (type(doc["_source"]["url"]) is list):
                d['url'] = doc["_source"]["url"][0]
            else:
                d['url'] = doc["_source"]["url"]

            d['url'] = ''.join(d['url'])
            d['url'] = d['url'].partition('?')[0]

            if (type(doc["_source"]["timestamp"]) is list):
                d['timestamp'] = doc["_source"]["timestamp"][0]
            else:
                d['timestamp'] = doc["_source"]["timestamp"]
            url =  d['url']
            html = unicode(doc["_source"]["raw_content"])
            parsed_uri = urlparse( url )
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

            try:
                soup = BeautifulSoup(''.join(html),"html.parser")
                d['content'] = soup.getText()
                d['title'] = str(soup.title.text)
                cssLinks = soup.findAll('link')
                # For each image in the document
                for css in cssLinks:
                    if not css['href'].startswith('http'):
                        cssUrl = urljoin(url,css['href'])
                        filename = "images/"+domain+"/"+urlparse(cssUrl).path
                    else:
                        cssUrl = css['href']
                        filename =  urlparse(css['href']).path
                    css['href'] = "electronic/"+filename
                    # If the image is not exist, then download it.
                    if not os.path.exists(os.path.dirname(filename)):
                        os.makedirs(os.path.dirname(filename))

                    if not os.path.isfile(filename):
                        urllib.urlretrieve (cssUrl, filename)

                images = soup.findAll('img')
                # For each image in the document
                for img in images:
                    if not img['src'].startswith('http'):
                        imageUrl = urljoin(url,img['src'])
                        filename = "images/"+domain+"/"+urlparse(imageUrl).path
                    else:
                        imageUrl = img['src']
                        filename =  urlparse(img['src']).path
                    img['src'] = "electronic/"+filename
                    # If the image is not exist, then download it.
                    if not os.path.exists(os.path.dirname(filename)):
                        os.makedirs(os.path.dirname(filename))

                    if not os.path.isfile(filename):
                        urllib.urlretrieve (imageUrl, filename)

                anchors = soup.findAll('a')
                # For each anchor
                for anchor in anchors:
                    if not anchor['href'].startswith('http'):
                        anchor['href'] = urljoin(url,anchor['href'])

                d['html'] = soup.prettify()
            except Exception,e: 
                d['html'] = html
                error_doc_number = error_doc_number+1
                print e
                continue

            if ( "crawl_data" in doc["_source"] and  bool(doc["_source"]["crawl_data"]) ):
            	for v in doc["_source"]["crawl_data"]:
                    if ("model" in v):
                    	if v["model"] in entities:
                            duplicate = False
                            for i in entities[v["model"]]:
                                if i["id"]==doc["_id"]:
                                    duplicate = True
                                    break
                            if duplicate == False:
                    		    entities[v["model"]].append(d)
                    	else:
                            entities[v["model"]] = []
                            entities[v["model"]].append(d)

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
        if doc["timestamp"] < minTimestamp :
            minTimestamp = doc["timestamp"]
        if doc["timestamp"] > maxTimestamp :
            maxTimestamp = doc["timestamp"]
    
    print maxTimestamp, ' - ', minTimestamp
    data = {"title": "Crime Warning","docs":v,"entity":k, "duration":maxTimestamp-minTimestamp}

    req = urllib2.Request('http://localhost:3000/crimeWarning')
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))
f.close()


