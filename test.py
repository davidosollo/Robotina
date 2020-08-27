
import numpy as np
import pandas as pd
from tensorflow import keras

#GetSect
def getSec(npPercentage):

    TaskSec = np.array([])
    pdNoSort = np.reshape(npPercentage, 4)
    pdSort  = np.copy(-np.sort(-npPercentage))
    pdSort = np.reshape(pdSort , 4)

    for task in pdSort:
        i = 0
        for Percent in pdNoSort:
            if task == Percent:
                TaskSec = np.append(TaskSec,i)
                break
            i = i + 1
    return TaskSec


#Construccion del Modelo
def build_model(xSize):


  model = keras.Sequential()
  model.add(keras.layers.Dense(32, kernel_initializer='glorot_uniform',
                               activation='relu', input_shape=xSize))
  model.add(keras.layers.Dropout(0.2))
  model.add(keras.layers.Dense(120, activation='tanh'))
  model.add(keras.layers.Dense(4, activation='softmax'))

  model.compile(loss='mean_squared_error',
                optimizer=keras.optimizers.Adam())

  return  model


dfRobo = pd.read_excel('./DataSets/RoboCogni.xlsx')


X = dfRobo[dfRobo.columns[0:4]].to_numpy()
Y = dfRobo[dfRobo.columns[4:]].to_numpy()

X = X / X.max(axis=0)

print(X.shape)
print(Y.shape)

#Construir el Modelo
model = build_model([X.shape[1]])

X = np.asarray(X).astype(np.float32)
Y = np.asarray(Y).astype(np.float32)

#Entrenar el Modelo
history = model.fit(X, Y,
                    batch_size=150, epochs=100,
                    validation_split=0.2, verbose=1)

model.summary()



# Cada vez que se inicialize ====================
xTest = np.array([[1.0, 1.0, 1.0, 1.0]])




results = model.predict(xTest)

RoboSecs = getSec(results)



print("End")