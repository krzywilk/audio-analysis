import numpy as np
from scipy import fft
from scipy import signal

if __name__ == '__main__':
    from audio.audio_utils import read_audio_file
    import cv2
    import matplotlib.pyplot as plt

    rate, audio_data = read_audio_file('../tmp_files/StarWars3.wav')
    frequencies, times, spectrogram = signal.spectrogram(audio_data, rate)
    plt.pcolormesh(times, frequencies, spectrogram)
    plt.imshow(spectrogram)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [ms]')
    plt.show()
