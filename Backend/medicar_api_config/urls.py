"""Medicar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token

from medicar_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('rest_auth.registration.urls')),
    url(r'^refresh-token/', refresh_jwt_token),
    url(r'^login/', obtain_jwt_token),

    path('delete_consulta/<int:consulta_id>/', views.delete_consulta, name='delete_consulta'),
    url(r'^create_consulta/$', views.add_consulta, name='post_consulta'),
    url(r'^retrieve_especialidades/$', views.retrieve_especialidades, name='get_especialidades'),
    url(r'^retrieve_medicos/$', views.retrieve_medicos, name='get_medicos'),
    url(r'^retrieve_consultas/$', views.retrieve_consultas, name='get_consultas'),
    url(r'^retrieve_agendas/$', views.retrieve_agendas, name='get_agendas')
]

