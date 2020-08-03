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
import time
# Create your views here.
#from .models import *
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
            login(request, user)
            return redirect('app-profile')
        print(form.errors)
    context = {
        'form': form,
        'pageName' : 'Register'
    }
    return render(request,"mainApp/register.html",context)


def home(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return redirect("app-results")
        else:
            return redirect("app-register")
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
        return redirect('app-results')
    context = {
        'zip' : getZip(request),
        'form' : form,
        'pageName' : 'profile'
    }
    return render(request,'mainApp/profile.html',context)
def results(request):
    context = {}
    algopreds = [0,0,0,0]
    mlpreds = [0,0,0,0]
    form = locationForm()
    form2 = feedbackForm()
    if request.user.is_authenticated:
        email = request.user.username
        name = email[0:email.index('@')]

        # query database for patient data
        database = dbAccess('patientData.db')
        currentPatientData = list(database.readColumn(request.user.username)[3:])
        database.closeConnection()

        dictionaryToAlgorithm =predict.getClimateData(getLong(getZip(results)),getLat(getZip(results)))
        toList = list(map(lambda x: dictionaryToAlgorithm.get(x), dictionaryToAlgorithm.keys()))
        print(toList)
        #print("This the prediction from the algorithm: ")
        # print(predict.algorithmPredict(dictionaryToAlgorithm, currentPatientData))
        # print(predict.mlPredict(toList,currentPatientData))
        if request.method == "POST":
            context = {}
            form = locationForm(request.POST)
            if form.is_valid():
                if True:
                    # query database for user data
                    database = dbAccess('patientData.db')
                    userZipCode = database.readColumn(request.user.username)[1]
                    database.closeConnection()
                    dictionaryToAlgorithm = predict.getClimateData(getLong(userZipCode),getLat(userZipCode))
                    toList = list(map(lambda x: dictionaryToAlgorithm.get(x), dictionaryToAlgorithm.keys()))
                    algopreds = predict.algorithmPredict(dictionaryToAlgorithm, currentPatientData)
                    mlpreds = predict.mlPredict(toList,currentPatientData)
                    print(algopreds, mlpreds)
        if request.method == 'POST' and 'risks' in request.POST:
            form2 = feedbackForm(request.POST)
            if form2.is_valid():
                print(form2.cleaned_data['risks'])
                context.update({'feedback': True})
    else:
        return redirect('app-register')

    colorMap = lambda x: "red" if x>.6 else ('yellow' if x>.3 else "green")
    newContext = {
        'zip': getZip(request),
        'pageName' : 'results',
        'username': name,
        'form' : form,
        'form2' : form2,
        'AQI': toList[0],
        'Pollen': toList[1],
        'Dust': toList[2],
        'Temperature': toList[3],
        'Humidity': toList[4],
        'CloudCover': toList[5],
        'HeatIndex': toList[6],
        'SO2': toList[7],
        'UVI': toList[8],
        'accolor': colorMap(algopreds[0]),
        'ahcolor': colorMap(algopreds[1]),
        'ascolor': colorMap(algopreds[2]),
        'abcolor': colorMap(algopreds[3]),
        'mccolor': colorMap(mlpreds[0]),
        'mhcolor': colorMap(mlpreds[1]),
        'mscolor': colorMap(mlpreds[2]),
        'mbcolor': colorMap(mlpreds[3]),
        'acval': round(algopreds[0]*100, 2),
        'ahval': round(algopreds[1]*100, 2),
        'asval': round(algopreds[2]*100, 2),
        'abval': round(algopreds[3]*100, 2),
        'mcval': round(mlpreds[0]*100, 2),
        'mhval': round(mlpreds[1]*100, 2),
        'msval': round(mlpreds[2]*100, 2),
        'mbval': round(mlpreds[3]*100, 2),
    }
    context.update(newContext)
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
