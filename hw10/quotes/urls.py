# from django.shortcuts import render
from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main_view, name="main"),
    path("<int:page>", views.main_view, name="main_paginate"),
    path("<int:page>/<str:tag_name>", views.main_view_tag, name="main_tag"),
    path('tag/', views.tag_change, name='tag'),
    path('author/', views.author_change, name='author'),
    path('authorshow/<int:author_id>', views.author_show, name='author_show'),
    path('quote/', views.quote_change, name='quote'),
]
