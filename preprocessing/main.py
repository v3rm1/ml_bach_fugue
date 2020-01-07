import numpy as np
from mido import MidiFile, MidiTrack, Message as MidiMessage
import music21
import converters.convert as cvt


def piano_roll_to_midi(piano_roll):
    """Convert piano roll to a MIDI file."""
    notes, frames = piano_roll.shape
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    now = 0
    piano_roll = np.hstack((np.zeros((notes, 1)),
                            piano_roll,
                            np.zeros((notes, 1))))
    velocity_changes = np.nonzero(np.diff(piano_roll).T)
    for time, note in zip(*velocity_changes):
        velocity = piano_roll[note, time + 1]
        message = MidiMessage(
            type='note_on' if velocity > 0 else 'note_off',
            note=int(note),
            velocity=int(127),
            time=int(time - now))
        track.append(message)
        now = time
    return midi


def transpose_key(filename):
    """ converting everything into the key of C major or A minor
    """
    # major conversions
    majors = dict(
        [("A-", 4), ("A", 3), ("B-", 2), ("B", 1), ("C", 0), ("D-", -1), ("D", -2), ("E-", -3), ("E", -4), ("F", -5),
         ("G-", 6), ("G", 5)])
    minors = dict(
        [("A-", 1), ("A", 0), ("B-", -1), ("B", -2), ("C", -3), ("D-", -4), ("D", -5), ("E-", 6), ("E", 5), ("F", 4),
         ("G-", 3), ("G", 2)])

    score = music21.converter.parse(filename)
    key = score.analyze('key')
    #    print key.tonic.name, key.mode
    if key.mode == "major":
        halfSteps = majors[key.tonic.name]
    elif key.mode == "minor":
        halfSteps = minors[key.tonic.name]

    newscore = score.transpose(halfSteps)
    newFileName = "C_" + filename
    newscore.write('midi', newFileName)


if __name__ == '__main__':
    # transpose_key('test1.mid')

    # mid = MidiFile('C_test1.mid')
    # tpb = mid.ticks_per_beat
    # metamessages, insmessages = cvt.split_tracks(mid)  # Make sure that only 4 instruments are passed forward
    # streams = cvt.notes_to_pitchstream(insmessages, tpb)
    # cvt.pitch_stream_to_text(streams, append=False)

    stream = cvt.text_to_pitch_stream()
    mid = cvt.pitchstream_to_midi(stream)
    mid.save('txt.mid')