"""
URL configuration for fortest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from helloapp import views 







urlpatterns = [
    path('', views.random_text_view, name='random_text'),
    path('update_likes/<int:text_id>/', views.update_likes, name='update_likes'),
    path('create_text/', views.create_text, name='create_text'),
    path('admin/', admin.site.urls),
    path('look_texts/', views.look_texts, name='look_texts'),
    path('search_texts/', views.search_texts, name='search_texts'),
    #path('', include('hello.urls')), 
    
]


