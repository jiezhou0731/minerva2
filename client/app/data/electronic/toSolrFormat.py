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


socket.setdefaulttimeout(3)
error_doc_number = 0
doc_total_number = 0
domains = {}

for fileNumber in range (0,1727):
    with open("dump/"+str(fileNumber)+".json") as json_file:
        f = open('toSolr/'+str(fileNumber)+'.json','w')
        f.write("[")
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
            if (doc["_source"]["url"] is list):
                d['url'] = doc["_source"]["url"][0]
            else:
                d['url'] = doc["_source"]["url"]

            d['url'] = ''.join(d['url'])
            d['url'] = d['url'].partition('?')[0]

            if (doc["_source"]["timestamp"] is list):
                d['timestamp'] = doc["_source"]["timestamp"][0]
            else:
                d['timestamp'] = doc["_source"]["timestamp"]
            url =  d['url']
            html = unicode(doc["_source"]["raw_content"])
            parsed_uri = urlparse( url )
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

            if domain in domains:
                if domains[domain]>=1000 or (not "crawl_data" in doc["_source"]) or( "crawl_data" in doc["_source"] and not bool(doc["_source"]["crawl_data"])):
                    continue
                domains[domain] = domains[domain]+1
            else:
                domains[domain] = 1

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
            docCount = docCount + 1
            if docCount!=1: f.write(",")
            f.write(json.dumps(d).encode('utf-8'))
            
        f.write("]")
        f.close()


'''
doc = json_data["hits"]["hits"][0]["_source"]["raw_content"].encode('utf-8')
print doc

print "############################################"
soup = BeautifulSoup(''.join(doc),"html.parser")
print soup.getText()

f = open('processed.txt','w')
#f.write(soup.getText(separator=u' ').encode('utf-8'))
f.close()


#print soup.title
#print soup.prettify()
'''