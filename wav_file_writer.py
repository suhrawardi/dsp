import numpy as np
from signals.silent_signal import SilentSignal
from wave import open as open_wave

class WavFileWriter:
    def __init__(self, filename="sound.wav", framerate=11025):
        self.filename = filename
        self.framerate = framerate
        self.nchannels = 1
        self.sampwidth = 2
        self.bits = self.sampwidth * 8
        self.bound = 2 ** (self.bits - 1) - 1

        self.fmt = "h"
        self.dtype = np.int16

        self.fp = open_wave("wavs/" + self.filename, "w")
        self.fp.setnchannels(self.nchannels)
        self.fp.setsampwidth(self.sampwidth)
        self.fp.setframerate(self.framerate)

    def write(self, wave):
        zs = wave.quantize(self.bound, self.dtype)
        self.fp.writeframes(zs.tostring())

    def close(self, duration=0):
        print("Writing " + self.filename)
        if duration:
            self.write(rest(duration))

        self.fp.close()

def rest(duration):
    signal = SilentSignal()
    wave = signal.make_wave(duration)
    return wave
