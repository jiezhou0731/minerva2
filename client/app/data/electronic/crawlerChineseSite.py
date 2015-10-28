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
import time


def has_background_attribute(tag):
    return tag.has_attr('background')

socket.setdefaulttimeout(3)

f = open('cn.json','w')
doc_total_number = 0
error_doc_number = 0
url = "http://old.infineom.com"
nextUrl = "http://old.infineom.com/elecview/MOTOROLA/171119.html"

f.write("[")
while doc_total_number<101:
    try :
        currentUrl = nextUrl
        page=urllib2.urlopen(nextUrl)
        soup = BeautifulSoup(page.read(), "lxml")

        for elem in soup(text=re.compile(u'上一条库存')):
            nextUrl = urljoin(url,elem.parent.findAll('a')[0]['href'])
            print nextUrl

        d = {}
        d['id'] = 'gucn'+str(doc_total_number)
        d['_type'] = 'electronics'
        d['url'] = currentUrl
        d['timestamp'] = int(time.time()*1000)
        d['title'] = soup.title.text
        [s.extract() for s in soup('script')]
        d['content'] = soup.getText()

        parsed_uri = urlparse( currentUrl )
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
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
            try :
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))

                if not os.path.isfile(filename):
                    urllib.urlretrieve (cssUrl, filename)
            except:
                pass


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
            try :
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))

                if not os.path.isfile(filename):
                    urllib.urlretrieve (imageUrl, filename)
            except:
                pass

        anchors = soup.findAll('a')
        # For each anchor
        for anchor in anchors:
            if not anchor['href'].startswith('http'):
                anchor['href'] = urljoin(url,anchor['href'])

        if doc_total_number != 0 :
            f.write(',')

        
        for background in soup.find_all(has_background_attribute) :
            background['background'] = "electronic/images/"+domain+"/"+urlparse( background['background'] ).path

        d['html'] = soup.prettify()
        f.write(json.dumps(d).encode('utf-8'))

        doc_total_number=doc_total_number+1
    except:
        pass

f.write("]")
f.close()

