Pipeline:

mid_to_text     --> quartet_corpus.txt
word2vec_setup  --> list_of_words.obj, input_data_w2v.obj, output_data_w2v.obj
word2vec        --> embeddings.obj
embed_corpun    --> embedded_corpus.obj
lstm_train      --> lstm_model.h5
lstm_test       --> new_music.obj
embed_to_text   --> new_music.txt
text_to_mid     --> output.mid
