# from django.shortcuts import render,render_to_response
#-*-coding:utf-8-*-
from django.http  import HttpResponse
from ipip import IP
import os,json,httplib
# Create your views here.
def Get_Client_Ip(request):
    try:
      real_ip = request.META['HTTP_X_FORWARDED_FOR']
      regip = real_ip.split(",")[0]
    except:
      try:
        regip = request.META['REMOTE_ADDR']
      except:
        regip = ""
    return regip
def IpQuery(req):
    IP.load(os.path.abspath("mydata4vipweek2.dat"))
    Key=['country','province','city','county','isp','ip']
    Result=IP.find(Get_Client_Ip(req)).split('\t')
    Result.append(Get_Client_Ip(req))
    Mesage=dict(zip(Key,Result))
    return HttpResponse(json.dumps(Mesage, ensure_ascii=False))
def GetArea(req):
    IP.load(os.path.abspath("mydata4vipweek2.dat"))
    Key=['country','province','city','county','isp','ip']
    # Area=IP.find(Get_Client_Ip(req)).split('\t')
    Area=IP.find('202.99.224.68').split('\t')
    Area.append(Get_Client_Ip(req))
    ResultStr=''
    Mesage=dict(zip(Key,Area))
    for key in Mesage.keys():
        Key=Mesage[key].decode("utf8")
        # ResultStr=ResultStr+key+"="+Mesage[key]+ ','
        ResultStr=ResultStr+key+"="+Key+ ','
        # ResultStr=''
    return ResultStr
def Http_Push_Json(host,port,url,body):
    try:
        headers = {"Content-type": "application/json",
                   "Connection": "keep-alive",
                   }
        httpClient = httplib.HTTPConnection(host, port, timeout=60)
        httpClient.request("POST", url, body, headers)
        response = httpClient.getresponse()
        return response.read()
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
    return
def MetricPush(req):
    ResponseJson=''
    try:
        MetricJsonMesage=''
        if req.method == 'POST':
            for JsonString in  json.loads(req.body):
                JsonString['tags']=JsonString['tags']+GetArea(req)
                if MetricJsonMesage <>"":
                    MetricJsonMesage= MetricJsonMesage+','+json.dumps(JsonString)
                elif MetricJsonMesage =="":
                    MetricJsonMesage=MetricJsonMesage+json.dumps(JsonString)
                elif len(MetricJsonMesage)>65536:
                    MetricJsonMesage="["+MetricJsonMesage+"]"
                    MetricJsonMesage=''
            MetricJsonMesage="["+MetricJsonMesage+"]"
            ResponseJson=Http_Push_Json('192.168.11.202','6060','/api/push',MetricJsonMesage)
            print MetricJsonMesage
            # return HttpResponse(MetricJsonMesage, content_type="application/json")
    except:
        import sys
        print(sys.exc_info()[0], sys.exc_info()[1])
    return HttpResponse( ResponseJson , content_type='application/json')
