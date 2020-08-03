import random
import csv

# generate random climate data
def genClimateData():
    AQI = random.gauss(10, 3) #random.randint(0, 500)
    Pollen = random.gauss(1.5, .3) #random.randint(0, 3)
    Dust = random.gauss(.1, .03) #random.randint(0, 400)
    Temperature = random.gauss(20, 4) #random.randint(0, 40)
    Humidity = random.gauss(40, 20) #random.randint(0, 100)
    CloudCover = random.gauss(2, .5) #random.randint(0, 2)
    HeatIndex = random.gauss(25, 5) #random.randint(10, 55)
    SO2 = random.gauss(.1, .03) #random.randint(0, 1)
    UVI = random.gauss(7, 2) #random.randint(0, 11)
    data = {"AQI": AQI, "Pollen": Pollen, "Dust": Dust, "Temperature": Temperature,
    "Humidity": Humidity, "CloudCover": CloudCover, "HeatIndex": HeatIndex, "SO2": SO2, "UVI": UVI}
    return data

# disease-climate data
numToWarning = {1: "Safe", 2:"Caution", 3:"Stay in"}
DiseaseToMetric = {
        "Asthma":	{"AQI":[4,12],	"Pollen":[1,1.5],	"Dust":[0.01,0.1],	"Temperature": [25,30], "Humidity":	[8,85], "CloudCover":	[2,3], "HeatIndex": [25,30],	"SO2": [0.05,0.1], 	"UVI": [3,4]},
        "Melanoma":	{"AQI":[4,15],	"Pollen":[2,2.5],	"Dust":[0.01,0.1],	"Temperature": [27,33], "Humidity":	[9,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [0.1,0.15], 	"UVI": [5,6]},
        "Photoaging":	{"AQI":[4,15],	"Pollen":[2,2.5],	"Dust":[0.01,0.1],	"Temperature": [27,33], "Humidity":	[9,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [0.1,0.15], 	"UVI": [5,6]},
        "Basal Cell Carcinoma":	{"AQI":[4,15],	"Pollen":[2,2.5],	"Dust":[0.01,0.1],	"Temperature": [27,33], "Humidity":	[9,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [0.1,0.15], 	"UVI": [5,6]},
        "Dysautonomia":	{"AQI":[4,12],	"Pollen":[1,1.5],	"Dust":[0.01,0.1],	"Temperature": [27,33], "Humidity":	[9,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [0.05,0.1], 	"UVI": [3,4]},
        "Lung Cancer":	{"AQI":[4,12],	"Pollen":[1,1.5],	"Dust":[0.01,0.1],	"Temperature": [27,33], "Humidity":	[8,85], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [0.05,0.1], 	"UVI": [3,4]},
        "Pneumonia":	{"AQI":[4,12],	"Pollen":[1,1.5],	"Dust":[0.01,0.1],	"Temperature": [27,33], "Humidity":	[8,85], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [0.05,0.1], 	"UVI": [3,4]},
        "Chronic Bronchitis":	{"AQI":[4,12],	"Pollen":[1,1.5],	"Dust":[0.01,0.1],	"Temperature": [27,33], "Humidity":	[7,80], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [0.05,0.1], 	"UVI": [3,4]},
        "Cystic Fibrosis":	{"AQI":[4,12],	"Pollen":[1,1.5],	"Dust":[0.01,0.1],	"Temperature": [28,33], "Humidity":	[7,75], "CloudCover":	[2,3], "HeatIndex": [25,30],	"SO2": [0.05,0.1], 	"UVI": [3,4]},
        "Diabetes":	{"AQI":[4,15],	"Pollen":[1,1.5],	"Dust":[0.01,0.1],	"Temperature": [27,33], "Humidity":	[9,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [0.1,0.15], 	"UVI": [3,4]},
        "Arthritis":	{"AQI":[4,15],	"Pollen":[2,2.5],	"Dust":[0.01,0.1],	"Temperature": [27,33], "Humidity":	[8,85], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [0.1,0.15], 	"UVI": [3,4]},
        "Epilepsy":	{"AQI":[4,15],	"Pollen":[2,2.5],	"Dust":[0.05,0.15],	"Temperature": [27,33], "Humidity":	[9,100], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [0.1,0.15], 	"UVI": [3,4]},
        "Migraines":	{"AQI":[4,15],	"Pollen":[2,2.5],	"Dust":[0.05,0.15],	"Temperature": [28,33], "Humidity":	[9,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [0.1,0.15], 	"UVI": [5,6]},
        "Seasonal Allergic Rhinitis":	{"AQI":[4,150],	"Pollen":[1,1.5],	"Dust":[0.01,0.1],	"Temperature": [28,33], "Humidity":	[8,85], "CloudCover":	[28,33], "HeatIndex": [25,30],	"SO2": [0.1,0.15], 	"UVI": [3,4]},
        "Pollen Allergy":	{"AQI":[7,12],	"Pollen":[1,1.5],	"Dust":[0.01,0.1],	"Temperature": [27,33], "Humidity":	[9,100], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [0.05,0.1], 	"UVI": [3,4]},
        "Dust Allergy":	{"AQI":[7,12],	"Pollen":[1,1.5],	"Dust":[0.01,0.1],	"Temperature": [27,33], "Humidity":	[8,85], "CloudCover":	[2,3], "HeatIndex": [28,33],	"SO2": [0.05,0.1], 	"UVI": [3,4]},
        "Albinism":	{"AQI":[4,15],	"Pollen":[2,2.5],	"Dust":[0.05,0.15],	"Temperature": [28,33], "Humidity":	[9,100], "CloudCover":	[1,2], "HeatIndex": [28,33],	"SO2": [0.1,0.15], 	"UVI": [3,4]},
        "Photodermatitis":	{"AQI":[4,15],	"Pollen":[2,2.5],	"Dust":[0.05,0.15],	"Temperature": [28,33], "Humidity":	[9,100], "CloudCover":	[1,2], "HeatIndex": [25,30],	"SO2": [0.1,0.15], 	"UVI": [5,6]},
        "Hyperhidrosis":	{"AQI":[4,15],	"Pollen":[2,2.5],	"Dust":[0.05,0.15],	"Temperature": [28,33], "Humidity":	[8,85], "CloudCover":	[1,2], "HeatIndex": [25,30],	"SO2": [0.1,0.15], 	"UVI": [5,6]}
}

diseases = list(DiseaseToMetric.keys())
# predict threats for single disease
def predictDisease(climateData, disease):
    #print(climateData)
    HeatRisk, BreatheRisk, SkinRisk, CancerRisk = 1, 2, 1, 1

    for diseas in disease:
        if diseas in DiseaseToMetric.keys():
            AQIData = int(climateData.get("AQI"))
            AQIMetric = DiseaseToMetric.get(diseas).get("AQI")
            if AQIData > AQIMetric[0]:
                if AQIData > AQIMetric[1]:
                    BreatheRisk += 1.5
                    CancerRisk += 1.5
                else:
                    BreatheRisk += 1
                    CancerRisk += 1
            PollenData = int(climateData.get("Pollen"))
            PollenMetric = DiseaseToMetric.get(diseas).get("Pollen")
            if PollenData > PollenMetric[0]:
                if PollenData > PollenMetric[1]:
                    BreatheRisk += 1.5
                else:
                    BreatheRisk += 1
            DustData = int(climateData.get("Dust"))
            DustMetric = DiseaseToMetric.get(diseas).get("Dust")
            if DustData > DustMetric[0]:
                if DustData > DustMetric[1]:
                    BreatheRisk += 1.5
                else:
                    BreatheRisk += 1
            TempData = int(climateData.get("Temperature"))
            TempMetric = DiseaseToMetric.get(diseas).get("Temperature")
            if TempData > TempMetric[0]:
                if TempData > TempMetric[1]:
                    HeatRisk += 1.5
                    SkinRisk += 1.5
                else:
                    HeatRisk += 1
                    SkinRisk += 1
            HeatIData = int(climateData.get("HeatIndex"))
            HeatIMetric = DiseaseToMetric.get(diseas).get("HeatIndex")
            if HeatIData > HeatIMetric[0]:
                if HeatIData > HeatIMetric[1]:
                    HeatRisk += 1.5
                else:
                    HeatRisk += 1
            CloudCData = int(climateData.get("CloudCover"))
            CloudCMetric = DiseaseToMetric.get(diseas).get("CloudCover")
            if CloudCData <= CloudCMetric[0]:
                if CloudCData <= CloudCMetric[1]:
                    HeatRisk += 1.5
                    CancerRisk += 1.5
                else:
                    HeatRisk += 1
                    CancerRisk += 1
            HumidityData = int(climateData.get("Humidity"))
            HumidityMetric = DiseaseToMetric.get(diseas).get("Humidity")
            if HumidityData > HumidityMetric[0]:
                if HumidityData > HumidityMetric[1]:
                    HeatRisk += 1.5
                    SkinRisk += 1.5
                else:
                    HeatRisk += 1
                    SkinRisk += 1
            SO2Data = int(climateData.get("SO2"))
            SO2Metric = DiseaseToMetric.get(diseas).get("SO2")
            if SO2Data > SO2Metric[0]:
                if SO2Data > SO2Metric[1]:
                    SkinRisk += 1.5
                else:
                    SkinRisk += 1
            UVData = int(climateData.get("UVI"))
            UVMetric = DiseaseToMetric.get(diseas).get("UVI")
            if UVData > UVMetric[0]:
                if UVData > UVMetric[1]:
                    CancerRisk += 1.5
                else:
                    CancerRisk += 1
    if CancerRisk > 3:
        CancerRisk = 3
    if HeatRisk > 3:
        HeatRisk = 3
    if SkinRisk > 3:
        SkinRisk = 3
    if BreatheRisk > 3:
        BreatheRisk = 3

    normalizeLabels = {1:0, 2:.5, 3:1}
    print("THE ALGORITHM BEFORE Normalizing", CancerRisk, HeatRisk, SkinRisk, BreatheRisk)
    labels = list(map(lambda x: normalizeLabels.get(round(x)), [CancerRisk, HeatRisk, SkinRisk, BreatheRisk]))
    print("THE ALGORITHM PREDICTS", labels)
    return labels

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

#print(generateDataPoint())
