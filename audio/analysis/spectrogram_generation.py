import numpy as np
from numpy.random._examples.cffi.extending import rng
from scipy import fft
from scipy import signal


def synthetic_signal_1():
    fs = 10e3
    N = 1e5
    NFFT = 1024
    amp = 2 * np.sqrt(2)
    noise_power = 0.01 * fs / 2
    time = np.arange(N) / float(fs)
    mod = 500 * np.cos(2 * np.pi * 0.25 * time)
    carrier = amp * np.sin(2 * np.pi * 3e3 * time + mod)
    noise = rng.normal(scale=np.sqrt(noise_power), size=time.shape)
    noise *= np.exp(-time / 5)
    x = carrier + noise
    return fs,x, NFFT


if __name__ == '__main__':
    from audio.audio_utils import read_audio_file
    import cv2
    import matplotlib.pyplot as plt

    rate, audio_data = read_audio_file('../../tmp_files/StarWars3.wav')
    # rate, audio_data, nfft = synthetic_signal_1()
    frequencies, times, spectrogram = signal.spectrogram(audio_data, rate)
    plt.pcolormesh(times, frequencies, spectrogram, shading='auto')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [ms]')
    plt.show()
