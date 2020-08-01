from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.
from .models import *
from .forms import registerForm, loginForm

def loginPage(request):
    form = loginForm()
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')

    context = {
        'form':form,
        'pageName' : 'Login'
    }
    return render(request,"mainApp/login.html",context)


def register(request):
    form = registerForm()
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        print(form.errors)
    context = {
        'form': form,
        'pageName' : 'Register'
    }
    return render(request,"mainApp/register.html",context)


def home(request):
    context = {
        'pageName' : 'Home'
    }
    return render(request,'mainApp/base.html',context)
