import numpy as np
import pickle
from keras.models import Sequential
from keras.layers import Dense, LSTM, Bidirectional, Lambda
from keras.optimizers import RMSprop
import tensorflow as tf

### MAIN
f = open("embedded_corpus.obj", 'rb')
corpus = pickle.load(f)

print('Build model...')
maxlen = 20
model = Sequential()
model.add(LSTM(800, return_sequences = True, input_shape=(maxlen, 800)))
model.add(LSTM(800))
model.add(Dense(800))
optimizer = RMSprop(lr=0.01)
model.compile(loss='mse', optimizer=optimizer)

# load weights into new model
#model.load_weights("lstm_model.h5")
#print("Loaded model from disk")

print('Set up training data')
input_data = np.zeros((len(corpus)-maxlen, maxlen, 800))
output_data = np.zeros((len(corpus)-maxlen, 800))

for i in range(0, len(corpus)-maxlen):
    input_data[i] = corpus[i:i+maxlen]
    output_data[i] = corpus[i+maxlen]

model.fit(input_data, output_data, batch_size=32, epochs=10, verbose=2)

# serialize weights to HDF5
model.save_weights("lstm_model.h5")
print("Saved model to disk")
