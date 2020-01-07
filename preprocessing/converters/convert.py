from mido import MidiFile, MidiTrack, Message as MidiMessage
import numpy as np
from music21 import note, stream, chord
import pandas as pd
import numpy as np

def pitchstream_to_midi(pitchstreams):
    """Convert pitchstream to a MIDI file."""
    midi = MidiFile()

    ticks_per_beat = 300
    if len(pitchstreams[0]) > 1:  # More than one instruments in the track
        tracks = [MidiTrack() for track in range(len(pitchstreams[0]))]
        previous_pitches = [0] * len(pitchstreams[0])
        for track in tracks:
            midi.tracks.append(track)
        for pitchstream in pitchstreams:
            for i, pitches in enumerate(pitchstream):
                tracks[i].append(MidiMessage(type='note_on', note=0, velocity=0, time=0))
                if pitches != '0':
                    tracks[i].append(MidiMessage(type='note_on', note=pitches, velocity=127, time=ticks_per_beat))
                    previous_pitches[i] = pitches
                elif pitches != previous_pitches[i]:
                    tracks[i].append(MidiMessage(type='note_off', note=previous_pitches[i], velocity=0, time=0))
                    previous_pitches[i] = pitches
    else:  # Only one instrument in the track
        track = MidiTrack()
        midi.tracks.append(track)
        track.append(MidiMessage(type='note_on', note=0, velocity=0, time=0))
        for pitch in pitchstreams:
            if pitch != '0':
                track.append(MidiMessage(type='note_on', note=pitch, velocity=127, time=ticks_per_beat))
                previous_pitch = pitch
            elif pitch != previous_pitch:
                track.append(MidiMessage(type='note_off', note=previous_pitch, velocity=0, time=0))
                previous_pitch = pitch

    return midi

def split_tracks(midfile):
    """Break file into different tracks and store them separately

    :param midfile: MidiFile object
    :return: meta messages, instrument messages
    """
    meta_messages = []
    instrument_messages = []
    for i, track in enumerate(midfile.tracks):
        temp_meta_messages = []
        temp_instrument_messages = []
        for msg in track:
            if msg.is_meta:
                temp_meta_messages.append(msg)
            else:
                temp_instrument_messages.append(msg)
        meta_messages.append(temp_meta_messages)
        instrument_messages.append(temp_instrument_messages)
    total_tracks = len(instrument_messages)
    if total_tracks > 4:
        print('Found tracks having more than 4 instruments!\n Removing instruments')
        instrument_messages = instrument_messages[:4]
    return meta_messages, instrument_messages

def combine_tracks(metadata, instrument_tracks):
    """
    Combines array of instruments to MidiFile object
    :param
    instrument_tracks: array of instruments
    metadata: metadata of the conditioning file so that the output is in the same style and key

    :return MidFile object:
    """
    mid = MidiFile()
    header = []
    for data in metadata:
        for msg in data:
            if msg.type == 'smpte_offset' or msg.type == 'time_signature' or msg.type == 'key_signature'\
                    or msg.type == 'set_tempo':
                header.append(data)
                break

    for data in header:
        track = MidiTrack()
        mid.tracks.append(track)
        for elements in data:
            track.append(elements)

    for data in instrument_tracks:
        track = MidiTrack()
        mid.tracks.append(track)
        for elements in data:
            track.append(elements)

    return mid

def notes_to_pitchstream(notes_list, ticks_per_beat):
    """
    Get list of instrument notes and convert to pitchstream
    :param notes_list: obtained from instrument tracks
    ticks_per_beat: calculate beats based on this
    :return: array of pitchstreams
    """

    pitch_streams = []
    for streams in notes_list:
        pitch_stream = []
        for msg in streams:
            if str(msg).split(' ')[0] != 'program_change' and str(msg).split(' ')[0] != 'pitchwheel':
                msg = str(msg).split(' ')
                ticks = int(msg[4].split('=')[-1])
                beats = (ticks*4)//ticks_per_beat  # get by quarter beats
                for i in range(beats):
                    if msg[0] == 'note_on' and msg[3].split('=')[-1] != '0':    # some files have note_on but velocity=0
                        pitch_stream.append(msg[2].split('=')[-1])  # add note to stream
                    elif msg[0] == 'note_off':
                        pitch_stream.append('0')
        pitch_streams.append(pitch_stream)
    return pitch_streams

def text_to_pitch_stream(file_name='corpus.txt'):
    """Converts text file to pitch stream

    :param file_name: name of the file to read from
    :return: pitch stream
    """
    pitch_stream = []
    with open(file_name, 'r') as f:
        while f.readline():
            c = f.readline()
            c = c.split()
            pitch_stream.append([int(a) for a in c])
    return pitch_stream

def pitch_stream_to_text(pitch_stream, file_name='corpus.txt', append=True):
    """Converts pitch stream to word file for further analysis
        One word consists of 4 instruments

    :param pitch_stream: list of pitches | 4 pitch stream list
    :param file_name: name of file in which to save the data
    :param append: True by default
    """
    mode = 'w'
    if append:
        mode = 'a'

    max_length = np.max([len(a) for a in pitch_stream])
    output_arr = np.zeros((max_length, 4), dtype='int8')
    for i, c in enumerate(pitch_stream):
        output_arr[:len(c), i] = [int(a) for a in c]  # convert chr to int
    with open(file_name, mode) as f:
        for notes in output_arr:
            notes = str(notes).strip('[]')
            f.write(notes)
            f.write('\n')

def messages_to_corpus(messages, filename='corpus.txt', append=True):
    """
    Converts midi messages to corpus of encoding to feed into the network
    :param
    messages: array of instrument messages
    filename: Name of the file in which to save the converted text
    append: Overwrites if false
    """
    # todo
    pass

def corpus_to_message(filename='output.txt'):
    """
    Converts the output of the
    :param filename: name of the file generated during prediction
    """
    # todo
    pass
