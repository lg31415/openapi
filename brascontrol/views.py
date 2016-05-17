#-*-coding:utf-8-*-
# from django.shortcuts import render , render_to_response
from django.http  import HttpResponse
import paramiko,telnetlib,json
DeviceList=[{'name':'Device-001','host':'127.0.0.1','port':'22','username':'admin','password':'123456','protocol':'SSH2','brand':'ZTE'},
            {'name':'Device-002','host':'192.168.11.202','port':'23','username':'admin','password':'123456','protocol':'TELNET','brand':'H3C'}]

def BrasSendCmd(request,active):
    DeviceParams = request.GET.get('device')
    InfoParams = GetDeviceInfo(DeviceParams)
    cmd=CreateCmd(InfoParams['brand'],active)
    if InfoParams['protocol']=='TELNET':
        try:
            print TelnetHost(InfoParams['host'],InfoParams['port'],InfoParams['username'],InfoParams['password'],cmd,'')
            response = HttpResponse(json.dumps({'result':'0','message':'OK'}))
        except Exception,e:
            response = HttpResponse(json.dumps({'result':'1','message':'Fail'}))
            print e
    elif InfoParams['protocol']=='SSH2':
        try:
            print SSH2Host(GetDeviceInfo['host'],GetDeviceInfo['port'],GetDeviceInfo['username'],GetDeviceInfo['password'],cmd)
            response = HttpResponse(json.dumps({'message':'OK','result':'0'}))
        except Exception,e:
            response = HttpResponse(json.dumps({'message':'Fail','result':'1'}))
            print e
    return HttpResponse( response , content_type='application/json')
def GetDeviceInfo(device):
    for DeviceInfo in DeviceList:
        if device==DeviceInfo['name']:
            result= {'host':DeviceInfo['host'],'port':DeviceInfo['port'],'username':DeviceInfo['username'],'password':DeviceInfo['password'],'protocol':DeviceInfo['protocol'],'brand':DeviceInfo['brand']}
    return  result
def TelnetHost(host,port,username,password,command,finishtag = ':~$'):
    #连接Telnet服务器
    HostConnection = telnetlib.Telnet(host,port)
    #输入登录用户名
    # HostConnection.read_until('login: ')
    HostConnection.write(username + '\n')
    #输入登录密码
    # HostConnection.read_until('Password: ')
    HostConnection.write(password + '\n')
    #登录完毕后，执行ls命令
    for cmd in command:
        HostConnection.read_until(finishtag)
        # print cmd+'\n'
        HostConnection.write(cmd+'\n')
    #ls命令执行完毕后，终止Telnet连接（或输入exit退出）
    HostConnection.read_until(finishtag)
    return  HostConnection.read_very_lazy()
    HostConnection.close()
    #tn.write('exit\n')
def SSH2Host(ip,port,username,password,command):
    try:
        HostConnection = paramiko.SSHClient()
        HostConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        HostConnection.connect(ip,port,username,password,timeout=10)
        for m in command:
            stdin,stdout,stderr = HostConnection.exec_command(m)
            #stdin.write("Y")   #简单交互，输入 ‘Y’
            out = stdout.readlines()
            #屏幕输出
            for o in out:
                print o,
        return '%s\tOK\n'%(ip)
        HostConnection.close()
    except :
        return '%s\tError\n'%(ip)
def CreateCmd(brand,Active):
    if brand=='ZTE' and Active=='free':
        return ['configure terminal','ipv4-access-list acl_portal_web', 'no rule 1','!','end','exit']
    elif brand=='H3C' and Active=='free':
        return [ 'interface Reth44','no ip policy-based-route vip','no portal enable method direct'
            ,'no portal domain 51iwifi.com','no portal bas-ip 183.131.101.4','no portal apply web-server wziwifi'
            ,'no portal apply mac-trigger-server imc ']
    elif brand=='ZTE' and Active=='lock':
        return ['configure terminal','ipv4-access-list acl_portal_web', 'rule 1 permit ip any any','!','end','exit']
    elif brand=='H3C' and Active=='lock':
        return [ 'interface Reth44','ip policy-based-route vip','portal enable method direct','portal domain 51iwifi.com',
                 'portal bas-ip 183.131.101.4','portal apply web-server wziwifi','portal apply mac-trigger-server imc ']
    else:
        return []
