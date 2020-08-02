import tensorflow as tf
from baseAlgorithm import genClimateData, diseases

climate = genClimateData()
climate = np.array(list(map(lambda x: climate.get(x), climate.keys())))
patient = np.array(list(map(lambda x: 0, diseases)))

model = tf.keras.models.load_model('predictiveModel.h5')
model.predict([climate, patient])
