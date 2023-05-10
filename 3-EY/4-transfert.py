import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, Input, Flatten, Reshape, ConvLSTM2D, MaxPooling2D,BatchNormalization
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.utils import pad_sequences
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
import sklearn
# fix random seed for reproducibility
tf.random.set_seed(7)
# pip3 install tensorflow numpy pandas scikit-learn





dateparse = lambda x: datetime.strptime(x, '%d-%m-%Y')
df2 = pd.read_csv("Crop_Yield_Data_challenge_2.csv", parse_dates=['Date of Harvest'], date_parser=dateparse)
df2

borne = [
    (-0.0440750, 1.1379025),
    (-0.0215250, 1.1155175),
    (-0.1473925, 1.13914),
    (0.04604250, 1.2140225),
    (21762.0000, 56916.0),
    (293.0, 48423.0)
]
mini = np.array([
    -0.0440750,
    -0.0215250,
    -0.1473925,
    0.04604250,
    21762.0000,
    293.0,
])
multi = np.array([
    1.1819775, 
    1.1370425, 
    1.2865325, 
    1.16798, 
    35154.0, 
    48130.0
])


x2 = []
y2 = []
for i in range(len(df2)):
    with open(f"inputs_lstm/{i}.npy", "rb") as f:
        arr = np.load(f)
        arr = np.transpose(arr, (0, 2, 3, 1))
        arr = (arr-mini)/multi
        x2.append(arr)
    y2.append([(df2.loc[i, "Rice Yield (kg/ha)"]-5200)/(8000-52000)])
    

x2 = pad_sequences(x2, dtype="float", maxlen=32)
y2 = np.array(y2)


x2, y2 = shuffle(x2, y2)

model_reg = Sequential()
model = load_model("models_finaux/petit_lstm_g/14-1.00.h5")
model_reg.add(Input(shape=(None, 100, 100, 6)))
for layer in model.layers[:-1]:
    layer.trainable = False
    model_reg.add(layer)

model_reg.add(Dense(16))
model_reg.add(Dense(16))
model_reg.add(Dense(1, activation="sigmoid"))
model_reg.summary()

model_reg.compile(
    optimizer='sgd',
    loss='mse',
    metrics=['mse']
)

checkpoint = ModelCheckpoint(
    filepath='model/transfert/{epoch:02d}-{val_mse:.2f}.h5', 
    monitor="mse", mode="min", 
    save_best_only=True, verbose=1
)
callbacks = [checkpoint]


history = model_reg.fit(
    x2, y2,
    batch_size=16, 
    validation_split = 0.1,
    # class_weight=class_weight,
    epochs=1_000, callbacks=callbacks
)
    


