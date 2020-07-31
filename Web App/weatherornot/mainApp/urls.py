from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('login', views.login, name='app-login'),
    path('register', views.register, name='app-register')
]
