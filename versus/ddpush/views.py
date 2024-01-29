from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import UploadFileForm
from django.http import HttpResponseRedirect

#RESTful api
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from social_django.utils import psa

#REDIS
from django.core.cache import cache


from django.views.decorators.csrf import csrf_exempt

import requests,json
import os, dotenv

from .Tools import handle_log_text,handle_log_json,preprocess_and_load , handle_uploaded_file, handle_push


dotenv.load_dotenv()

# Create your views here.

#datadog rest api
api_key = os.environ.get('dd_api_key')
url = "https://http-intake.logs.datadoghq.com/v1/input/"+api_key
headers = {
        "Content-Type": "application/json",
}



# ddpush/
@login_required
def index(request):
    return render(request, 'ddpush/index.html')


# ddpush/log/
@login_required
def log(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'],request.POST,url,headers)
            return HttpResponseRedirect('/ddpush/log/')
    else:
        form = UploadFileForm()
    return render(request, 'ddpush/upload.html',{'form': form})




 
# ddpush/log/text/
@api_view(['GET','POST'])
def log_text(request):
    row = request.body.decode('utf-8')
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        Token.objects.get_or_create(user=request.user)
        handle_log_text.delay(row, client_ip, url, headers)
        #handle_log_text(row, client_ip, url, headers)
        res = {
            "status" : "Queue push success"
        }
        return JsonResponse(res)

    except Exception as e:
        res = {
            "status" : f"{e}"
        }
        return JsonResponse(res)


# ddpush/log/json/
@api_view(['GET','POST'])
def log_json(request):
    row = request.body.decode('utf-8')
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        Token.objects.get_or_create(user=request.user)
        json_row = preprocess_and_load(row)
        tag = json_row.get('tag')
        logs = json_row.get('log')
        if tag ==None : tag = f"api.sec,ddpush/log/josn/"
        if logs == None: logs = json_row

        handle_log_json.delay(row, client_ip, url, headers)
        #handle_log_json(row, client_ip, url, headers)
        res = {
            "status" : "Queue push success"
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status" : f"{e}"
        }
        return JsonResponse(res)


# ddpush/log/yaml/
@api_view(['GET','POST'])
def log_yaml(request):
    cache.set('my_key', 'hello, world!', 300)
    value = cache.get('my_key')
    data = {"redis":value}
    return JsonResponse(data)


# ddpush/log/file
# /
@api_view(['POST'])
def log_file(request):
    #case:1 로그데이터가 yaml 형태로 왔을 때
    data = {}
    return JsonResponse(data)



# ddpush/event/
def event(request):
    cert = request.GET.get('event')
    data = {"message": f"{cert}"}
    return JsonResponse(data)




# Token 유지를 위해 필요
@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    token = request.GET.get('access_token')
    user = request.backend.do_auth(token)

    if user:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key})  # or HttpResponse or whatever
    else:
        return HttpResponseBadRequest('Bad Token')




def push(request):
    try:
        n=0
        while n<30000:
            handle_push.delay(n)
            n = n + 1
        res = {
            "status" : "Queue push success"
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status" : f"{e}"
        }
        return JsonResponse(res)