from pyo import *
import time

s = Server().boot()

#s.start()
class MyInstrument(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)

        # self.freq is derived from the 'degree' argument.
        self.phase = Phasor([self.freq, self.freq * 1.01])

        # self.dur is derived from the 'beat' argument.
        self.duty = Expseg([(0, 2), (self.dur, 0.4)], exp=4).play()

        self.osc = Compare(self.phase, self.duty, mode="<", mul=1, add=-0.3)
        #self.osc.ctrl()

        # EventInstrument created the amplitude envelope as self.env.
        self.filt = ButLP(self.osc, freq=10000, mul=self.env).out()

        
scl = EventScale('C', 'ionian')

# We tell the Events object which instrument to use with the 'instr' argument.
e = Events(
    instr=MyInstrument,
    midinote=EventSeq([scl[i] for i in range(4)], 1),
    beat=1 / 2.0,
    db=-12,
    attack=0.01,
    decay=0.05,
    sustain=0.7,
    release=0.01,
).play()

#s.gui(locals())
s.start()

time.sleep(2)


s.stop()