import json
import random
from django.views.decorators.csrf import csrf_exempt
from tweetme.settings import ALLOWED_HOSTS
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from . models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request,'pages/home.html',context={},status=200)

@api_view(['POST']) # http method allowed
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    data = request.POST
    serializer = TweetSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = request.user)
        return Response(serializer.data, status= 201)

    return Response({}, status= 400)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many= True)
    return Response(serializer.data)

@api_view(['GET'])
def tweet_detail_view(request, *args, **kwargs):
    qs = Tweet.objects.filter(id = tweet_id)
    if not qs:
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data,status=200)




# @csrf_exempt
def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({},status = 401)
        return redirect(settings.LOGIN_URL)
    # print("ajax",request.is_ajax())
    form = TweetForm(request.POST or None)
    # print(form.data)
    next_url = request.POST.get("next") or None
    # print(form.is_valid)
    if form.is_valid():
        obj = form.save(commit=False)
        # do something in form
        obj.user = user #anonymous user also allowed
        obj.save()
        
        if request.is_ajax():
            return JsonResponse(obj.serialize(),status = 201) # 201 == created items
        if next_url != None and is_safe_url(next_url,ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors,status = 400)
    return render(request, 'components/form.html',context={'form':form})

def tweet_list_view_pure_django(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        'isUser':False,
        'response': tweets_list,
    }
    return JsonResponse(data)

def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    '''
    REST API VIEW
    return json data
    '''
    data={
        'id': tweet_id,
        # 'content':obj.content,
        # 'image_path':obj.img.url
    }
    status = 200
    try:
        obj = Tweet.objects.get(id = tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status = 404
   
    return JsonResponse(data,status = status)
