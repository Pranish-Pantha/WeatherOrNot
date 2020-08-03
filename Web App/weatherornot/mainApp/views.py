from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from .baseAlgorithm import diseases
import requests,json,sys
from .predictModule import predictor
import pgeocode

# Create your views here.
from .models import *
from .forms import registerForm, loginForm, diseaseForm
# from .models import diseaseModel

predict = predictor()
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
    context = {
        'pageName' : 'Home'
    }
    return render(request,'mainApp/home.html',context)


def profile(request):
    form = diseaseForm()
    if request.method == 'POST':
        form = diseaseForm(request.POST)
        if form.is_valid():
            patientData = list(map(lambda x: 0, diseases))
            conds = dict(form.cleaned_data)["Conditions"]
            for i in range(len(conds)):
                for j in range(len(diseases)):
                    if conds[i] == diseases[j]:
                        patientData[j] = 1
            if form.cleaned_data['Location'] != "":
                print("This the prediction from the algorithm: ")
                print(predict.algorithmPredict(predict.getClimateData(getLong(form.cleaned_data),getLat(form.cleaned_data)),patientData))
                print(predict.mlPredict(predict.getClimateData(getLong(form.cleaned_data),getLat(form.cleaned_data)),patientData))
                #heat risk,
    context = {
        'zip' : getZip(request),
        'form' : form,
        'pageName' : 'profile'
    }
    return render(request,'mainApp/profile.html',context)
def output(request):
    context = {}
    if User.is_authenticated:
        context.update({
            'pageName': 'Output',

        })
    return render(request,'mainApp/output.html',context)
def getZip(request):
    rootAPI = 'http://ip-api.com/json/'
    req = requests.get(rootAPI)
    res = json.loads(req.text)
    zip = res['zip']
    return zip


def getLat(zip):
    gcode = pgeocode.Nominatim('US')
    lat = gcode.query_postal_code(zip['Location'])['latitude']
    return lat

def getLong(zip):
    gcode = pgeocode.Nominatim('US')
    long = gcode.query_postal_code(zip['Location'])['longitude']
    return long
