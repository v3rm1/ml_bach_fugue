import pickle
import numpy as np

def get_similarity(a, b):
    dist = np.linalg.norm(a-b)
    return dist

f = open("embeddings.obj", 'rb')
embeddingList = pickle.load(f)
D = {line[0] : line[1] for line in embeddingList}

while True:
    print("Give a word, to get the 10 most similar words. (use form x-x-x-x)")
    key = input()
    X = D[key]
    embeddingList.sort(key = lambda x: get_similarity(x[1], X))
    for i in range(10):
        print(embeddingList[i][0], " : ", get_similarity(embeddingList[i][1], X))
            

    

