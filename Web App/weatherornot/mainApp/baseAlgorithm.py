import random
import csv

# generate random climate data
def genClimateData():
    AQI = random.gauss(150, 40) #random.randint(0, 500)
    Pollen = random.gauss(1.5, .3) #random.randint(0, 3)
    Dust = random.gauss(200, 40) #random.randint(0, 400)
    Temperature = random.gauss(20, 4) #random.randint(0, 40)
    Humidity = random.gauss(40, 20) #random.randint(0, 100)
    CloudCover = random.gauss(2, .5) #random.randint(0, 2)
    HeatIndex = random.gauss(25, 5) #random.randint(10, 55)
    SO2 = random.gauss(.4, .1) #random.randint(0, 1)
    UVI = random.gauss(7, 2) #random.randint(0, 11)
    data = {"AQI": AQI, "Pollen": Pollen, "Dust": Dust, "Temperature": Temperature,
    "Humidity": Humidity, "CloudCover": CloudCover, "HeatIndex": HeatIndex, "SO2": SO2, "UVI": UVI}
    return data

# disease-climate data
numToWarning = {1: "Safe", 2:"Caution", 3:"Stay in"}
DiseaseToMetric = {
        "Asthma":	{"AQI":[51,100],	"Pollen":[1,1.5],	"Dust":[100,150],	"Temperature": [30,35], "Humidity":	[80,85], "CloudCover":	[2,3], "HeatIndex": [25,30],	"SO2": [1.5,2], 	"UVI": [3,4]},
        "Melanoma":	{"AQI":[100,150],	"Pollen":[2,2.5],	"Dust":[250,300],	"Temperature": [33,38], "Humidity":	[95,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [4,8], 	"UVI": [5,6]},
        "Photoaging":	{"AQI":[100,150],	"Pollen":[2,2.5],	"Dust":[250,300],	"Temperature": [33,38], "Humidity":	[95,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [4,8], 	"UVI": [5,6]},
        "Basal Cell Carcinoma":	{"AQI":[100,150],	"Pollen":[2,2.5],	"Dust":[250,300],	"Temperature": [33,38], "Humidity":	[95,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [4,8], 	"UVI": [5,6]},
        "Dysautonomia":	{"AQI":[51,100],	"Pollen":[1,1.5],	"Dust":[100,150],	"Temperature": [33,38], "Humidity":	[95,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [1.5,2], 	"UVI": [3,4]},
        "Lung Cancer":	{"AQI":[51,100],	"Pollen":[1,1.5],	"Dust":[100,150],	"Temperature": [33,38], "Humidity":	[80,85], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [1.5,2], 	"UVI": [3,4]},
        "Pneumonia":	{"AQI":[51,100],	"Pollen":[1,1.5],	"Dust":[100,150],	"Temperature": [33,38], "Humidity":	[80,85], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [1.5,2], 	"UVI": [3,4]},
        "Chronic Bronchitis":	{"AQI":[51,100],	"Pollen":[1,1.5],	"Dust":[100,150],	"Temperature": [33,38], "Humidity":	[75,80], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [1.5,2], 	"UVI": [3,4]},
        "Cystic Fibrosis":	{"AQI":[51,100],	"Pollen":[1,1.5],	"Dust":[100,150],	"Temperature": [30,35], "Humidity":	[70,75], "CloudCover":	[2,3], "HeatIndex": [25,30],	"SO2": [1.5,2], 	"UVI": [3,4]},
        "Diabetes":	{"AQI":[100,150],	"Pollen":[1,1.5],	"Dust":[100,150],	"Temperature": [33,38], "Humidity":	[95,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [4,8], 	"UVI": [3,4]},
        "Arthritis":	{"AQI":[100,150],	"Pollen":[2,2.5],	"Dust":[250,300],	"Temperature": [33,38], "Humidity":	[80,85], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [4,8], 	"UVI": [3,4]},
        "Epilepsy":	{"AQI":[100,150],	"Pollen":[2,2.5],	"Dust":[250,300],	"Temperature": [33,38], "Humidity":	[95,100], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [4,8], 	"UVI": [3,4]},
        "Migraines":	{"AQI":[100,150],	"Pollen":[2,2.5],	"Dust":[250,300],	"Temperature": [30,35], "Humidity":	[95,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [4,8], 	"UVI": [5,6]},
        "Seasonal Allergic Rhinitis":	{"AQI":[100,150],	"Pollen":[1,1.5],	"Dust":[100,150],	"Temperature": [95,100], "Humidity":	[80,85], "CloudCover":	[28,33], "HeatIndex": [25,30],	"SO2": [4,8], 	"UVI": [3,4]},
        "Pollen Allergy":	{"AQI":[51,100],	"Pollen":[1,1.5],	"Dust":[100,150],	"Temperature": [33,38], "Humidity":	[95,100], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [1.5,2], 	"UVI": [3,4]},
        "Dust Allergy":	{"AQI":[51,100],	"Pollen":[1,1.5],	"Dust":[100,150],	"Temperature": [33,38], "Humidity":	[80,85], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [1.5,2], 	"UVI": [3,4]},
        "Albinism":	{"AQI":[100,150],	"Pollen":[2,2.5],	"Dust":[250,300],	"Temperature": [30,35], "Humidity":	[95,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [4,8], 	"UVI": [3,4]},
        "Photodermatitis":	{"AQI":[100,150],	"Pollen":[2,2.5],	"Dust":[250,300],	"Temperature": [30,35], "Humidity":	[95,100], "CloudCover":	[1,2], "HeatIndex": [25,30],	"SO2": [4,8], 	"UVI": [5,6]},
        "Hyperhidrosis":	{"AQI":[100,150],	"Pollen":[2,2.5],	"Dust":[250,300],	"Temperature": [30,35], "Humidity":	[80,85], "CloudCover":	[1,2], "HeatIndex": [25,30],	"SO2": [4,8], 	"UVI": [5,6]}
}

diseases = list(DiseaseToMetric.keys())

# predict threats for single disease
def predictDisease(climateData, disease):
    HeatRisk, BreatheRisk, SkinRisk, CancerRisk = 1, 1, 1, 1
    AQIData = climateData.get("AQI")
    print(disease)
    AQIMetric = DiseaseToMetric.get(disease).get("AQI")
    if AQIData > AQIMetric[0]:
        if AQIData > AQIMetric[1]:
            BreatheRisk += 1.5
            CancerRisk += 1.5
        else:
            BreatheRisk += 0.5
            CancerRisk += 0.5
    PollenData = climateData.get("Pollen")
    PollenMetric = DiseaseToMetric.get(disease).get("Pollen")
    if PollenData > PollenMetric[0]:
        if PollenData > PollenMetric[1]:
            BreatheRisk += 1.5
        else:
            BreatheRisk += 0.5
    DustData = climateData.get("Dust")
    DustMetric = DiseaseToMetric.get(disease).get("Dust")
    if DustData > DustMetric[0]:
        if DustData > DustMetric[1]:
            BreatheRisk += 1.5
        else:
            BreatheRisk += 0.5
    TempData = climateData.get("Temperature")
    TempMetric = DiseaseToMetric.get(disease).get("Temperature")
    if TempData > TempMetric[0]:
        if TempData > TempMetric[1]:
            HeatRisk += 1.5
            SkinRisk += 1.5
        else:
            HeatRisk += 0.5
            SkinRisk += 0.5
    HeatIData = climateData.get("HeatIndex")
    HeatIMetric = DiseaseToMetric.get(disease).get("HeatIndex")
    if HeatIData > HeatIMetric[0]:
        if HeatIData > HeatIMetric[1]:
            HeatRisk += 1.5
        else:
            HeatRisk += 0.5
    CloudCData = climateData.get("CloudCover")
    CloudCMetric = DiseaseToMetric.get(disease).get("CloudCover")
    if CloudCData <= CloudCMetric[0]:
        if CloudCData <= CloudCMetric[1]:
            HeatRisk += 1.5
            CancerRisk += 1.5
        else:
            HeatRisk += 0.5
            CancerRisk += 0.5
    HumidityData = climateData.get("Humidity")
    HumidityMetric = DiseaseToMetric.get(disease).get("Humidity")
    if HumidityData > HumidityMetric[0]:
        if HumidityData > HumidityMetric[1]:
            HeatRisk += 1.5
            SkinRisk += 1.5
        else:
            HeatRisk += 0.5
            SkinRisk += 0.5
    SO2Data = climateData.get("SO2")
    SO2Metric = DiseaseToMetric.get(disease).get("SO2")
    if SO2Data > SO2Metric[0]:
        if SO2Data > SO2Metric[1]:
            SkinRisk += 1.5
        else:
            SkinRisk += 0.5
    UVData = climateData.get("UVI")
    UVMetric = DiseaseToMetric.get(disease).get("UVI")
    if UVData > UVMetric[0]:
        if UVData > UVMetric[1]:
            CancerRisk += 1.5
        else:
            CancerRisk += 1.5
    if CancerRisk > 3:
        CancerRisk = 3
    if HeatRisk > 3:
        HeatRisk = 3
    if SkinRisk > 3:
        SkinRisk = 3
    if BreatheRisk > 3:
        BreatheRisk = 3

    normalizeLabels = {1:0, 2:.5, 3:1}
    return list(map(lambda x: normalizeLabels.get(round(x)), [CancerRisk, HeatRisk, SkinRisk, BreatheRisk]))

diseasesInput = list(map(lambda x: (x,x), diseases))

def generateDataPoint():
    climateData = genClimateData()
    #return predictDisease(climateData, diseases[3])
    diseaseEncodings = list(map(lambda x: 0, diseases))
    numDiseases = random.randint(0,15)
    for i in range(numDiseases):
        q = random.randint(0, len(diseaseEncodings)-1)
        diseaseEncodings[q] = 1
        #print(diseases[q])
    predictions = [0,0,0,0]
    for i in range(len(diseaseEncodings)):
        if diseaseEncodings[i] == 1:
            diseasePreds = predictDisease(climateData, diseases[i])
            for j in range(len(diseasePreds)):
                f = lambda x: 1 if x>1 else x
                predictions[j] = f(predictions[j] + diseasePreds[j])
    return (climateData, diseaseEncodings, predictions)

print(generateDataPoint())
