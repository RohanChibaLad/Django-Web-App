"""
URL configuration for myproject project.

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
from django.urls import path
from api.views import login_view, logout_view, post_story, get_stories, delete_story, register_agency, list_agencies

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login_view, name='login'),
    path('api/logout/', logout_view, name='logout'),
    path('api/stories/', post_story, name='post_story'),
    path('api/get_stories/', get_stories, name='get_stories'),
    path('api/stories/<int:key>/', delete_story, name='delete_story'),
    path('api/directory/register/', register_agency, name='register_agency'),
    path('api/directory/list/', list_agencies, name='list_agencies')
]