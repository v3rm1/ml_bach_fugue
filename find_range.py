mins = [999, 999, 999, 999]
maxs = [0, 0, 0, 0]

text_file = open("F.txt", "r")
for line in text_file:
	track_values = line.split()
	for t in range(0,4):
		track_pitch = int(track_values[t])
		if not track_pitch == 0: #values of 0 are rests
			if track_pitch > maxs[t]:
				maxs[t] = track_pitch
			if track_pitch < mins[t]:
				mins[t] = track_pitch

for t in range(0,4):
	print("Track ", t, ": From ", mins[t], " to ", maxs[t])
	print("\tRange: ", maxs[t] - mins[t], " plus 1 for rests")
