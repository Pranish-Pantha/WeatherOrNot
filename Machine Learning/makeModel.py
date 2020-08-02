import tensorflow as tf
from baseAlgorithm import generateDataPoint, diseases
import numpy as np

climateFeatures = []
patientFeatures = []
features = []
labels = []

testCases = 1000
for i in range(testCases):
    data = generateDataPoint()
    #print(data)
    climateFeatures.append(list(map(lambda x: data[0].get(x), data[0].keys())))
    patientFeatures.append(data[1])
    features.append(list(map(lambda x: data[0].get(x), data[0].keys())) + data[1])
    labels.append(data[2])

climateFeatures = np.array(climateFeatures)
patientFeatures = np.array(patientFeatures)
features = np.array(features)
labels = np.array(labels)

print(labels)
# climate parameters
# 1: Normalized AQI
# 2: Pollen Concentration (0-1) -- Divide by 3 to normalize
# 3: Dust Concentration (AOD 0-1)
# 4: Temperature (Deg C)
# 5: Humidity (Relative 0-1) -- Divide by 100
# 6: Air Pressure (Pascals / 101325) -> ATM
# 7: Cloud Cover (low = 0, medium = .5, high=1)
# 8: Heat-Index (Deg C)
# 9: Sulfur Dioxide Concentration (AOD 0-1)
numDiseases = len(diseases)

# input and process climate data
climateInput = tf.keras.layers.Input(shape=[9])
climate_dense1 = tf.keras.layers.Dense(128, activation='relu')(climateInput)
#climate_dense2 = tf.keras.layers.Dense(128, activation='relu')(climate_dense1)
#climate_dense3 = tf.keras.layers.Dense(128, activation='relu')(climate_dense2)

# patient parameters
# binary(0/1) state for each disease
# one-hot encoded data

# input and process patient data
patientInfoInput = tf.keras.layers.Input(shape=[numDiseases])
patient_dense1 = tf.keras.layers.Dense(128, activation='relu')(patientInfoInput)
#patient_dense2 = tf.keras.layers.Dense(128, activation='relu')(patient_dense1)
#patient_dense3 = tf.keras.layers.Dense(128, activation='relu')(patient_dense2)

# concatenate patient and climate output layers and output predictions
concat_layer = tf.keras.layers.Concatenate()([climate_dense1, patient_dense1])
concat_dense1 = tf.keras.layers.Dense(64, activation='relu')(concat_layer)
#concat_dense2 = tf.keras.layers.Dense(64, activation='relu')(concat_dense1)
#concat_dropout = tf.keras.layers.Dropout(.2)(concat_dense2)
concat_dropout = tf.keras.layers.Dropout(.5)(concat_dense1)
output = tf.keras.layers.Dense(4, activation='sigmoid', dtype='float32')(concat_dropout)

model = tf.keras.Model(inputs=[climateInput, patientInfoInput], outputs=[output])

'''
model = tf.keras.models.Sequential([tf.keras.layers.Dense(128, activation='relu', input_shape=[numDiseases+9]),
                                   tf.keras.layers.Dense(128, activation='relu'),
                                   tf.keras.layers.Dense(128, activation='relu'),
                                   tf.keras.layers.Dense(4, activation='sigmoid')])
'''
model.compile(optimizer=tf.keras.optimizers.RMSprop(), loss='categorical_crossentropy')


model.summary()
#model.fit(features, labels, batch_size=1, epochs=10, verbose=1)
model.fit([climateFeatures, patientFeatures], labels, batch_size=100, epochs=4000, verbose=1)
preds = model.predict([climateFeatures, patientFeatures])
print(np.round(preds, 2))
model.save('predictiveModel.h5')
