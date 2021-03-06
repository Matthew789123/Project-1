from django.urls import path

from . import views

import http

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("rand/", views.rand, name="rand")
]
