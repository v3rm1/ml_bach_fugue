import numpy as np
import pickle

### SET UP
norm_file = []
offsets = [0, 0, 12, 24]

text_file = open("quartet_corpus.txt", "r")
for line in text_file:
	track_values = line.split()
	norm_line = []
	for t in range(0,4):
		track_pitch = int(track_values[t])
		if not track_pitch == 0:
			track_pitch += offsets[t]
		norm_line.append(track_pitch)
	norm_file.append(norm_line)
text_file.close()

print("Load list of words")
newfile1 = open("list_of_words.obj", 'rb')
list_of_words = pickle.load(newfile1, encoding='latin1')
newfile1.close()

print("Converting file to word format (with indices)")
word_file = []
for i in range(0,int(len(norm_file)/4)):
    line = []
    for t in range(0,4):
        word = str(norm_file[i*4][t]) + "-" + str(norm_file[i*4+1][t]) + "-" + str(norm_file[i*4+2][t]) + "-" + str(norm_file[i*4+3][t])
        idx = list_of_words.index(word)
        line.append(idx)
    word_file.append(line)
del norm_file

### encode the file

f = open("embeddings.obj", 'rb')
embeddingList = pickle.load(f)

print("Converting the file to embedded format")
embed_file = np.zeros((len(word_file), 800))
for i in range(len(word_file)):
    vector = np.concatenate((embeddingList[word_file[i][0]][1], embeddingList[word_file[i][1]][1], embeddingList[word_file[i][2]][1], embeddingList[word_file[i][3]][1]), axis=1)
    embed_file[i] = np.array(vector)
del word_file
    
filehandler = open("embedded_corpus.obj", 'wb') 
pickle.dump(embed_file, filehandler)
filehandler.close()
