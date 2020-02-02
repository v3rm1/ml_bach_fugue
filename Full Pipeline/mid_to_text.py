import mido
import os

majors = dict([('Ab', 4), ('G#', 4), ('A', 3), ('A#', 2), ('Bb', 2), ('B', 1), ('C', 0), ('C#', -1), ('Db', -1), ('D', -2),
               ('D#', -3), ('Eb', -3), ('E', -4), ('F', -5), ('F#', 6), ('Gb', 6), ('G', 5)])

def get_key_sig(mid):
    track_0 = mid.tracks[0]
    for msg in track_0:
        if msg.is_meta and msg.type == "key_signature":
            return msg.key
    return "error"

def get_tempo(mid):
    track_0 = mid.tracks[0]
    for msg in track_0:
        if msg.is_meta and msg.type == "set_tempo":
            return mido.tempo2bpm(msg.tempo)
    return "error"

def get_time_sig(mid):
	track_0 = mid.tracks[0]
	t_s = ""
	for msg in track_0:
		if msg.is_meta and msg.type == "time_signature":
			if t_s == "":
				t_s = str(msg.numerator) + "/" + str(msg.denominator)
			else:
				return "yuck"
	return t_s

#COLLECT ALL MIDI FILES
all_files = os.listdir("MIDI_dir")
all_music = []
for f in all_files:
    print(f)
    mid = mido.MidiFile("MIDI_dir/" + f)
    time_sig = get_time_sig(mid)
    if not time_sig == "4/4":
        os.remove("MIDI_dir/" + f)
    else:
        if len(mid.tracks) >= 5:
            all_music.append(mid)



#
corpus = []
for piece in all_music:
    k_s = get_key_sig(piece)
    tempo = get_tempo(piece)
    key_offset = majors[k_s]
    ticks_per_16 = piece.ticks_per_beat / 4
    if tempo < 60:
        ticks_per_16 /= 2
    if tempo > 120:
        ticks_per_16 *= 2
    converted_piece = []
    for i in range(4):
        track = piece.tracks[i+1]
        current_16th = 0
        time_offset = 0 # this is janky, but we cannot accept 3rds!!!!
        for j in range(len(track)):
            msg = track[j]
            #print(msg)
            if msg.type == "note_on":
                note = msg.note + key_offset
                if msg.velocity > 0:
                    note = 0

				#figure out how long the note is in 16th notes. Note that 3rds are forced to fit
                n_16ths_float = msg.time / ticks_per_16 + time_offset
                n_16ths = int(n_16ths_float)
                time_offset = (n_16ths_float - n_16ths)


                for k in range(n_16ths):
                    if len(converted_piece) <= current_16th:
                        converted_piece += [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
                    converted_piece[current_16th][i] = note
                    current_16th += 1
    corpus = corpus + converted_piece

if os.path.exists("quartet_corpus.txt"):
    os.remove("quartet_corpus.txt")

### send to text file
f = open("quartet_corpus.txt", "x")
for print_line in corpus:
    f.write(str(print_line[0])+ "\t" + str(print_line[1]) + "\t" + str(print_line[2])+ "\t" + str(print_line[3]) + "\n")
						
print(len(corpus))
	

