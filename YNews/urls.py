"""YNews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YNews.settings")
django.setup()

from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from search import views
urlpatterns = [
    #path('admin/', admin.site.urls),
    #url('admin/',views.admin),
    url(r'^$', views.homeroot),
    url(r'^(\d+)$',views.home),
    url(r'^search$',views.engine),
    url(r'^search/result$',views.result),
    url(r'^newspage/(\d+)$',views.page),
    url(r'^search/result/(\d+)$',views.result)
]

#python manage.py runserver