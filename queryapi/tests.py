from django.http import HttpResponse
from json import loads, dumps
def json_response(request):
    dic = {}
    try:
        if request.method == 'POST':
            print('post info: ', request.body)
            jstr = loads((request.body).decode())
            print(jstr)
            return HttpResponse(jstr, content_type="application/json")
    except:
        import sys
        print(sys.exc_info()[0], sys.exc_info()[1])

    dic['message'] = "A beautiful json string response."
    dic['create_at'] = str(ctime())
    jstr = dumps(dic)
    return HttpResponse(jstr, content_type='application/json')