import numpy as np
import pickle
from keras.models import Sequential
from keras.layers import Dense, LSTM, Bidirectional, Lambda

def get_similarity(a, b):
    dist = np.linalg.norm(a-b)
    return dist

### Preproccessing stuff........

f = open("embeddings.obj", 'rb')
embeddingList = pickle.load(f)
f.close()

f = open("list_of_words.obj", 'rb')
list_of_words = pickle.load(f)
f.close()

###Main
print('Build model...')
maxlen = 20
model = Sequential()
model.add(LSTM(800, return_sequences = True, input_shape=(maxlen, 800)))
model.add(LSTM(800))
model.add(Dense(800))

# load weights into new model
model.load_weights("lstm_model_v2.h5")
print("Loaded model from disk")

input_matrix = np.zeros((maxlen, 800))

new_music = np.zeros((400,800))
for i in range(400):
    print(i)
    inp = input_matrix[np.newaxis,...]
    output = model.predict(inp)
    
    output_0 = output[0][:200]
    output_1 = output[0][200:400]
    output_2 = output[0][400:600]
    output_3 = output[0][600:]
    embeddingList.sort(key = lambda x: get_similarity(x[1], output_0))
    reg_0 = embeddingList[0][1]
    embeddingList.sort(key = lambda x: get_similarity(x[1], output_1))
    reg_1 = embeddingList[0][1]
    embeddingList.sort(key = lambda x: get_similarity(x[1], output_2))
    reg_2 = embeddingList[0][1]
    embeddingList.sort(key = lambda x: get_similarity(x[1], output_3))
    reg_3 = embeddingList[0][1]
    
    reg_out = np.concatenate((reg_0, reg_1, reg_2, reg_3), axis = 1)
    
    new_music[i] = reg_out
    input_matrix = np.concatenate((input_matrix[-(maxlen-1):],reg_out))
    
filehandler = open("new_music.obj", 'wb') 
pickle.dump(new_music, filehandler)
filehandler.close()
    
