import random
from django.views.decorators.csrf import csrf_exempt
from tweetme.settings import ALLOWED_HOSTS
from django.utils.http import is_safe_url
from django.conf import settings
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from . models import Tweet
from .forms import TweetForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request,'pages/home.html',context={},status=200)

# @csrf_exempt
def tweet_create_view(request, *args, **kwargs):
    # print("ajax",request.is_ajax())
    form = TweetForm(request.POST or None)
    # print(form.data)
    next_url = request.POST.get("next") or None
    # print(form.is_valid)
    if form.is_valid():
        obj = form.save(commit=False)
        # do something in form
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

def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        'isUser':False,
        'response': tweets_list,
    }
    return JsonResponse(data)

def tweet_detail_view(request, tweet_id, *args, **kwargs):
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
