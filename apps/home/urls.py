# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('audio', views.audio_upload, name='audio'),
    path('cloud',views.cloud_retrieval,name='cloud'),
    path('video', views.video_upload, name='video'),
    path('forum', views.disussion,name='forum'),
    path('analysis/<str:id>/', views.get_time, name='analysis'),
    path('v_analysis/<str:id>/', views.new_get_time, name='v_analysis'),



    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
