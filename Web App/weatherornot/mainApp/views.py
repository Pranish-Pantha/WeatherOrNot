from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
import requests,json

# Create your views here.
from .models import *
from .forms import registerForm, loginForm, diseaseForm, locForm
# from .models import diseaseModel

def loginPage(request):
    form = loginForm()
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('app-home')
        else:
            context.update({
                "error_message" : "Incorrect username or password."
            })
    context.update({
        'form':form,
        'pageName' : 'Login'
    })

    return render(request,"mainApp/login.html",context)


def register(request):
    form = registerForm()
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            username = request.POST.get('email')
            user= User.objects.create_user(username,request.POST.get('email'),request.POST.get('password1'))
            user.save()
            return redirect('app-home')
        print(form.errors)
    context = {
        'form': form,
        'pageName' : 'Register'
    }
    return render(request,"mainApp/register.html",context)


def home(request):
    form = diseaseForm()
    form2 = locForm()
    if request.method == 'POST':
        form = diseaseForm(request.POST)
        if form.is_valid():
            form.save()
    if request.method == 'POST':
        form2 = locForm(request.POST)
        if form2.is_valid():
            form2.save()
    context = {
        'zip' : getZip(request),
        'form' : form,
        'form2' : form2,
        'pageName' : 'Home'
    }
    return render(request,'mainApp/home.html',context)
def output(request):
    context = {
        'pageName': 'Output',
    }
    return render(request,'mainApp/output.html',context)
def getZip(request):
    rootAPI = 'http://ip-api.com/json/'
    req = requests.get(rootAPI)
    res = json.loads(req.text)
    zip = res['zip']
    return zip

