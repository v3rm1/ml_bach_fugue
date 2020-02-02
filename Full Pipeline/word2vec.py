import pickle
import keras
from keras.utils import to_categorical
from keras.layers import Dense
from keras.models import model_from_json
import numpy as np
import os

newfile1 = open("list_of_words.obj", 'rb')
list_of_words = pickle.load(newfile1, encoding='latin1')
newfile1.close()

newfile2 = open("input_data_w2v.obj", 'rb')
input_data = pickle.load(newfile2, encoding='latin1')
newfile2.close()

newfile3 = open("output_data_w2v.obj", 'rb')
output_data = pickle.load(newfile3, encoding='latin1')
newfile3.close()
    
###BUILD THE EMBEDDINGS########################################################################
   
# Build the model.
model = keras.Sequential([
  Dense(200, input_shape=(len(list_of_words),)),
  Dense(len(list_of_words), activation='softmax'),
])
model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])

# load weights into new model
model.load_weights("model_real.h5")
print("Loaded model from disk")

TRAINING_ITER = 10
subset_size = 200000
    
for i in range(TRAINING_ITER):
    print("Iteration: ", i)
    
    #shuffle the data
    order = np.arange(len(input_data))
    np.random.shuffle(order)
    input_data = input_data[order]
    output_data = output_data[order]
    
    #loop over subsets of data
    idx_left = 0
    while idx_left < len(input_data):
        idx_right = min(len(input_data), idx_left + subset_size)
        encode_in = to_categorical(input_data[idx_left:idx_right], len(list_of_words))
        encode_out = to_categorical(output_data[idx_left:idx_right], len(list_of_words))
        model.fit(encode_in, encode_out, epochs=1, batch_size=32, verbose=2)
        idx_left += subset_size
        
#create embeddingifier model
embed_model= keras.Sequential([
    Dense(200, input_shape=(len(list_of_words),)),
])

#set weights of the first layer
embed_model.set_weights(model.layers[0].get_weights())

save_embeddings = []
for i in range(len(list_of_words)):
    vector = embed_model.predict(to_categorical([i], len(list_of_words)))
    word = list_of_words[i]
    save_embeddings.append([word, vector])
    
filehandler = open("embeddings.obj", 'wb') 
pickle.dump(save_embeddings, filehandler)
filehandler.close()


# serialize weights to HDF5
model.save_weights("model_real.h5")
print("Saved model to disk")



    
    
    

