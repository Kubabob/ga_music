from pyo import *

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
