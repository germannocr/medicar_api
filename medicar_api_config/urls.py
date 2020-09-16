"""todo_list URL Configuration

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

from todo_list_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('rest_auth.registration.urls')),
    url(r'^refresh-token/', refresh_jwt_token),
    url(r'^login/', obtain_jwt_token),

    path('update_card/<int:card_id>/', views.update_card, name='update_card'),
    path('delete_card/<int:card_id>/', views.delete_card, name='delete_card'),
    url(r'^create_card/$', views.add_card, name='create_card'),
    url(r'^todo_cards/$', views.retrieve_todo_cards, name='todo_cards'),
    url(r'^doing_cards/$', views.retrieve_doing_cards, name='doing_cards'),
    url(r'^done_cards/$', views.retrieve_done_cards, name='done_cards'),

]

