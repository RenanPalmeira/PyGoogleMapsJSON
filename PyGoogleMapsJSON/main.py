#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import json
import urllib
import StringIO
from wsgiref.simple_server import make_server

url=lambda name: "http://maps.google.com/maps/api/geocode/json?" + (urllib.urlencode({'address':(name),'sensor':'false'}))
def GoogleMap(user):
    pattern=url(str(user))
    
    request=urllib.urlopen(pattern).read()
    
    body=StringIO.StringIO(request)
    
    result=json.load(body)
    
    if 'status' not in result or result['status'] != 'OK':
        return None
        
    else:
       lat=result['results'][0]['geometry']['location']['lat']
       lng=result['results'][0]['geometry']['location']['lng']
       return str((lat,lng))
    
    
if __name__=='__main__':
    host='localhost'
    port=5000
    
    user=raw_input("Digite um endereço:")
    address=GoogleMap(user)
    
    def app(env,res):
        res('200 OK',[('Content-type','text/html')])
        return address
    
    
    print "* Running http://%s:%s" % (host,port)
    
    server=make_server(host,port,app)
    server.handle_request()
    