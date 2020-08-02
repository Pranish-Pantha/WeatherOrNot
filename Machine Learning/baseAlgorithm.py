import random
import csv

# generate random climate data
def genClimateData():
    AQI = random.randint(0, 500)
    Pollen = random.randint(0, 3)
    Dust = random.randint(0, 400)
    Temperature = random.randint(0, 40)
    Humidity = random.randint(0, 100)
    CloudCover = random.randint(0, 2)
    HeatIndex = random.randint(10, 55)
    SO2 = random.randint(0, 1)
    UVI = random.randint(0, 11)
    data = {"AQI": AQI, "Pollen": Pollen, "Dust": Dust, "Temperature": Temperature,
    "Humidity": Humidity, "CloudCover": CloudCover, "HeatIndex": HeatIndex, "SO2": SO2, "UVI": UVI}
    return data

# disease-climate data
numToWarning = {1: "Safe", 2:"Caution", 3:"Stay in"}
DiseaseToMetric = {
"Asthma": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Melanoma": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Photoaging": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Basal cell carcinoma": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"dysautonomia": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Lung Cancer": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Pneumonia": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"chronic bronchitis": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Cystic fibrosis": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Diabetes": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Arthritis": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Epilepsy": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Migraines": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"seasonal allergic rhinitis": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Pollen Allergy": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Dust Allergy": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"albinism": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Photodermatitis": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
"Hyperhidrosis": {"AQI": [50, 150], "Pollen": [10, 50], "Dust": [10, 50], "Temperature": [30, 35], "Humidity": [90, 100], "CloudCover": [1, 1], "HeatIndex": [25, 30], "SO2": [10, 50], "UVI": [6, 8]},
}

diseases = list(DiseaseToMetric.keys())

# predict threats for single disease
def predictDisease(climateData, disease):
    HeatRisk, BreatheRisk, SkinRisk, CancerRisk = 1, 1, 1, 1
    AQIData = climateData.get("AQI")
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
    return dict(zip(["CancerRisk", "HeatRisk", "SkinRisk", "BreatheRisk"], list(map(lambda x: numToWarning.get(round(x)), [CancerRisk, HeatRisk, SkinRisk, BreatheRisk]))))

diseasesInput = list(map(lambda x: (x,x), diseases))

def generateDataPoint():
    climateData = genClimateData()
    #return predictDisease(climateData, diseases[3])
    diseaseEncodings = list(map(lambda x: 0, diseases))
    numDiseases = random.randint(0,5)
    for i in range(numDiseases):
        q = random.randint(0, len(diseaseEncodings)-1)
        diseaseEncodings[q] = 1
        print(diseases[q])
    predictions = {
        'CancerRisk': "Safe",
        'HeatRisk': "Safe",
        'SkinRisk': "Safe",
        'BreatheRisk': "Safe"
    }
    for i in range(len(diseaseEncodings)):
        if diseaseEncodings[i] == 1:
            predictions.update(predictDisease(climateData, diseases[i]))
    return (climateData, diseaseEncodings, predictions)
print(diseases)
