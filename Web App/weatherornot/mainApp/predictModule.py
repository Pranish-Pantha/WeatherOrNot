import tensorflow as tf
from .baseAlgorithm import predictDisease, diseases
from .climateAPI import Climate
from dotenv import load_dotenv
import numpy
import os

class predictor:
    def __init__(self):
        load_dotenv('.env')
        usernameM = os.getenv('usernameM')
        passwordM = os.getenv('passwordM')
        token = os.getenv('token')
        openWeatherToken = os.getenv('openWeatherToken')
        weatherbitToken = os.getenv('weatherBitToken')

        self.model = tf.keras.models.load_model('predictiveModel.h5')
        self.climateLoader = Climate(usernameM, passwordM, token, openWeatherToken, weatherbitToken)

    def algorithmPredict(self, climateData, patientData):
        return predictDisease(climateData, patientData)

    def mlPredict(self, climateData, patientData, reload=False):
        if reload:
            self.model = tf.keras.models.load_model('predictiveModel.h5')
        climate = np.array([climateData])
        patient = np.array([patientData])
        return np.round(model.predict([climate, patient])[0], 2)

    def feedbackTrainModel(self, climateData, patientData, correctOutput, save=False):
        climate = np.array([climateData])
        patient = np.array([patientData])
        output = np.array([correctOutput])
        self.model.fit([climate, patient], output, batch_size=1, epochs=5)
        if save:
            self.model.save('predictiveModul.h5')

    def getClimateData(self, long, lat):
        return self.climateLoader.getAllMetrics(long, lat)

#print(predictor().getClimateData(-78.8496384,35.8612992))
