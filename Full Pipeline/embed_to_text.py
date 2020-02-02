import pickle
import numpy as np

def get_string(embeddingList, embedded_word):
    for line in embeddingList:
        if (line[1] == embedded_word).all():
            return line[0]
    print("ERROR")
    quit()

norm_file = []
offsets = [0, 0, 12, 24]

f = open("new_music.obj", 'rb')
embedded_music = pickle.load(f)
f.close()

f = open("embeddings.obj", 'rb')
embeddingList = pickle.load(f)
f.close()


norm_file = np.zeros((len(embedded_music)*4,4))
for i in range(len(embedded_music)):
    embedded_line = embedded_music[i]
    for t in range(4):
        embedded_word = embedded_line[t*200:(t+1)*200]
        str_word = get_string(embeddingList, embedded_word)
        str_word = str_word.split("-")
        list_notes = [int(str_word[i]) for i in range(len(str_word))]
        for j in range(4):
            if list_notes[j] == 0:
                norm_file[i*4+j][t] = 0
            else:
                norm_file[i*4+j][t] = list_notes[j] - offsets[t]

f = open("new_music.txt", "w")
for print_line in norm_file:
    f.write(str(int(print_line[0]))+ "\t" + str(int(print_line[1])) + "\t" + str(int(print_line[2]))+ "\t" + str(int(print_line[3])) + "\n")
