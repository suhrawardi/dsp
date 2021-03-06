from __future__ import print_function, division

import math
import random

import numpy as np

from signals.cos_signal import CosSignal
from signals.sin_signal import SinSignal
from signals.glottal_signal import GlottalSignal
from signals.parabolic_signal import ParabolicSignal
from signals.sawtooth_signal import SawtoothSignal
from signals.square_signal import SquareSignal
from signals.triangle_signal import TriangleSignal

from signals.sound_wave import SoundWave as Wave

from wav_file_writer import WavFileWriter


def make_note(midi_num, duration, sig_cons=CosSignal, framerate=11025):
    freq = midi_to_freq(midi_num)
    signal = sig_cons(freq)
    wave = signal.make_wave(duration, framerate=framerate)
    wave.apodize()
    return wave


def make_chord(midi_nums, duration, sig_cons=CosSignal, framerate=11025):
    freqs = [midi_to_freq(num) for num in midi_nums]
    signal = sum(sig_cons(freq) for freq in freqs)
    wave = signal.make_wave(duration, framerate=framerate)
    wave.apodize()
    return wave


def midi_to_freq(midi_num):
    x = (midi_num - 69) / 12.0
    freq = 440.0 * 2 ** x
    return freq


def sin_wave(freq, duration=1, offset=0):
    signal = SinSignal(freq, offset=offset)
    wave = signal.make_wave(duration)
    return wave


def cos_wave(freq, duration=1, offset=0):
    signal = CosSignal(freq, offset=offset)
    wave = signal.make_wave(duration)
    return wave


def mag(a):
    return np.sqrt(np.dot(a, a))


def main():
    cos_basis = cos_wave(440)
    sin_basis = sin_wave(440)

    wave = cos_wave(440, offset=math.pi / 2)
    cos_cov = cos_basis.cov(wave)
    sin_cov = sin_basis.cov(wave)
    print(cos_cov, sin_cov, mag((cos_cov, sin_cov)))

    wfile = WavFileWriter("a-note.wav")
    for m in range(60, 0, -1):
        wfile.write(make_note(m, 0.25))
    wfile.close()

    signal = GlottalSignal(440)
    signal.plot("glottalsignal")

    for sig_cons in [
        SinSignal,
        TriangleSignal,
        SawtoothSignal,
        GlottalSignal,
        ParabolicSignal,
        SquareSignal,
    ]:
        wfile = WavFileWriter(sig_cons.__name__ + ".wav")
        sig = sig_cons(440)

        wave = sig.make_wave(0.02)
        wave.apodize()
        wave.plot(sig_cons.__name__)

        wave = sig.make_wave(1)
        wave.apodize()
        wfile.write(wave)
        wfile.close()

    wave1 = make_note(69, 1)
    wave2 = make_chord([69, 72, 76], 1)
    wave = wave1 | wave2

    wfile = WavFileWriter("wave1_wave2.wav")
    wfile.write(wave)
    wfile.close()

    sig1 = CosSignal(freq=440)
    sig2 = CosSignal(freq=523.25)
    sig3 = CosSignal(freq=660)
    sig4 = CosSignal(freq=880)
    sig5 = CosSignal(freq=987)
    sig = sig1 + sig2 + sig3 + sig4 + sig5

    wave = sig.make_wave(0.02)
    wave.plot("sig5")

    wave = sig.make_wave(duration=1)
    wave.normalize()

    wfile = WavFileWriter()
    wfile.write(wave)
    wfile.close()


if __name__ == "__main__":
    main()
