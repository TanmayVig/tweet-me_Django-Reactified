from django.contrib import admin
from django.urls import path
from .views import (home_view, 
                            tweet_list_view, 
                            tweet_detail_view, 
                            tweet_create_view,
                            tweet_delete_view,
                            tweet_action_view)

app_name = 'tweet_api'

urlpatterns = [
    path('',tweet_list_view,name = "tweet_list"),
    path('action/',tweet_action_view),
    path('create/',tweet_create_view,name="tweet-form"),
    path('<int:tweet_id>/', tweet_detail_view,name = "tweet_single"),
    path('<int:tweet_id>/delete/', tweet_delete_view,name = "delete"),
]