import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, Input, Flatten, Reshape, ConvLSTM2D, MaxPooling2D, Dropout
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
df1 = pd.read_csv("Challenge_2_submission_template.csv", parse_dates=['Date of Harvest'], date_parser=dateparse)
df1

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

x1 = []
y1 = []
for i in range(len(df1)):
    with open(f"inputs_lstm_val/{i}.npy", "rb") as f:
        arr = np.load(f)
        arr = np.transpose(arr, (0, 2, 3, 1))
        arr = (arr-mini)/multi
        x1.append(arr)
    if df1.loc[i, "Season(SA = Summer Autumn, WS = Winter Spring)"] == "SA":
        y1.append([1, 0])
    else:
        y1.append([0, 1])

x2 = []
y2 = []
for i in range(len(df2)):
    with open(f"inputs_lstm/{i}.npy", "rb") as f:
        arr = np.load(f)
        arr = np.transpose(arr, (0, 2, 3, 1))
        arr = (arr-mini)/multi
        x2.append(arr)
    if df2.loc[i, "Season(SA = Summer Autumn, WS = Winter Spring)"] == "SA":
        y2.append([1, 0])
    else:
        y2.append([0, 1])

x1 = pad_sequences(x1, dtype="float", maxlen=32)
y1 = np.array(y1)
x2 = pad_sequences(x2, dtype="float", maxlen=32)
y2 = np.array(y2)
# x2, y2 = shuffle(x2, y2)

class_weight = {
    0: 1/np.count_nonzero(y2[:, 0]==1),
    1: 1/np.count_nonzero(y2[:, 1]==1)
}



model = Sequential()
model.add(Input(shape=(None,100, 100, 6)))
model.add(ConvLSTM2D(filters=3, kernel_size=3, return_sequences=False))

pretrained = ResNet50(
    include_top=False, 
    input_shape=model.output_shape[1:]
)
for layer in pretrained.layers:
    layer.trainable = False
    
model.add(pretrained)
model.add(MaxPooling2D())
model.add(Flatten())
model.add(Dense(32))
model.add(Dense(16))
model.add(Dropout(0.4))
model.add(Dense(2, activation="softmax"))


model.summary()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

checkpoint = ModelCheckpoint(
    filepath='model/petit_lstm_g/{epoch:02d}-{val_accuracy:.2f}.h5', 
    monitor="val_accuracy", mode="max", 
    save_best_only=True, verbose=1
)
callbacks = [checkpoint]


history = model.fit(
    x2, y2, shuffle=True,
    batch_size=16, 
    validation_data = (x1, y1),
    # class_weight=class_weight,
    epochs=1_000, callbacks=callbacks
)



        


