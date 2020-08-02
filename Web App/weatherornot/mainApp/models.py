from django.db import models
from multiselectfield import MultiSelectField

# Create your models here.
class diseaseModel(models.Model):
    diseases = ['Asthma', 'Melanoma', 'Photoaging', 'Basal Cell Carcinoma', 'Dysautonomia', 'Lung Cancer', 'Pneumonia',
                'Chronic Bronchitis', 'Cystic Fibrosis', 'Diabetes', 'Arthritis', 'Epilepsy', 'Migraines',
                'Seasonal Allergic Rhinitis', 'Pollen Allergy', 'Dust Allergy', 'Albinism', 'Photodermatitis',
                'Hyperhidrosis']
    diseasesInput = list(map(lambda x: (x, x), diseases))
    diseaseField = MultiSelectField(choices=diseasesInput)