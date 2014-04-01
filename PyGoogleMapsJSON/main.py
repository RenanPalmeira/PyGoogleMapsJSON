#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
import sys
import json
import urllib
import StringIO
from jinja2 import Environment, FileSystemLoader
from wsgiref.simple_server import make_server

folder = os.path.dirname(os.path.abspath(__file__))

url=lambda name: "http://maps.google.com/maps/api/geocode/json?" + (urllib.urlencode({'address':(name),'sensor':'false'}))


def template(**kwargs):
    var=kwargs
    j2_env = Environment(loader=FileSystemLoader(folder),trim_blocks=True)
    return j2_env.get_template('template.html').render(var)
    
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
       address=result['results'][0]['address_components'][0]['short_name']
       return [lat,lng,address]

if __name__=='__main__':
    host='localhost'
    port=5000
    
    user=raw_input("Digite Um Endereço:")
    
    if GoogleMap(user):
        lat,lng,title=GoogleMap(user)
        def app(env,res):
            res('200 OK',[('Content-type','text/html')])
            address=template(title=title,x=lat,y=lng)
            return [address.encode('utf-8')]
        
        print "* Running http://%s:%s" % (host,port)
        server=make_server(host,port,app)
        server.serve_forever()
    
    else:
        print "Nenhum Endereço Encontrado"