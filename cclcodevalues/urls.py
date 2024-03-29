"""cclcodevalues URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.templatetags.static import static # Not from django.conf.urls.static 
from django.views.generic.base import RedirectView
from .views import (
    homepage,
    parsecode,
    listedcode,
    query,
    output
)
from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('',  views.homepage, name="home"),
    path('parsecode/', views.parsecode, name="parse"),
    path('listedcode/', views.listedcode, name="listedcode"),
    path('query/', views.query, name="query"),
    path('output/', views.output, name="output"),
    path('favicon.ico', RedirectView.as_view(url=static('favicon.ico')))
]
