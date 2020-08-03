from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('login', views.loginPage, name='app-login'),
    path('register', views.register, name='app-register'),
    path('profile',views.profile,name='app-profile'),
    path('results',views.results,name='app-results'),
]
