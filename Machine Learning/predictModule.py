import tensorflow as tf
from baseAlgorithm import predictDisease, diseases

class predictor:
    def __init__(self):
        self.model = tf.keras.models.load_model('predictiveModel.h5')

    def algorithmPredict(self, climateData, patientData):
        return predictDisease(climateData, patientData)

    def mlPredict(self, climateData, patientData):
        climate = np.array([climateData])
        patient = np.array([patientData])
        return np.round(model.predict([climate, patient])[0], 2)

    def feedbackTrainModel(self, climateData, patientData, correctOutput, save=False):
        climate = np.array([climateData])
        patient = np.array([patientData])
        output = np.array([correctOutput])
        self.model.fit([climate, patient], output, batch_size=1, epochs=5)
        if save:
            self.model.save('predictModule.h5')
