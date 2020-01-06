from mido import MidiFile, MidiTrack, Message as MidiMessage
import numpy as np
from music21 import note, stream, chord
import pandas as pd

def pitchstream_to_midi(pitchstream):
    """Convert pitchstream to a MIDI file."""
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    ticks_per_beat = 300
    delta_time = 0
    now = 0
    previous_pitch = 0
    track.append(MidiMessage(type='note_on', note=0, velocity=0, time=0))
    for pitch in pitchstream:
        if pitch != '0':
            # track.append(MidiMessage(type='note_off', note=previous_pitch, velocity=0, time=0))
            # previous_pitch = pitch
            track.append(MidiMessage(type='note_on', note=pitch, velocity=127, time=ticks_per_beat))
            previous_pitch = pitch
            # delta_time = 0
            # now += 1
        elif pitch != previous_pitch:
            track.append(MidiMessage(type='note_off', note=previous_pitch, velocity=0, time=0))
            previous_pitch = pitch
            # delta_time += 1
            # now += 1
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
    :return: array of pitchstream
    """
    pitch_stream = []
    for msg in notes_list:
        if str(msg).split(' ')[0] != 'program_change' and str(msg).split(' ')[0] != 'pitchwheel':
            msg = str(msg).split(' ')
            ticks = int(msg[4].split('=')[-1])
            beats = (ticks*4)//ticks_per_beat  # get by quarter beats
            for i in range(beats):
                if msg[0] == 'note_on' and msg[3].split('=')[-1] != '0':    # some files have note_on but velocity=0
                    pitch_stream.append(msg[2].split('=')[-1])  # add note to stream
                elif msg[0] == 'note_off':
                    pitch_stream.append('0')
    return pitch_stream

def text_to_pitch_stream(file_name='corpus.txt'):
    """Converts text file to pitch stream

    :param file_name: name of the file to read from
    :return: pitch stream
    """
    pitch_stream = []
    with open(file_name, 'r') as f:
        while True:
            c = f.read(1)
            if not c:
                break
            pitch_stream.append(ord(c))
    return pitch_stream

def pitch_stream_to_text(pitch_stream, file_name='corpus.txt', append=True):
    """Converts pitch stream to word file for further analysis

    :param pitch_stream: list of pitches
    :param file_name: name of file in which to save the data
    :param append: True by default
    """
    mode = 'w'
    if append:
        mode = 'a'

    with open(file_name, mode) as f:
        for i, note in enumerate(pitch_stream):
            f.write(chr(int(note)))

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
