from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.db import models

diseases = ['Asthma', 'Melanoma', 'Photoaging', 'Basal Cell Carcinoma', 'Dysautonomia', 'Lung Cancer', 'Pneumonia',
            'Chronic Bronchitis', 'Cystic Fibrosis', 'Diabetes', 'Arthritis', 'Epilepsy', 'Migraines',
            'Seasonal Allergic Rhinitis', 'Pollen Allergy', 'Dust Allergy', 'Albinism', 'Photodermatitis',
            'Hyperhidrosis']
diseasesInput = list(map(lambda x: (x, x), diseases))

class registerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','password1','password2']
        # userName = forms.CharField(label='Username')
class loginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','password1']

class diseaseForm(forms.Form):
    # diseaseCheck = forms.MultipleChoiceField(
    #     required=True,
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=diseasesInput,
    # )
    Conditions = forms.MultipleChoiceField(
        required = False,
        choices=diseasesInput,
        widget=forms.SelectMultiple(attrs={'class': 'selectField'}),
    )
    Location = forms.CharField(label='Zip Code', required=False)
    # Conditions = forms.MultipleChoiceField(
    #     required = False,
    #     widget = forms.CheckboxSelectMultiple(attrs={'class': 'selectField'}),
    #     choices = diseasesInput,
    # )


