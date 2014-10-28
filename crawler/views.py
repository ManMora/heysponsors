from django.shortcuts import render
import urllib
import json
from bs4 import BeautifulSoup
import requests
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt


class result():
    def __init__(self, name=None, logo=None, tel=None, email=None, direccion=None):
        self.name = name
        self.logo = logo
        self.tel = tel
        self.email = email
        self.direccion = direccion

@csrf_exempt
def gettags(request):
    if request.POST != None and request.POST.get('url') != None:
        print("HOLA!")
        print(request.POST.get('url'))
        htmlfile = urllib.urlopen(request.POST.get('url'))
        soup = BeautifulSoup(htmlfile)
        print("hola")
        results = []
        vcards = soup.find_all("li", class_="vcard")

        for x in vcards:
            if x.span['class'] != None and x.span['class'] == 'street-address':
                addr = x.span.string
            else:
                addr = None
            a = x.find_all("span",class_="tel")
            if len(a) > 0:
                tel = a[0].string

            b = x.find_all("span",class_="street-address")
            if len(b)>0:
               addr = b[0].string

            if x.img != None:
               img = x.img['src']
            else:
               img = None

            results.append(result(x.h3.a.string,img,tel,None,addr))
            print(results)
        return HttpResponse(json.dumps([dict(result=x.__dict__) for x in results]), content_type="application/json")
    return HttpResponse(json.dumps(None), content_type="application/json")

