"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls', namespace='myapp')),
    path('BuildPc', include('myapp.urls', namespace='myapp')),
    path('PreMade', include('myapp.urls', namespace='myapp')),
    path('ContactUs', include('myapp.urls', namespace='myapp')),
    path('ShoppingCart', include('myapp.urls', namespace='myapp')),

    path('AdminPanel/', include('myapp.urls', namespace='myapp')),
    path('AdminPanel/History', include('myapp.urls', namespace='myapp')),
    path('AdminPanel/Stock_Data', include('myapp.urls', namespace='myapp')),
    path('AdminPanel/User_Data', include('myapp.urls', namespace='myapp')),

    path('Check', include('myapp.urls', namespace='myapp')),
    path('login', include('myapp.urls', namespace='myapp')),
    path('ShopDetail', include('myapp.urls', namespace='myapp')),
    path('signup', include('myapp.urls', namespace='myapp')),
    path('UserAccount', include('myapp.urls', namespace='myapp')),
    path('', include('myapp.urls'))
]
