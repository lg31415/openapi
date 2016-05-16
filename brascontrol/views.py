from django.shortcuts import render , render_to_response
from django.http  import HttpResponse

# Create your views here.
def BrasSendBreaker(request):
    response = HttpResponse("I am OK!")
    return HttpResponse( response , content_type='application/json')
def BrasSendLocker(request):
    response = HttpResponse("I am OK!")
    return HttpResponse( response , content_type='application/json')
