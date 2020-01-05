from midiutil.MidiFile import MIDIFile

###Class Definitions
class Note:
	def __init__(self, time = 0, pitch = 0):
		self.duration = 0.125
		self.time = time
		self.pitch = pitch
	def add_dur(self):
		self.duration += 0.125

###Function Definitions
def add_note_to_track(track, note, mf):
	if not note.pitch == 0:	#pitch of 0 means no note is being played
		volume = 100
		channel = 0
		mf.addNote(track, channel, note.pitch, note.time, note.duration, volume)

###Main file##################################################################################

# create your MIDI object
mf = MIDIFile(4)     # 4 tracks

time = 0    # start at the beginning
beats_per_minute = 150

mf.addTrackName(0, time, "Track 1")
mf.addTempo(0, time, beats_per_minute)
mf.addTrackName(1, time, "Track 2")
mf.addTempo(1, time, beats_per_minute)
mf.addTrackName(2, time, "Track 3")
mf.addTempo(2, time, beats_per_minute)
mf.addTrackName(3, time, "Track 4")
mf.addTempo(3, time, beats_per_minute)

#initialize a list which stores notes, and only adds them to the midi after the full duration is known
note_storage = [Note(), Note(), Note(), Note()]

text_file = open("F.txt", "r")
for line in text_file:
	track_values = line.split()
	for t in range(0,4):
		track_pitch = int(track_values[t])
		current_note = note_storage[t]
		if track_pitch == current_note.pitch:
			current_note.add_dur()
			note_storage[t] = current_note
		else:
			add_note_to_track(t, current_note, mf)
			note_storage[t] = Note(time, track_pitch)
	time += 0.125 #move 1/8 beat into the future

#After text file ends, add the remaining notes
for i in range(0,4):
	add_note_to_track(i, note_storage[i], mf)

# write it to disk
with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)
