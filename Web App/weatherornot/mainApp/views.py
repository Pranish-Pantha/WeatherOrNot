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
from db import dbAccess
# Create your views here.
from .models import *
from .forms import registerForm, loginForm, diseaseForm, locationForm, feedbackForm
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

            # add user to database
            database = dbAccess('patientData.db')
            database.make_db()
            database.addEntry([username, getZip(request), username[0:username.index('@')]] + list(map(lambda x: "0", range(19))))
            database.printTable()
            database.closeConnection()

            user.save()
            return redirect('app-profile')
        print(form.errors)
    context = {
        'form': form,
        'pageName' : 'Register'
    }
    return render(request,"mainApp/register.html",context)


def home(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            redirect("app-results")

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

            # query database for user data
            database = dbAccess('patientData.db')
            currentUserData = list(database.readColumn(request.user.username)[:3])
            # merge userdata with new patient data and update database
            database.updateEntry(request.user.username, currentUserData + patientData)
            database.printTable()
            database.closeConnection()

                #heat risk,
        redirect('app-results')
    context = {
        'zip' : getZip(request),
        'form' : form,
        'pageName' : 'profile'
    }
    return render(request,'mainApp/profile.html',context)
def results(request):
    form = locationForm()
    form2 = feedbackForm()
    if request.method == 'POST':
        form = feedbackForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    if request.user.is_authenticated:
        email = request.user.username
        name = email[0:email.index('@')]

        # query database for patient data
        database = dbAccess('patientData.db')
        currentPatientData = list(database.readColumn(request.user.username)[3:])
        database.closeConnection()

        dictionaryToAlgorithm, listToModel =predict.getClimateData(getLong(getZip(results)),getLat(getZip(results)))
        toList = list(map(lambda x: dictionaryToAlgorithm.get(x), dictionaryToAlgorithm.keys()))
        #print("This the prediction from the algorithm: ")
        # print(predict.algorithmPredict(dictionaryToAlgorithm, currentPatientData))
        # print(predict.mlPredict(toList,currentPatientData))
        if request.method == "POST":
            form = locationForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['Location'] != "":
                    dictionaryToAlgorithm, listToModel =predict.getClimateData(getLong(form['Location']),getLat(form['Location']))
                    toList = list(map(lambda x: dictionaryToAlgorithm.get(x), dictionaryToAlgorithm.keys()))
                    print("This the prediction from the algorithm: ")
                    # print(predict.algorithmPredict(dictionaryToAlgorithm, currentPatientData))
                    # print(predict.mlPredict(toList,currentPatientData))
    else:
        redirect('app-register')

    context = {
        'zip': getZip(request),
        'pageName' : 'results',
        'username': name,
        'form' : form,
        'form2' : form2,
    }

    return render(request,'mainApp/results.html',context)
def getZip(request):
    rootAPI = 'http://ip-api.com/json/'
    req = requests.get(rootAPI)
    res = json.loads(req.text)
    zip = res['zip']
    return zip


def getLat(zip):
    gcode = pgeocode.Nominatim('US')
    lat = gcode.query_postal_code(zip)['latitude']
    return lat

def getLong(zip):
    gcode = pgeocode.Nominatim('US')
    long = gcode.query_postal_code(zip)['longitude']
    return long
