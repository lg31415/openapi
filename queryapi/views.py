# from django.shortcuts import render,render_to_response
#-*-coding:utf-8-*-
from django.http  import HttpResponse
from ipip import IP
from queryapi.models import AreaCode
from collections import OrderedDict
import os,json,httplib
# Create your views here.
def Get_Client_Ip(request):
    try:
      real_ip = request.META['HTTP_X_FORWARDED_HOST']
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
    Code=''
    Mesage=dict(zip(Key,Area))
    # print Mesage
    for key in Mesage.keys():
        if  key=='country':
            CodeValue=Get_Area_Code(Mesage[key],'COUNTRY')
        elif key=='province':
            CodeValue=Get_Area_Code(Mesage[key],'PROVINCE')
        elif key=='city':
            CodeValue=Get_Area_Code(Mesage[key],'CITY')
        elif key=='county':
            CodeValue=Get_Area_Code(Mesage[key],'COUNTY')
        elif key=='isp':
            CodeValue=Get_Area_Code(Mesage[key],'ISP')
        elif key=='ip':
            CodeValue=Mesage[key]
        if key in ['province','city','isp','ip']:
             ResultStr=ResultStr+key+"="+CodeValue+ ','
    return ResultStr
def GetAreaName(req):
    IP.load(os.path.abspath("mydata4vipweek2.dat"))
    Key=['country','province','city','county','isp','ip']
    Area=IP.find(Get_Client_Ip(req)).split('\t')
    Area.append(Get_Client_Ip(req))
    Mesage=dict(zip(Key,Area))
    ResultStr=''
    for key in Mesage.keys():
        if key in ['province','city','isp','ip']:
             ResultStr=ResultStr+key+"="+Mesage[key]+ ','
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
        MetricJsonMesage=""
        if req.method == 'POST':
            for JsonString in  json.loads(req.body):
                JsonString['tags']=JsonString['tags']+GetAreaName(req)
                # JsonString['tags']=JsonString['tags']+GetArea(req)
                if MetricJsonMesage <>"":
                    MetricJsonMesage= MetricJsonMesage+','+json.dumps(JsonString)
                elif MetricJsonMesage =="":
                    MetricJsonMesage=MetricJsonMesage+json.dumps({'endpoint':JsonString['endpoint'],'metric':JsonString['metric'],'value':JsonString['value'],'step':JsonString['step'],'counterType':JsonString['counterType'],'tags':JsonString['tags'],'timestamp':JsonString['timestamp']})
                elif len(MetricJsonMesage)>65536:
                    MetricJsonMesage="["+MetricJsonMesage+"]"
                    ResponseJson=Http_Push_Json('192.168.11.202','6060','/api/push',MetricJsonMesage)
                    HttpResponse( ResponseJson , content_type='application/json')
                    MetricJsonMesage=''
            MetricJsonMesage="["+MetricJsonMesage+"]"
            ResponseJson=Http_Push_Json('192.168.11.202','6060','/api/push',MetricJsonMesage)
            print MetricJsonMesage
            # return HttpResponse(MetricJsonMesage, content_type="application/json")
    except:
        import sys
        print(sys.exc_info()[0], sys.exc_info()[1])
    return HttpResponse( ResponseJson , content_type='application/json')
def Get_Area_Code(AreaName,Areatype):
    try:
        # print AreaName,Areatype
        Data=AreaCode.objects.get(area_name=AreaName,area_type=Areatype)
        return Data.area_code
    except:
        return ''