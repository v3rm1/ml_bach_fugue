import pickle
import numpy as np
import os

### Make a set of words
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
    
print("Making set of words...")
set_of_words = set()
for t in range(0,4):
	for i in range(0,int(len(norm_file)/4)):
		word = str(norm_file[i*4][t]) + "-" + str(norm_file[i*4+1][t]) + "-" + str(norm_file[i*4+2][t]) + "-" + str(norm_file[i*4+3][t])
		set_of_words.add(word)
        
list_of_words = list(set_of_words)
del set_of_words
print(str(len(list_of_words)) + " words found")

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
    
###Generate word2vec dataset
print("Generate dataset for skipgram model")

#t-2
input_t_min_2 = np.empty(4*(len(word_file)-2))
output_t_min_2 = np.empty(4*(len(word_file)-2))
for i in range(len(word_file)-2):
    for t in range(4):
        input_t_min_2[4*i+t] = word_file[i+2][t]
        output_t_min_2[4*i+t] = word_file[i][t]
        
#t-1
input_t_min_1 = np.empty(4*(len(word_file)-1))
output_t_min_1 = np.empty(4*(len(word_file)-1))
for i in range(len(word_file)-1):
    for t in range(4):
        input_t_min_1[4*i+t] = word_file[i+1][t]
        output_t_min_1[4*i+t] = word_file[i][t]
        
#t+1
input_t_plu_1 = np.empty(4*(len(word_file)-1))
output_t_plu_1 = np.empty(4*(len(word_file)-1))
for i in range(len(word_file)-1):
    for t in range(4):
        input_t_plu_1[4*i+t] = word_file[i][t]
        output_t_plu_1[4*i+t] = word_file[i+1][t]
        
#t-2
input_t_plu_2 = np.empty(4*(len(word_file)-2))
output_t_plu_2 = np.empty(4*(len(word_file)-2))
for i in range(len(word_file)-2):
    for t in range(4):
        input_t_plu_2[4*i+t] = word_file[i][t]
        output_t_plu_2[4*i+t] = word_file[i+2][t]
        
#intertrack
input_intertrack = np.empty(12*len(word_file))
output_intertrack = np.empty(12*len(word_file))
for i in range(len(word_file)):
    for t1 in range(4):
        for j in range(3):
            idx = t1*3 + j    #this gives an idx from 0 to 11, for each combination
            t2 = (t1+j+1) % 4 #this ensures t1 never equals t2, and all combinations are added
            input_intertrack[i*12 + idx] = word_file[i][t1]
            output_intertrack[i*12 + idx] = word_file[i][t2]
del word_file
            
input_data = np.concatenate((input_t_min_2, input_t_min_1, input_t_plu_1, input_t_plu_2, input_intertrack))
del input_t_min_2, input_t_min_1, input_t_plu_1, input_t_plu_2, input_intertrack
output_data = np.concatenate((output_t_min_2, output_t_min_1, output_t_plu_1, output_t_plu_2, output_intertrack))
del output_t_min_2, output_t_min_1, output_t_plu_1, output_t_plu_2, output_intertrack

if len(input_data) == len(output_data):
    print(str(len(input_data)) + " data points to be trained")
else:
    print("error dataset made wrong")
    quit()
    
filehandler1 = open("list_of_words.obj", 'wb') 
pickle.dump(list_of_words, filehandler1)
filehandler1.close()
filehandler2 = open("input_data_w2v.obj", 'wb') 
pickle.dump(input_data, filehandler2)
filehandler2.close()
filehandler3 = open("output_data_w2v.obj", 'wb') 
pickle.dump(output_data, filehandler3)
filehandler3.close()
