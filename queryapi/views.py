# from django.shortcuts import render,render_to_response
from django.http  import HttpResponse
from ipip import IP
import json,os
# Create your views here.
def get_client_ip(request):
    try:
      real_ip = request.META['HTTP_X_FORWARDED_FOR']
      regip = real_ip.split(",")[0]
    except:
      try:
        regip = request.META['REMOTE_ADDR']
      except:
        regip = ""
    return regip
def ipquery(req):
    IP.load(os.path.abspath("mydata4vipweek2.dat"))
    Key=['country','province','city','county','isp','ip']
    Result=IP.find(get_client_ip(req)).split('\t')
    Result.append(get_client_ip(req))
    Mesage=dict(zip(Key,Result))
    return HttpResponse(json.dumps(Mesage, ensure_ascii=False))