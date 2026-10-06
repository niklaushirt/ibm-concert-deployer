from django.urls import path

from . import views

urlpatterns = [
    path('health', views.health, name='health'),
    path('loginui', views.loginui, name='loginui'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('doc', views.doc, name='doc'),
    path('config', views.config, name='config'),
    path('apps', views.apps, name='apps'),
    path('apps_system', views.apps_system, name='apps_system'),
    path('apps_demo', views.apps_demo, name='apps_demo'),
    path('apps_additional', views.apps_additional, name='apps_additional'),
    path('about', views.about, name='about'),
    path('watsonx', views.watsonx, name='watsonx'),
    path('', views.index, name='index'),
]
