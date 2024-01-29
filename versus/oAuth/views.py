from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from social_django.utils import psa

from django.views.decorators.csrf import csrf_exempt

import requests,json
import os, dotenv

@login_required
#@api_view(['GET'])
def index(request):
    try:
        token, _ = Token.objects.get_or_create(user=request.user)
        data = {"message": "Token create!", "token": token.key}
        return JsonResponse(data)
    except Exception as e:
        print(e)
        data = {"message": "Token fail"}
        return JsonResponse(data)



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


class ObtainAuthToken(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None or not user.is_active:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})