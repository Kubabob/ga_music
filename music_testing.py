from pyo import *
import time

s = Server().boot()

#s.start()
class funky80(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)

        # self.freq is derived from the 'degree' argument.
        self.phase = Phasor([self.freq, self.freq * 2])

        # self.dur is derived from the 'beat' argument.
        self.duty = Expseg([(0, 9), (self.dur, 0.6)], exp=10).play()

        self.osc = Compare(self.phase, self.duty, mode="<", mul=0.5, add=3)
        #self.osc.ctrl()

        # EventInstrument created the amplitude envelope as self.env.
        self.filt = ButLP(self.osc, freq=10000, mul=self.env).out()

        
scl = EventScale('D', 'minorH')
seq = [scl[random.randint(0,8)] for _ in range(16)]
sql = [scl[i] for i in range(8)]

# We tell the Events object which instrument to use with the 'instr' argument.
e = Events(
    instr=funky80,
    midinote=EventSeq(seq, 1),
    beat=1 / 2.7,
    db=-3,
    attack=0.05,
    decay=0.02,
    sustain=0.3,
    release=0.03,
).play()

'''
s = Server().boot()
s.amp = 0.1

# Start a source sound.
sf = SfPlayer("../snds/baseballmajeur_m.aif", speed=1, loop=True, mul=0.3)
# Mix the source in stereo and send the signal to the output.
sf2 = sf.mix(2).out()

# Sets values for 8 LFO'ed delay lines (you can add more if you want!).
# LFO frequencies.
freqs = [0.254, 0.465, 0.657, 0.879, 1.23, 1.342, 1.654, 1.879]
# Center delays in seconds.
cdelay = [0.0087, 0.0102, 0.0111, 0.01254, 0.0134, 0.01501, 0.01707, 0.0178]
# Modulation depths in seconds.
adelay = [0.001, 0.0012, 0.0013, 0.0014, 0.0015, 0.0016, 0.002, 0.0023]

# Create 8 sinusoidal LFOs with center delays "cdelay" and depths "adelay".
lfos = Sine(freqs, mul=adelay, add=cdelay)

# Create 8 modulated delay lines with a little feedback and send the signals
# to the output. Streams 1, 3, 5, 7 to the left and streams 2, 4, 6, 8 to the
# right (default behaviour of the out() method).
delays = Delay(sf, lfos, feedback=0.5, mul=0.5).out()

'''
s.gui(locals())
#s.start()

#time.sleep(3)


#s.stop()
