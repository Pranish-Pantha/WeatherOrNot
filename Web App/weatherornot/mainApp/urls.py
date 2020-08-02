from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('login', views.loginPage, name='app-login'),
    path('register', views.register, name='app-register'),
    path('output',views.output,name='app-output'),
    path('conditions',views.conditions,name='app-conditions'),
]
