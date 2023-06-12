from pyo import *
import random
from ga_options import *
import time
import instruments

def metronome(bpm: int):
    met = Metro(time=1 / (bpm / 60.0)).play()
    t = CosTable([(0, 0), (50, 1), (200, .3), (500, 0)])
    amp = TrigEnv(met, table=t, dur=.25, mul=1)
    freq = Iter(met, choice=[660, 440, 440, 440])
    return Sine(freq=freq, mul=amp).mix(2).out()

def tuning(scale: EventScale, bpm: int, tact_numbers: int, notes_per_tact: int, solution: list):
    server = Server().boot()

    m = metronome(bpm)

    num_notes = tact_numbers*notes_per_tact

    note_list_1 = []
    note_list_2 = []
    note_list_3 = []

    durr = []
    #durr = 4 / notes_per_tact
    db1 = []
    db2 = []
    db3 = []
    
    notes_per_sec = bpm/60
    
    for i in range(num_notes):
        if 0 <= solution[i+num_notes] < 3:
            note_list_1.append(scale[solution[i]])
            db1.append(-12)
            note_list_2.append(scale[1])
            db2.append(-100)
            note_list_3.append(scale[1])
            db3.append(-100)
        else:
            note_list_1.append(scale[solution[i]])
            db1.append(-12)
            note_list_2.append(scale[solution[i]+2])
            db2.append(-12)
            note_list_3.append(scale[solution[i]+4])
            db3.append(-12)
        #durr.append(float(solution[i+2*num_notes]/notes_per_sec))
        durr.append(float(solution[i+2*num_notes]))
        
        '''elif 5 <= solution[i+num_notes] < 7:
            note_list_1.append(scale[solution[i]])
            db1.append(-12)
            note_list_2.append(scale[solution[i]+2])
            db2.append(-12)
            note_list_3.append(scale[1])
            db3.append(-100)'''

    attack = 0.001
    decay = 0.05
    sustain = 0.5
    release = 0.005

# We tell the Events object which instrument to use with the 'instr' argument.
    e1 = Events(
        #instr=getattr(instruments, instrument),
        midinote=EventSeq(note_list_1, 1),
        #dur=durr,
        beat=durr,
        bpm=bpm,
        db=db1,
        attack=attack,
        decay=decay,
        sustain=sustain,
        release=release,
    ).play()

    e2 = Events(
        #instr=getattr(instruments, instrument),
        midinote=EventSeq(note_list_2, 1),
        #dur=durr,
        beat=durr,
        bpm=bpm,
        db=db2,
        attack=attack,
        decay=decay,
        sustain=sustain,
        release=release,
    ).play()

    e3 = Events(
        #instr=getattr(instruments, instrument),
        midinote=EventSeq(note_list_3, 1),
        #dur=durr,
        beat=durr,
        bpm=bpm,
        db=db3,
        attack=attack,
        decay=decay,
        sustain=sustain,
        release=release,
    ).play()

    '''for i in range(len(note_list_1)):
        e1 = Events(
        instr=getattr(instruments, instrument),
        midinote=EventSeq(note_list_1[i], 1),
        dur=durr[i],
        #beat=durr[i],
        bpm=bpm,
        db=db1[i],
        attack=attack,
        decay=decay,
        sustain=sustain,
        release=release,
    ).play()

    e2 = Events(
        instr=getattr(instruments, instrument),
        midinote=EventSeq(note_list_2[i], 1),
        dur=durr[i],
        #beat=durr[i],
        bpm=bpm,
        db=db2[i],
        attack=attack,
        decay=decay,
        sustain=sustain,
        release=release,
    ).play()

    e3 = Events(
        instr=getattr(instruments, instrument),
        midinote=EventSeq(note_list_3[i], 1),
        dur=durr[i],
        #beat=durr[i],
        bpm=bpm,
        db=db3[i],
        attack=attack,
        decay=decay,
        sustain=sustain,
        release=release,
    ).play()'''

    server.start()

    #time.sleep(notes_per_tact*tact_numbers* durr/(bpm/60))
    time.sleep(sum(durr)/(bpm/60))

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
