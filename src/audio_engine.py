from pyo import *
from config import BASE_FREQUENCY, MAX_CHORD_NOTES

class ChordEngine:
    def __init__(self):
        self.s = Server(audio='coreaudio', nchnls=2, duplex=0).boot()
        self.s.start()

        self.saw_wave = SawTable(order=10)
        self.freqs = [Sig(0) for _ in range(MAX_CHORD_NOTES)]
        self.osc_list = [Osc(self.saw_wave, freq=f, mul=0.1) for f in self.freqs]
        self.osc_list += [Sine(f, mul=0.05) for f in self.freqs]
        self.osc_list += [Sine(f+(1/8), mul=0.05) for f in self.freqs]
        self.mix = sum(self.osc_list) / len(self.osc_list)
        self.mix.out()

    # def __init__(self):
    #     self.s = Server(audio='coreaudio', nchnls=2, duplex=0).boot()
    #     self.s.start()

    #     self.soft_wave = TriangleTable(order=3)
    #     self.freqs = [Sig(0), Sig(0), Sig(0), Sig(0)]
    #     self.osc_list = [Osc(self.soft_wave, freq=f, mul=0.1) for f in self.freqs]


    #     self.mix = sum(self.osc_list) / len(self.osc_list)

    #     self.filt_env = Adsr(attack=5, decay=2, sustain=0.7, release=8, dur=0, mul=400)
    #     self.lfo = Sine(freq=0.03, mul=150)
    #     self.filt = ButLP(self.mix, freq=800 + self.filt_env + self.lfo)

    #     self.soft_fuzz = Disto(self.filt, drive=0.2, slope=0.5)

    #     self.amp_env = Adsr(attack=3, decay=1, sustain=0.8, release=6, dur=0, mul=0.6)
    #     self.pad = self.soft_fuzz * self.amp_env
    #     self.amp_env.play()
    #     self.filt_env.play()

    #     self.chorused = Chorus(self.pad, depth=1.2, feedback=0.05, bal=0.5)
    #     self.rev = Freeverb(self.chorused, size=0.7, damp=0.6, bal=0.4).out()
        
    
    def play_chord(self, frequencies):
        if frequencies[0] is not None:
            for i in range(len(frequencies)):
                self.freqs[i].value = float(frequencies[i]) if frequencies[i] else 0

    def set_volume(self, volume):
        #input: volume: float between 0 and 1
        self.mix.mul = volume

