import numpy as np

###Class definitions

class Model:
	def __init__(self, unigrams, bigrams):
		self.unigrams = unigrams
		self.bigrams = bigrams
	def get_note_probabilities(self, last_line):
		prior = self.unigrams
		cond_0 = self.bigrams[0][last_line[0]]
		cond_1 = self.bigrams[1][last_line[1]]
		cond_2 = self.bigrams[2][last_line[2]]
		cond_3 = self.bigrams[3][last_line[3]]

		total_prob = np.array(prior) * np.array(cond_0) * np.array(cond_1) * np.array(cond_2) * np.array(cond_3)
		final_prob = total_prob / sum(total_prob)

		#add smoothing
		for i in range(len(final_prob)):
			final_prob[i] += 0.01
		final_prob = final_prob / sum(final_prob)

		return final_prob
		
###Main###################################################################################################

#These are the ranges and lowest notes for each of the 4 tracks
ranges = [23, 27, 23, 27]
lowest_notes = [54, 45, 40, 28]

#normalize text file notes to start from 1
norm_file = []

text_file = open("F.txt", "r")
for line in text_file:
	track_values = line.split()
	norm_line = []
	for t in range(0,4):
		track_pitch = int(track_values[t])
		if not track_pitch == 0:
			track_pitch -= lowest_notes[t]
			track_pitch += 1
		norm_line.append(track_pitch)
	norm_file.append(norm_line)

#These are the probability models for each track
models = []

###Get Unigram probabilities
unigram_count = [[0 for j in range(0, ranges[i] + 1)] for i in range(0,4)]
for line in norm_file:
	for t in range(0,4):
		track_pitch = line[t]
		unigram_count[t][track_pitch] += 1

unigram_probs = [[0 for j in range(0, ranges[i] + 1)] for i in range(0,4)]
for t in range(0,4):
	sum_count = sum(unigram_count[t])
	for i in range(0, len(unigram_count[t])):
		unigram_probs[t][i] = unigram_count[t][i] / sum_count

###Get Bigram probabilities
for t in range(0,4):
	bigram_count = [[[0 for k in range(0,ranges[t] + 1)] for j in range(0, ranges[i] + 1)] for i in range(0,4)]
	previous_pitches = [0, 0, 0, 0]
	for line in norm_file:
		current_pitch = line[t]
		for p in range(0,4):
			bigram_count[p][previous_pitches[p]][current_pitch] += 1
		previous_pitches = line
	
	## add plus-one smoothing
	for i in range(0,len(bigram_count)):
		for j in range(0, len(bigram_count[i])):
			for k in range(0, len(bigram_count[i][j])):
				bigram_count[i][j][k] += 1

	## get probs
	bigram_probs = [[[0 for k in range(0,ranges[t] + 1)] for j in range(0, ranges[i] + 1)] for i in range(0,4)]
	for i in range(0,len(bigram_count)):
		for j in range(0, len(bigram_count[i])):
			sum_count = sum(bigram_count[i][j])
			for k in range(0, len(bigram_count[i][j])):
				bigram_probs[i][j][k] = bigram_count[i][j][k] / sum_count

	## create a full model containing both unigram and bigram probabilities
	models.append(Model(unigram_probs[t], bigram_probs))

###Predict notes#######################################################################################################
new_file = open("new_bach.txt", "x")

previous_pitches = norm_file[-13]
for i in range(0,1000):
	new_line = []
	for t in range(0, 4):
		probs = models[t].get_note_probabilities(previous_pitches)
		choice = np.random.choice(np.arange(0, ranges[t] +1), p=probs)
		new_line.append(choice)
	previous_pitches = new_line
	print_line = []
	for j in range(0,4):
		pitch = new_line[j]
		if not pitch == 0:
			pitch += lowest_notes[j]
			pitch -= 1
		print_line.append(pitch)
	new_file.write(str(print_line[0])+ "\t" + str(print_line[1]) + "\t" + str(print_line[2])+ "\t" + str(print_line[3]) + "\n")
	

new_file.close()

