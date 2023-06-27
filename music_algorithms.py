from ga_options import *
import time
from midiutil import MIDIFile


def metronome(bpm: int):
    met = Metro(time=1 / (bpm / 60.0)).play()
    t = CosTable([(0, 0), (50, 1), (200, .3), (500, 0)])
    amp = TrigEnv(met, table=t, dur=.25, mul=1)
    freq = Iter(met, choice=[660, 440, 440, 440])
    return Sine(freq=freq, mul=amp).mix(2).out()


class Music_algorithms:
    '''
    Backend of genetic algorithm music, sets server, metronome and saves file.
    '''

    def __init__(self, scale: EventScale, bpm: int, tact_numbers: int, notes_per_tact: int):
        self.note_list_1 = []
        self.note_list_2 = []
        self.note_list_3 = []
        self.durr = []
        self.vel1 = []
        self.vel2 = []
        self.vel3 = []
        self.num_notes = tact_numbers*notes_per_tact
        self.bpm = bpm
        self.scale = scale

    def play_music(self, solution: list):
        server = Server(nchnls=1).boot()

        self.note_list_1 = []
        self.note_list_2 = []
        self.note_list_3 = []
        self.durr = []
        self.vel1 = []
        self.vel2 = []
        self.vel3 = []

        m = metronome(self.bpm)
        
        
        for i in range(self.num_notes):
            if 0 <= solution[i+self.num_notes] < 4:
                self.note_list_1.append(self.scale[solution[i]])
                self.vel1.append(100)
                self.note_list_2.append(self.scale[1])
                self.vel2.append(0)
                self.note_list_3.append(self.scale[1])
                self.vel3.append(0)
            elif 4 <= solution[i+self.num_notes] < 7:
                self.note_list_1.append(self.scale[solution[i]])
                self.vel1.append(100)
                self.note_list_2.append(self.scale[solution[i]+2])
                self.vel2.append(100)
                self.note_list_3.append(self.scale[1])
                self.vel3.append(0)
            else:
                self.note_list_1.append(self.scale[solution[i]])
                self.vel1.append(100)
                self.note_list_2.append(self.scale[solution[i]+2])
                self.vel2.append(100)
                self.note_list_3.append(self.scale[solution[i]+4])
                self.vel3.append(100)
            self.durr.append(float(solution[i+2*self.num_notes]))
        else:
            self.note_list_1.append(self.scale[0])
            self.note_list_2.append(self.scale[2])
            self.note_list_3.append(self.scale[4])

            self.vel1.append(100)
            self.vel2.append(100)
            self.vel3.append(100)

            self.durr.append(2)
            
        
        attack = 0.001
        decay = 0.05
        sustain = 0.5
        release = 0.005

        e1 = Events(
            midinote=EventSeq(self.note_list_1, 1),
            midivel=self.vel1,
            beat=self.durr,
            bpm=self.bpm,
            attack=attack,
            decay=decay,
            sustain=sustain,
            release=release,
        ).play()

        e2 = Events(
            midinote=EventSeq(self.note_list_2, 1),
            midivel=self.vel2,
            beat=self.durr,
            bpm=self.bpm,
            attack=attack,
            decay=decay,
            sustain=sustain,
            release=release,
        ).play()

        e3 = Events(
            midinote=EventSeq(self.note_list_3, 1),
            midivel=self.vel3,
            beat=self.durr,
            bpm=self.bpm,
            attack=attack,
            decay=decay,
            sustain=sustain,
            release=release,
        ).play()

        
        server.start()

        time.sleep(sum(self.durr)/(self.bpm/60)+0.5)

        server.stop()

    def save_melody_to_midi(self, filename: str, solution):

        self.note_list_1 = []
        self.note_list_2 = []
        self.note_list_3 = []
        self.durr = []
        self.vel1 = []
        self.vel2 = []
        self.vel3 = []
        
        print(solution)
        
        for i in range(self.num_notes):
            if 0 <= solution[i+self.num_notes] < 4:
                self.note_list_1.append(self.scale[solution[i]])
                self.vel1.append(100)
                self.note_list_2.append(self.scale[1])
                self.vel2.append(0)
                self.note_list_3.append(self.scale[1])
                self.vel3.append(0)
            elif 4 <= solution[i+self.num_notes] < 7:
                self.note_list_1.append(self.scale[solution[i]])
                self.vel1.append(100)
                self.note_list_2.append(self.scale[solution[i]+2])
                self.vel2.append(100)
                self.note_list_3.append(self.scale[1])
                self.vel3.append(0)
            else:
                self.note_list_1.append(self.scale[solution[i]])
                self.vel1.append(100)
                self.note_list_2.append(self.scale[solution[i]+2])
                self.vel2.append(100)
                self.note_list_3.append(self.scale[solution[i]+4])
                self.vel3.append(100)
            self.durr.append(float(solution[i+2*self.num_notes]))
        else:
            self.note_list_1.append(self.scale[0])
            self.note_list_2.append(self.scale[2])
            self.note_list_3.append(self.scale[4])

            self.vel1.append(60)
            self.vel2.append(60)
            self.vel3.append(60)

            self.durr.append(2)

        mf = MIDIFile(1)

        track = 0
        channel = 0
        time = 0.0
        mf.addTrackName(track, time, filename)
        mf.addTempo(track, time, self.bpm)

        for i in range(len(self.note_list_1)):
            mf.addNote(track, channel, self.note_list_1[i], time, self.durr[i], self.vel1[i])
            mf.addNote(track, channel, self.note_list_2[i], time, self.durr[i], self.vel2[i])
            mf.addNote(track, channel, self.note_list_3[i], time, self.durr[i], self.vel3[i])
            time += self.durr[i]


        with open(f'{filename}.mid', 'wb') as file:
            mf.writeFile(file)
