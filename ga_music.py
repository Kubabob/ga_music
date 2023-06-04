from pyo import *
import random
from ga_options import *
import time
import instruments

def tuning(scale: EventScale, bpm: int, instrument: EventInstrument, tact_numbers: int, notes_per_tact: int, solution: list[int]):
    server = Server().boot()


    note_list = []
    
    for sol in solution:
        note_list.append(scale[sol])


# We tell the Events object which instrument to use with the 'instr' argument.
    e = Events(
        instr=getattr(instruments, instrument),
        midinote=EventSeq(note_list, 1),
        beat=1 / (bpm/60),
        db=-12,
        attack=0.01,
        decay=0.05,
        sustain=0.7,
        release=0.01,
    ).play()

    server.start()

    time.sleep((tact_numbers*notes_per_tact)/(bpm/60))

    server.stop()


'''tuning(key=option(KEYS, 'C', 'Klucz', str),
       scale=option(SCALES, 'major', 'Skala', str),
       population_count=option(None, 10, 'Liczba na populacje', int),
       mutation_prob=option(None, 0.5, 'Prawdopodobienstwo mutacji [0-1]', float),
       bpm=option(None, 120, 'Tempo [0-128]', int),
       octaves_count=option(None, 2, 'Liczba oktaw', int),
       first_octave=option(None, 4, 'Numer pierwszej oktawy', int),
       instrument=option(INSTRUMENTS, 'MyInstrument', 'Wybierz instrument', str),
       tact_numbers=option(None, 2, 'Liczba taktów', int),
       notes_per_tact=option(None, 4, 'Liczba nut na takt', int),
       is_pause=option(IS_PAUSE, False, 'Czy uwzględniać pauzy', bool),
       solution=[0,1,2,3,4,5])'''
