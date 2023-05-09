#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, Input, Flatten, Reshape, ConvLSTM2D, MaxPooling2D
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
# fix random seed for reproducibility
tf.random.set_seed(7)


# In[3]:


dateparse = lambda x: datetime.strptime(x, '%d-%m-%Y')
df = pd.read_csv("Challenge_2_submission_template.csv", parse_dates=['Date of Harvest'], date_parser=dateparse)
df


# In[4]:


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


# In[31]:


x = []
y = []
for i in range(len(df)):
    with open(f"inputs_lstm_val/{i}.npy", "rb") as f:
        arr = np.load(f)
        arr = np.transpose(arr, (0, 2, 3, 1))
        arr = (arr-mini)/multi
        x.append(arr)
    if df.loc[i, "Season(SA = Summer Autumn, WS = Winter Spring)"] == "SA":
        y.append([1, 0])
    else:
        y.append([0, 1])
x = pad_sequences(x)
y = np.array(y)
# x, y = shuffle(x, y)


# In[6]:


class_weight = {
    0: 1/np.count_nonzero(y[:, 0]==1),
    1: 1/np.count_nonzero(y[:, 1]==1)
}


# In[7]:


np.count_nonzero(y[:, 0]==1)


# In[8]:


np.count_nonzero(y[:, 1]==1)


# In[32]:


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
model.add(Flatten())
model.add(Dense(10))
model.add(Dense(2, activation="softmax"))
model.summary()


# In[33]:


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[34]:


# import os
# checkpoint = ModelCheckpoint(filepath='model.{epoch:02d}-{val_loss:.2f}.h5', monitor="val_loss", mode="min", save_best_only=True, verbose=1)
checkpoint = ModelCheckpoint(
    filepath='model/{epoch:02d}-{accuracy:.2f}.h5', 
    monitor="accuracy", mode="max", 
    save_best_only=True, verbose=1
)
callbacks = [checkpoint]


# In[35]:
history = model.fit(
    x, y, 
    batch_size=10, shuffle=True, 
    # class_weight=class_weight,
    epochs=1_000, callbacks=callbacks
)

# In[103]:


import time
print(time.asctime())

